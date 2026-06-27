from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import datetime, UTC

project_id = "juancloudproject"
table_id = "juancloudproject.mosefadata.streamingsell"
key_path = "/content/juancloudproject.json"

credentials = service_account.Credentials.from_service_account_file(key_path)
client = bigquery.Client(credentials=credentials, project=project_id)

rows_to_insert = [
    {
        "location": "14.76, -14.76",
        "prix": 10.5,
        "typeproduit": "fruit",
        "agent_timestamp": datetime.now(UTC).isoformat()
    },
    {
        "location": "10.76, -14.76",
        "prix": 20.75,
        "typeproduit": "legume",
        "agent_timestamp": datetime.now(UTC).isoformat()
    }
]

errors = client.insert_rows_json(table_id, rows_to_insert)
if not errors:
    print("Insertion reussie")
else:
    print("Erreurs :", errors)
