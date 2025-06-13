"""
    Description: Defines a Retreiver Tool For the Woodworking Documents 
    Author: Thomas Purk
    Date: 2025-06-05
    Reference: TODO

"""

import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.tools import Tool

# Load the local environment configuration
load_dotenv(".env.development.local")

# Load the FAISS vector store
embeddings = OpenAIEmbeddings()
faiss_store = FAISS.load_local(
    folder_path=os.environ['VECTOR_STORE_PATH'],
    embeddings=embeddings,
    allow_dangerous_deserialization=True # trusted pickles only
)

# Default - Similarity (Semantic) Search
# Default - Key Word Arguments "k" = 4, returns 4 results
retriever = faiss_store.as_retriever()

def retrieve_text(query: str) -> str:
    """Retrieves detailed information about gala guests based on their name or relation."""
    results = retriever.invoke(query)
    if results:
        return "\n\n".join([doc.page_content for doc in results])
    else:
        return "No matching guest information found."
    
woodworking_retriever_tool = Tool(
    name="woodworking_retriever",
    func=retrieve_text,
    description="Retrieves information regarding woodworking topics from a set a authoritative reputable texts."
)