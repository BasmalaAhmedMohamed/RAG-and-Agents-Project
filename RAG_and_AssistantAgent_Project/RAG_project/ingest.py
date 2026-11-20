from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
import shutil
import os
from langchain_openai import OpenAIEmbeddings
from config import EMBED_MODEL, API_key, DB_DIR, CHUNK_SIZE, CHUNK_OVERLAP, COLLECTION_name, PDF_path, TextFile_path



def load_documents(PDF_path: str, TextFile_path: str):
    try: 
        PDF_Loader = PyPDFLoader(PDF_path)
        Text_Loader = TextLoader(TextFile_path)
        
        PDF_Docs = PDF_Loader.load()
        Text_Doc = Text_Loader.load()
        return [PDF_Docs, Text_Doc]
    except:
        raise f"No files named {PDF_path.name} and {TextFile_path.name} in data dictionary!"
    
    

def split_documents(Docs_List: list):
    PDF_Docs = Docs_List[0]
    Text_Doc = Docs_List[1]
    splitter = RecursiveCharacterTextSplitter(chunk_size =CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP,separators=["\n\n","\n"])
    PDF_splitted_Docs = splitter.split_documents(PDF_Docs)
    TextFile_splitted_Docs = splitter.split_documents(Text_Doc)
    return [PDF_splitted_Docs, TextFile_splitted_Docs]




def build_vector_store(All_splitted_Docs: list):
    embedding_model = OpenAIEmbeddings(model=EMBED_MODEL, api_key=API_key)

    if os.path.exists(DB_DIR):
        shutil.rmtree(DB_DIR)

    chroma_db = Chroma.from_documents(documents=All_splitted_Docs, embedding=embedding_model, collection_name=COLLECTION_name, persist_directory=str(DB_DIR))
    chroma_db.persist()


def ingestion_process():
    try: 
        Docs = load_documents(PDF_path, TextFile_path)
    except:
        raise "No files with these paths in data dictionary!"
    
    splitted_Docs_List = split_documents(Docs)
    print(f"PDF file is splitted into -> {len(splitted_Docs_List[0])} chunks.\n Text file is splitted into -> {len(splitted_Docs_List[1])} chunks.\n")
    build_vector_store (splitted_Docs_List[0] + (splitted_Docs_List[1]))
    return 



if __name__ == "__main__":
    ingestion_process()