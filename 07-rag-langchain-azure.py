import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from bs4 import SoupStrainer
from langchain.tools import tool
from langchain.agents import create_agent


load_dotenv()

# The LLM in RAg Pipeline
model = AzureChatOpenAI(
    azure_deployment= 'gpt-4.1',
    model= 'gpt-4.1',
    api_version='2025-01-01-preview'
)

# Embeddings Model Configuration
embeddings = AzureOpenAIEmbeddings(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["OPENAI_EMBEDDING_MODEL"],
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
)

# Use in memory vector store for simplicity
vector_store = InMemoryVectorStore(embeddings)

def load_documents(url: str = "https://lilianweng.github.io/posts/2023-06-23-agent/"):
    # Only keep post title, headers, and content from the full HTML.
    bs4_strainer = SoupStrainer(class_=("post-title", "post-header", "post-content"))
    loader = WebBaseLoader(
        web_paths=(url,),
        bs_kwargs={"parse_only": bs4_strainer},
    )
    # Load the documents frqom the web page
    docs = loader.load()
    print(f"Total documents loaded: {len(docs)}")
    print(f"Total documents loaded: {docs[0].page_content[:500]}...")
    return docs


# Split the documents into smaller chunks
def split_text(docs: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    splits = text_splitter.split_documents(docs)
    print(f"Total splits: {len(splits)}")
    return splits

# Index the documents
def index_documents(docs):
    vector_store = InMemoryVectorStore(embeddings)
    return vector_store.add_documents(docs)

# Execute the RAG pipeline (Indexing)
doc_ids = index_documents(split_text(load_documents()))

# Define a simple retrieval function
@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information to help answer a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        f"Source:{doc.metadata} \n Content:{doc.page_content}" 
        for doc in retrieved_docs
        )
    return serialized, retrieved_docs

def get_tools():
    return [retrieve_context]

def get_system_prompt():
    return (
        "You have access to a tool that retrieves context from a blog post"
        "Use the tool to help answer user queries"
    )

def get_agent():
    return create_agent(model, [retrieve_context], system_prompt = get_system_prompt())

query = (
    "What is the standard method for Task Decomposition?\n\n"
    "Once you get the answer, look up common extensions of that method."
)

for event in get_agent().stream(
    {"messages": [{"role": "user", "content": query}]},
    stream_mode="values",
):
    event["messages"][-1].pretty_print()




