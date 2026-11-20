from langchain_core.prompts import ChatPromptTemplate
import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from config import DB_DIR, COLLECTION_name, EMBED_MODEL, API_key, TOP_K, Fetch_K, lambda_mult, CHAT_MODEL, Temperature, Max_Tokens
from ingest import ingestion_process
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Answer ONLY from from this context: {context}. Include citations for each retrieved doc in this format [file, page] for PDF files and in this format [file] for txt files. If answer used many retrieved files, after each paragraph include the file format for the file that used to writeexi this paragraph. If you don't find the answer in the context say I don't know the answer from the stored documents."),
    ("human","Question: {question}")])



def get_retriever(search_type: str):
    if not os.path.exists(DB_DIR):
        ingestion_process()
    
    embedding_model = OpenAIEmbeddings(model=EMBED_MODEL, api_key=API_key)
    chroma_vectorstore = Chroma(
        persist_directory=DB_DIR,
        embedding_function=embedding_model,
        collection_name=COLLECTION_name
    )

    if search_type.lower().strip() == "mmr":
        return chroma_vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": TOP_K, "fetch_k": Fetch_K, "lambda_mult": lambda_mult})
    
    elif search_type.lower().strip() == "similarity":
        return chroma_vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": TOP_K})
    
    else:
        raise "The search type must be mmr or similarity"
    



def format_docs(Docs: list):
    Docs_with_header = []
    for doc in Docs:
        if "page" in doc.metadata:
            Docs_with_header.append(f"{doc.page_content}\n [{doc.metadata['source'].split("\\")[-1]},p.{doc.metadata['page']+1}")
        else:
            Docs_with_header.append(f"{doc.page_content}\n [{doc.metadata['source'].split("\\")[-1]}")
            
    return "\n\n\n".join(Docs_with_header)



def build_rag_chain(question: str, search_type: str = "mmr") -> dict:
    retriever = get_retriever(search_type)
    Docs = retriever.invoke(question)
    context = format_docs(Docs)
    
    llm = ChatOpenAI(model=CHAT_MODEL, temperature=Temperature, max_tokens=Max_Tokens)
    
    chain = PROMPT | llm | StrOutputParser()
    response = chain.invoke({"context":context, "question":question})

    return {"question": question, "docs": Docs, "answer": response}