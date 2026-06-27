from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime, UTC

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic_name = 'streaming-sales'

produits = ['fruit', 'legume', 'viande', 'poisson', 'boisson']
locations = [
    (14.76, -14.76),
    (10.76, -14.76),
    (48.85, 2.35),
    (33.59, -7.61),
    (5.32, -4.01),
]


def generate_message():
    loc = random.choice(locations)
    return {
        "location": f"{loc[0]}, {loc[1]}",
        "prix": round(random.uniform(1.0, 50.0), 2),
        "typeproduit": random.choice(produits),
        "agent_timestamp": datetime.now(UTC).isoformat()
    }


if __name__ == "__main__":
    print(f"Producteur Kafka demarre sur le topic '{topic_name}'")
    try:
        while True:
            message = generate_message()
            producer.send(topic_name, value=message)
            producer.flush()
            print(f"Message envoye: {message}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Producteur arrete.")
    finally:
        producer.close()
