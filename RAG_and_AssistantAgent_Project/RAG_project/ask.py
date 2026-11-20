from rag_chain import build_rag_chain
import numpy as np
import argparse

def main():
    
    parser = argparse.ArgumentParser(description="The retrieving method argument parser.")
    parser.add_argument("--search", type=str, default="mmr", help="Retrieving method argument (mmr/similarity).")
    
    arg = parser.parse_args()
    search_type = arg.search
    
    print(f"Your retrieving method now is: {search_type}")    
        
    while True:
        question = input("Please write your question! Or write 'exit' or 'quit' to stop!\n").strip().lower()
        if not question: 
            continue
        elif question in["exit", "quit"]:
            break
        else:
            try:
                response_dict = build_rag_chain(question, search_type)
                source_files_names = sorted(np.unique([doc.metadata["source"] for doc in response_dict["docs"]]).tolist())
                files_names = [file_name.split("\\")[-1] for file_name in source_files_names]
                print(f"Answer:\n{response_dict["answer"]} \n\nSource file names:\n{"\n".join(files_names)}\n\n")
                
            except Exception as error:
                print(f"\nAn error occurred while answering: {error}\n")
                
                


if __name__ == "__main__":
    main()