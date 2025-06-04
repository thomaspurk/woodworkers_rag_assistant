# Description: Conver Text Files into a vector store of embeddings
# Author: Thomas Purk
# Date: 2025-04-15
# Reference: ChatGPT

import os
import random
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Load the local environment configuration
load_dotenv(".env.development.local")
VECTOR_STORE_PATH = os.environ['VECTOR_STORE_PATH']

embeddings = OpenAIEmbeddings()


# Load the FAISS vector store
faiss_store = FAISS.load_local(
    folder_path= VECTOR_STORE_PATH ,
    embeddings=embeddings,
    allow_dangerous_deserialization=True # trusted pickles only
    )

# FAISS index info
faiss_index = faiss_store.index
num_vectors = faiss_index.ntotal
vector_dimension = faiss_index.d
index_type = type(faiss_index).__name__


document_ids = list(faiss_store.index_to_docstore_id.values())
num_documents = len(document_ids)

print(f"\n{"-" * 50}\n")
print("FAISS Vector Store Summary:")
print(f"- Index Type       : {index_type}")
print(f"- Total Vectors    : {num_vectors}")
print(f"- Vector Dimension : {vector_dimension}")
print(f"- Total Documents  : {num_documents}")
print(f"\n{"-" * 50}\n")

sample_docs = random.sample(
    population=document_ids, 
    k=min(3, num_documents)
)

print("Vector Store Document Samples:")
for i in sample_docs:
    doc =faiss_store.get_by_ids([i])[0]
    print(f"\n--- Document {i} ---")
    print(f"Content: {doc.page_content[:200]}...")  # Truncate to first 200 chars
    print(f"Metadata: {doc.metadata}")