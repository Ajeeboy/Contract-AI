# Import handler libraries
import hashlib
import tempfile
import os
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    CSVLoader,
    UnstructuredFileLoader
    )
from datetime import datetime, timezone
from langchain_core.documents import Document

# Import handler scripts
from components.config import config
from components.modules import indexes
from components.modules import models


# Define function for hashing
def hash_text(text: str):
    sha_hash = hashlib.sha256()
    sha_hash.update(text.encode("utf-8"))
    hashed_text = sha_hash.hexdigest()
    return hashed_text

# Define function for verifying vector db documents
def verify_vector_db(uploaded_documents):
    chunk_sources = indexes.index_retrieve_sources()
    embedded_files = {}
    unembedded_files = {}
    for file_name, file_bytes in uploaded_documents.items():
        if file_name in chunk_sources:
            embedded_files[file_name] = file_bytes
        if not file_name in chunk_sources:
            unembedded_files[file_name] = file_bytes
    return embedded_files, unembedded_files

# Define function to build vector data
def build_vector_data(unembedded_files):
    vector_data = []
    for file_name, file_bytes in unembedded_files.items():
        with tempfile.TemporaryDirectory() as temp_dir:     # TODO: still uses temp files and can't work around due to langchain requirements
            temp_file_path = os.path.join(temp_dir, file_name)
            with open(temp_file_path, "wb") as temp_file:
                temp_file.write(file_bytes.getvalue())
                temp_file.close()
            file_type = f"*.{file_name.split('.')[-1].lower()}"
            loader_type = config.loader_mappings.get(file_type)
            if loader_type == PyPDFLoader:
                loader = PyPDFLoader(temp_file_path, extract_images=True)
            elif loader_type == Docx2txtLoader:
                loader = Docx2txtLoader(temp_file_path)
            elif loader_type == TextLoader:
                loader = TextLoader(temp_file_path, autodetect_encoding=True, encoding="utf-8")
            elif loader_type == CSVLoader:
                loader = CSVLoader(temp_file_path, autodetect_encoding=True, encoding="utf-8")
            else:
                loader = UnstructuredFileLoader(temp_file_path)
            pages = loader.load()
            chunks = models.text_splitter.split_documents(pages)
            for i, chunk in enumerate(chunks):
                chunk_file_path = chunk.metadata["source"]
                vector_data.append({
                    "id": hash_text(chunk.page_content),
                    "content": chunk.page_content,
                    "content_vector": models.embeddings_client.embed_query(chunk.page_content),
                    "chunk_id": i,
                    "chunk_source": chunk_file_path.split("\\")[-1],
                    "chunk_type": chunk_file_path.split(".")[-1],
                    "chunk_datetime": datetime.now(timezone.utc).isoformat()
                    })
    return vector_data

# Define function to update vector database
def upload_vectors(uploaded_documents):
    embedded_files, unembedded_files = verify_vector_db(uploaded_documents)
    if len(unembedded_files) > 0:
        vector_data = build_vector_data(unembedded_files)
        models.search_client.upload_documents(documents=vector_data)        # TODO: doesn't update vectors of existing files at the moment
        return True
    else:
        file_chunk_datetimes = {}
        for file in embedded_files.keys():
            chunk_datetimes = indexes.index_retrieve_datetimes(file)
            file_chunk_datetimes[file] = sorted(chunk_datetimes, reverse=True)[0]
        return file_chunk_datetimes

# Define function to filter vector database
def filter_chunks(document):
    filtered_chunks = []
    for vector in models.search_client.search(search_text="*", filter=f"chunk_source eq '{document}'"):
        filtered_chunks.append(Document(page_content=vector["content"]))
    return filtered_chunks