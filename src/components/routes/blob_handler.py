# Import handler libraries
from azure.storage.blob import BlobServiceClient
import io

# Define function to download blobs
def download_blobs(adls_connection_string, adls_container_name, adls_folder_name):
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=adls_connection_string)
    container_client = blob_service_client.get_container_client(adls_container_name)
    blob_data = {}
    for blob in container_client.list_blobs(name_starts_with=adls_folder_name):
        blob_client = container_client.get_blob_client(blob.name)
        blob_data[blob.name.split("/")[-1]] = io.BytesIO(blob_client.download_blob().readall())
    return blob_data

# Define function to upload blobs
def upload_blobs(adls_connection_string, adls_container_name, adls_folder_name, file_name, file_object):
        blob_service_client = BlobServiceClient.from_connection_string(adls_connection_string)
        container_client = blob_service_client.get_container_client(adls_container_name)
        blob_client = container_client.get_blob_client(adls_folder_name + file_name)
        blob_client.upload_blob(file_object, overwrite=True, blob_type="BlockBlob")

# Define function to wipe blobs
def wipe_blobs(adls_connection_string, adls_container_name, adls_folder_name):
     blob_service_client = BlobServiceClient.from_connection_string(adls_connection_string)
     container_client = blob_service_client.get_container_client(adls_container_name)
     blob_list = container_client.list_blobs(name_starts_with=adls_folder_name)
     for blob in blob_list:
          container_client.delete_blob(blob.name)