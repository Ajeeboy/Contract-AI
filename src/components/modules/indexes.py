# Import handler libraries
import requests

# Import handler scripts
from components.config import config


# Define function to delete existing index
def index_delete():
    api_url = f"https://{config.search_name}.search.windows.net/indexes/{config.search_index}?api-version={config.search_version}"
    api_headers = {
        "Content-Type": "application/json",
        "api-key": config.search_admin_key
        }
    api_response = requests.delete(api_url, headers = api_headers)
    return api_response.status_code

# Define function to create new index
def index_create():
    api_url = f"https://{config.search_name}.search.windows.net/indexes/{config.search_index}?api-version={config.search_version}"
    api_headers = {
        "Content-Type": "application/json",
        "api-key": config.search_admin_key
        }
    index_schema = {
        "name": config.search_index,
        "fields": [
            {"name": "id", "type": "Edm.String", "key": True, "searchable": True, "filterable": True, "sortable": True, "facetable": True},
            {"name": "content", "type": "Edm.String", "searchable": True, "filterable": True, "sortable": True, "facetable": True, "analyzer": "standard.lucene"},
            {"name": "content_vector", "type": "Collection(Edm.Single)", "searchable": True, "dimensions": 1536, "vectorSearchProfile": "vector-profile"},
            {"name": "chunk_id", "type": "Edm.Int64", "searchable": False, "filterable": True, "sortable": True, "facetable": True},
            {"name": "chunk_source", "type": "Edm.String", "searchable": True, "filterable": True, "sortable": True, "facetable": True, "analyzer": "standard.lucene"},
            {"name": "chunk_type", "type": "Edm.String", "searchable": True, "filterable": True, "sortable": True, "facetable": True, "analyzer": "standard.lucene"},
            {"name": "chunk_datetime", "type": "Edm.DateTimeOffset", "searchable": False, "filterable": True, "sortable": True, "facetable": True}
            ],
        "similarity": {"@odata.type": "#Microsoft.Azure.Search.BM25Similarity", "k1": None, "b": None},
        "vectorSearch": {
            "algorithms": [{"name": "vector-config", "kind": "hnsw", "hnswParameters": {"metric": "cosine", "m": 4, "efConstruction": 400, "efSearch": 500}}],
            "profiles": [{"name": "vector-profile", "algorithm": "vector-config"}]
            }
        }
    api_response = requests.put(api_url, headers = api_headers, json = index_schema)
    return api_response.status_code

# Define function to pull distinct chunk_source values
def index_retrieve_sources():
    api_url = f"https://{config.search_name}.search.windows.net/indexes/{config.search_index}/docs/search?api-version={config.search_version}"
    api_headers = {
        "Content-Type": "application/json",
        "api-key": config.search_query_key
        }
    api_body = {
        "count": True,
        "facets": ["chunk_source"],
        "search": "*",
        "select": "chunk_source"
        }
    api_response = requests.post(api_url, headers=api_headers, json=api_body)
    facets = api_response.json().get("@search.facets", {})
    chunk_sources = [facet["value"] for facet in facets.get("chunk_source", [])]
    return chunk_sources

# Define function to pull last chunk_datetime values
def index_retrieve_datetimes(file_name):
    api_url = f"https://{config.search_name}.search.windows.net/indexes/{config.search_index}/docs/search?api-version={config.search_version}"
    api_headers = {
        "Content-Type": "application/json",
        "api-key": config.search_query_key
        }
    api_body = {
        "count": True,
        "facets": ["chunk_datetime"],
        "search": "*",
        "select": "chunk_datetime",
        "filter": f"chunk_source eq '{file_name}'"
        }
    api_response = requests.post(api_url, headers=api_headers, json=api_body)
    facets = api_response.json().get("@search.facets", {})
    chunk_datetimes = [facet["value"] for facet in facets.get("chunk_datetime", [])]
    return chunk_datetimes