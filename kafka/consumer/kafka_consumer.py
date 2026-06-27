from kafka import KafkaConsumer
from opensearchpy import OpenSearch
import json

consumer = KafkaConsumer(
    'streaming-sales',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9200}],
    http_compress=True
)

index_name = 'streaming-sales-index'

if __name__ == "__main__":
    print(f"Consommateur Kafka demarre, indexation vers '{index_name}'")
    try:
        for msg in consumer:
            document = msg.value
            client.index(index=index_name, body=document)
            print(f"Document indexe dans OpenSearch: {document}")
    except KeyboardInterrupt:
        print("Consommateur arrete.")
    finally:
        consumer.close()
