# Description: Conver Text Files into a vector store of embeddings
# Author: Thomas Purk
# Date: 2025-04-15
# Reference: 

import os
import json
from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load the local environment configuration
load_dotenv(".env.development.local")
CORPUS_PATH = os.environ['CORPUS_PATH']
VECTOR_STORE_PATH = os.environ['VECTOR_STORE_PATH']


def load_files(corpus_path: str) -> list:
    """ Reads the files with a TXT extension in the specified folder. Loads the text into a list.

        Args:
            corpus_path (str): A JSON array document containing objects with a file property that stores the relative path to the file Example [{'file': 'documents/filename.txt'}]
        
        Returns
            list: A list containing LangChain documents.
    """

    # Instantiate a text splitter object to split into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    corpus_path_root = os.path.dirname(corpus_path)
    with open(corpus_path, 'r') as file:
        corpus = json.load(file)

    # Iterate over the files and add loaded docs to the list
    documents = []
    for item in corpus:
        file_path = os.path.join(corpus_path_root, item["file"])
        loader = TextLoader(file_path)
        cur_docs = loader.load()
        cur_docs = text_splitter.split_documents(cur_docs)
        documents.extend(cur_docs)
    
    # Function return
    return documents

# Get documents
documents = load_files(CORPUS_PATH)

# Create Vector Store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(
    documents=documents,
    embedding=embeddings
)

# Save Vector Store to disk
vectorstore.save_local(VECTOR_STORE_PATH)

