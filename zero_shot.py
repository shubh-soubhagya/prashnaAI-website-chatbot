import os
import logging
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.agents import create_openai_tools_agent
from langchain.agents import AgentExecutor
import time
from dotenv import load_dotenv

load_dotenv()
logging.getLogger("langchain").setLevel(logging.ERROR)  # Suppress unnecessary logs

groq_api_key = os.getenv('GROQ_API_KEY')

# Load PDFs
loader = PyPDFDirectoryLoader(r".\pdf_app_test")
docs = loader.load()
print(f"✅ Loaded {len(docs)} documents successfully.")

documents = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0).split_documents(docs)
print(f"✅ Successfully split into {len(documents)} text chunks.")

# Embedding Model
embeddings_model = HuggingFaceEmbeddings(model_name=r"C:\Users\hp\Desktop\prashna\models\all-MiniLM-L6-v2")
vectordb = FAISS.from_documents(documents, embeddings_model)
retriever = vectordb.as_retriever()

from langchain.tools.retriever import create_retriever_tool
pdf_tool = create_retriever_tool(retriever, "pdf_search", "Search for PDF information only!")

tools = [pdf_tool]

# Load LLaMA 3 (via GROQ)
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-8b-8192")

# Prompt Setup
prompt = ChatPromptTemplate.from_template(
"""
Answer the questions based on the provided PDF context only.
Provide accurate and detailed responses strictly from the PDF content.
<context>
{context}
<context>
Questions:{input}
{agent_scratchpad}
"""
)

agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

while True:
    query = input("Input your query here: ")
    if query.lower() in ["exit", "quit", "q"]:
        print("Exiting... Goodbye!")
        break

    start_time = time.time()
    try:
        response = agent_executor.invoke({
            "input": query,
            "context": "",
            "agent_scratchpad": ""
        })
        print(f"\n🟩 Final Output:\n{response['output']}")
        print(f"⏱️ Total Response Time: {time.time() - start_time:.2f} seconds")

    except Exception as e:
        print(f"❗ Error: {e}") 