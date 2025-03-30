import pandas as pd
import chromadb
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import OpenAI
import openai
import os
from dotenv import load_dotenv
import chromadb
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
from sentence_transformers import SentenceTransformer


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
if not openai_api_key:
    raise ValueError("Missing OpenAI API Key. Make sure your .env file is set up correctly.")


# Load CSV
def load_csv(csv_file):
    return pd.read_csv(csv_file)

df = load_csv("small_employee_dataset.csv")


# Initialize ChromaDB (Runs in-memory, no API needed)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Use a local embedding model (e.g., all-MiniLM-L6-v2)
embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vector_store = Chroma(collection_name="user_data", client=chroma_client, embedding_function=embedding_model)

# Insert data into ChromaDB
for _, row in df.iterrows():
    vector_store.add_texts(texts=[str(row)], metadatas=[row.to_dict()])

# Query function
def query_rag(user_query):
    docs = vector_store.similarity_search(user_query, k=3)
    retrieved_data = [doc.page_content for doc in docs]
    print("Retrieved Data:", retrieved_data)
    return retrieved_data

# Example query
query = "Only giver me details of Rahul"
retrieved_docs = query_rag(query)
print("Retrieved Documents:", retrieved_docs)