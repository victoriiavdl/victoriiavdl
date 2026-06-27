# Pipeline Kafka — Cloud Engineering (M2 MOSEF)

Pipeline de traitement de donnees en temps reel avec Kafka, OpenSearch, NiFi, BigQuery et BigQuery ML.

**Auteurs** : Juan, Victoria, Tasnim, Jorel, Melina, Amel

---

## Architecture

Le projet repose sur deux parcours complementaires :

### Parcours 1 : Streaming (Kafka + OpenSearch)

```
Producteur Python → Topic Kafka → Consommateur Python → OpenSearch → Dashboard
```

- **Producteur** (`producer/`) : genere des messages JSON (ventes avec localisation, prix, type de produit) et les envoie vers un topic Kafka
- **Consommateur** (`consumer/`) : lit les messages du topic et les indexe dans OpenSearch
- **OpenSearch** (`opensearch/`) : mapping des champs (geo_point, float, text, date), index pattern et visualisation via Discover/Dashboard
- **NiFi** : alternative low-code pour automatiser le flux Kafka → OpenSearch

### Parcours 2 : Analytique Cloud (BigQuery + BigQuery ML)

```
Donnees JSON → BigQuery → K-means (BigQuery ML) → Vue analytique
```

- **Chargement** (`bigquery/load_data.py`) : insertion de donnees JSON dans la table `mosefadata.streamingsell`
- **Clustering** (`bigquery/queries.sql`) : modele K-means pour segmenter les ventes par zone geographique
- **Vue analytique** : chiffre d'affaires, nombre de ventes et prix moyen par zone et type de produit

---

## Structure du projet

```
kafka/
├── producer/
│   └── kafka_producer.py       # Producteur Kafka
├── consumer/
│   └── kafka_consumer.py       # Consommateur Kafka → OpenSearch
├── opensearch/
│   ├── mapping.json            # Schema OpenSearch
│   └── create_index.py         # Creation de l'index
├── bigquery/
│   ├── load_data.py            # Chargement dans BigQuery
│   └── queries.sql             # K-means, vue analytique, requetes
├── docs/
│   ├── rapport.pdf             # Rapport complet
│   └── slides.pdf              # Slides de presentation
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

### 1. Creer l'index OpenSearch
```bash
cd opensearch && python create_index.py
```

### 2. Lancer le producteur
```bash
python producer/kafka_producer.py
```

### 3. Lancer le consommateur
```bash
python consumer/kafka_consumer.py
```

### 4. BigQuery
```bash
python bigquery/load_data.py
```
Les requetes SQL (K-means, vue analytique) sont dans `bigquery/queries.sql`.

---

## Stack

| Outil | Role |
|---|---|
| **Kafka** | Transport de messages en streaming |
| **OpenSearch** | Indexation et visualisation |
| **NiFi** | Automatisation du pipeline |
| **BigQuery** | Stockage analytique cloud |
| **BigQuery ML** | Clustering K-means |
