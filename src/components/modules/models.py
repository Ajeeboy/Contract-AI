# Import handler libraries
import openai
from langchain_openai import AzureOpenAIEmbeddings
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureChatOpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Import handler scripts
from components.config import config


# Set OpenAI variables
openai.api_type = config.openai_type
openai.api_key = config.openai_key
openai.api_base = config.openai_base
openai.api_version = config.openai_version

# Create embeddings model
embeddings_client = AzureOpenAIEmbeddings(
    azure_endpoint=config.openai_base,
    deployment=config.openai_embedding_deployment,
    model=config.openai_embedding_model,
    openai_api_key=config.openai_key,
    openai_api_type=config.openai_type,
    openai_api_version=config.openai_version
    )

# Create vector model
vector_client = AzureSearch(
    azure_search_endpoint=config.search_endpoint,
    azure_search_key=config.search_admin_key,
    index_name=config.search_index,
    embedding_function=embeddings_client.embed_query
    )

# Create llm model
llm_client = AzureChatOpenAI(
    azure_endpoint=config.openai_base,
    deployment_name=config.openai_gpt_deployment,
    openai_api_key=config.openai_key,
    openai_api_version=config.openai_version
    )

# Create search model
search_client = SearchClient(
    endpoint=config.search_endpoint,
    index_name=config.search_index,
    credential=AzureKeyCredential(config.search_admin_key)
    )

# Create stuff chain
stuff_chain = create_stuff_documents_chain(
    llm_client,
    config.prompt_template
    )

# Create retrieval chain
retrieval_chain = create_retrieval_chain(
    vector_client.as_retriever(),
    stuff_chain
    )

# Create text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)