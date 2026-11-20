from datetime import datetime
from langchain_core.tools import tool
import ast
import operator
import numpy as np

from pathlib import Path
import sys

RAG_project_Path = Path(__file__).resolve().parent.parent/"RAG_project"
sys.path.insert(0, str(RAG_project_Path))

from rag_chain import build_rag_chain

GRADES = {
    "mona": {"math": 92, "ai": 81},
    "ali": {"math": 80, "ai": 90},
    "salma": {"math": 60, "ai": 80},
}


operations = {ast.Add: operator.add,
              ast.Sub: operator.sub,
              ast.Mult: operator.mul,
              ast.Div: operator.truediv,
              ast.Pow: operator.pow,
              ast.UAdd: operator.pos,
              ast.USub: operator.neg}



def calculate_expression_parts(part: str):
    if isinstance (part, ast.Constant):
        return part.value
    elif isinstance (part, ast.BinOp):
        left = calculate_expression_parts(part.left)
        right = calculate_expression_parts(part.right)
        result = operations[type(part.op)](left,right)
        return result
    elif isinstance (part, ast.UnaryOp):
        operand = calculate_expression_parts(part.operand)
        return operations[type(part.op)](operand)
    else:
        raise ValueError("Expression is not allowed!")
          
          
          
@tool
def calculator(expression: str):
    """ calculate an expression as +, -, *, / and **. Used when user ask for calculation request"""
    tree = ast.parse(expression, mode="eval")
    if isinstance(tree, ast.Expression):
        result =  calculate_expression_parts(tree.body)
        return result


@tool
def current_datetime():
    """ Return current datetime. Uesd when user ask for time or date. """
    return datetime.now().strftime("%A %d %B %Y, %H:%M")



@tool
def get_student_grades(name: str):
    """ Search for student's grades. Used when user ask for a student's grade. """
    grades = GRADES.get(name.strip().lower())
    if not grades:
        return f"There is no student called {name.strip()} in grades."
    return grades


@tool
def save_note(note: str):
    """ Append notes to notes.txt file. Used when user ask for save a note. """
    with open("notes.txt", "a", encoding="utf-8") as file:
        file.write(note + "\n")
    return "Save successful!"


@tool
def read_notes():
    """ Read notes from notes.txt file and return it to the user. Used when user ask about notes."""
    with open("notes.txt", "r", encoding="utf-8") as file:
        content = file.read()
    return content


@tool
def add_student(name: str, math: int, ai:int):
    """ Add student data in students' grades. Used when user ask for adding a student and give its name and scores in math and ai subjects."""
    GRADES[name.lower().strip()] = {"math": math, "ai": ai}
    return "Add successful!"





@tool
def ask_documents(question: str):
    """ Answer questions from RAG chain of project 1. Used when user ask question not about students or their grades."""
    try:
        response_dict = build_rag_chain(question)
        source_files_names = sorted(np.unique([doc.metadata["source"] for doc in response_dict["docs"]]).tolist())
        files_names = [file_name.split("\\")[-1] for file_name in source_files_names]
        return f"Answer:\n{response_dict["answer"]} \n\nSource file names:\n{"\n".join(files_names)}\n\n"
    except:
        return "Error while calling ask_documents tool!"


ALL_TOOLS = [calculator, current_datetime, get_student_grades, save_note, read_notes, add_student, ask_documents]

