# Import handler libraries
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    CSVLoader
    )


# Set openai configs
openai_type = "azure"
openai_embedding_model = "text-embedding-ada-002"
openai_gpt_model = "gpt-4"

# Set azure search configs
search_version = "2024-02-01"

# Set blob storage configs
adls_container_input = "landing-zone"
adls_folder_files_input = "files/webapp/"
adls_folder_questions_input = "questions/webapp/" 
adls_container_output = "processing-zone"
adls_folder_files_output = "files/webapp/"
adls_folder_questions_output = "answers/webapp/"

new_configs = False

if not new_configs:
    # Set openai configs
    openai_key = "ec8bdbcae2794f0b86858b8f6674add1"
    openai_base = "https://contract-ai-oai.openai.azure.com/"
    openai_version = "2023-12-01-preview"
    openai_embedding_deployment = "contract-ai-oai-embedding"
    openai_gpt_deployment = "contract-ai-oai-gpt"

    # Set azure search configs
    search_name = "contract-ai-srch"
    search_endpoint = "https://contract-ai-srch.search.windows.net"
    search_index = "contract-ai-srch-index"
    search_admin_key = "Ne5GdyRY5QWeGCN6RPEZHs2khjWlPHRhK4qeJUo67rAzSeDDhnDP"
    search_query_key = "diQpWak4rlg96iSMBjhnMNZhaMUlOgDDX54yUdaYRjAzSeAB6Q64"

    # Set blob storage configs
    adls_connection_string = "DefaultEndpointsProtocol=https;AccountName=contractaist;AccountKey=fFa02I7n2sM2JPTCdrqenuEemYj+dE+krK4pK/xEmWp5ZV5Onvy/AL54IJCeDi7619AJKmFNpr2e+AStj7Zn3w==;EndpointSuffix=core.windows.net"

elif new_configs:
    # Set openai configs
    openai_key = "51350949220945568a33356a0b8b53fd"
    openai_base = "https://contract-ai-demo-oai.openai.azure.com/"
    openai_version = "turbo-2024-04-09"
    openai_embedding_deployment = "contract-ai-demo-oai-embedding"
    openai_gpt_deployment = "contract-ai-demo-oai-gpt"

    # Set azure search configs
    search_name = "contract-ai-demo-srch"
    search_endpoint = "https://contract-ai-demo-srch.search.windows.net"
    search_index = "contract-ai-demo-srch-index"
    search_admin_key = "VXkKkd7bnhRVlgopHN7p8TzQL4agmVmUmauWKEsHH3AzSeCD0F9G"
    search_query_key = "SwYQg2DGdPtUn6iUa5DyOG3BquR6nwKJWS5pmrUDpNAzSeAGcrpY"

    # Set blob storage configs
    adls_connection_string = "DefaultEndpointsProtocol=https;AccountName=contractaidemost;AccountKey=tSDcTRPJcZkdw57ybh1IuWmm9EiRe/SQi46bUUyVDVDYK6KW5aGAhbyDNnz27JxIpPWgLq/mSPAK+AStLrEauQ==;EndpointSuffix=core.windows.net"

# Set prompt template config
prompt_template = PromptTemplate.from_template("""
    Your response to the given question should be factual and as accurate as possible, solely based on the provided context.
    Your response should state the answer as concisely as possible and then concisely provide any surrounding context of where the answer can be found in the document.
    You may use synonyms of the words in the given question to help search for an answer.
    If you cannot answer the given question with certainty then please state that fact and end your response.
    The question you are being presented with is between the following set of exclamation points: !{question}!
    The context which you may use to respond to this question can be found after this colon:
    {context}
    """)

# Set loader mapping config
loader_mappings = {
    "*.pdf": PyPDFLoader,
    "*.docx": Docx2txtLoader,
    "*.txt": TextLoader,
    "*.csv": CSVLoader
    }

# Set webapp steps config
webapp_steps = [
    "Start",
    "Select Documents",
    "Set Questions",
    "Review & Submit",
    "Review Outputs"
    ]