from opensearchpy import OpenSearch
import json

client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_compress=True
)

index_name = 'streaming-sales-index'

with open('mapping.json', 'r') as f:
    mapping = json.load(f)

if client.indices.exists(index=index_name):
    client.indices.delete(index=index_name)
    print(f"Index '{index_name}' supprime.")

response = client.indices.create(index=index_name, body=mapping)
print(f"Index '{index_name}' cree: {response}")
