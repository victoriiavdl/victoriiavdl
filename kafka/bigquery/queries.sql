-- ============================================
-- Verification du chargement
-- ============================================
SELECT *
FROM `mosefadata.streamingsell`
LIMIT 10;


-- ============================================
-- Creation du modele K-means (BigQuery ML)
-- ============================================
CREATE OR REPLACE MODEL `mosefadata.mymodel`
OPTIONS(
  MODEL_TYPE = 'KMEANS',
  NUM_CLUSTERS = 4,
  STANDARDIZE_FEATURES = TRUE
) AS
SELECT
  CAST(SPLIT(location, ',')[OFFSET(0)] AS FLOAT64) AS longitude,
  CAST(SPLIT(location, ',')[OFFSET(1)] AS FLOAT64) AS latitude
FROM `mosefadata.streamingsell`;


-- ============================================
-- Visualisation des centroides
-- ============================================
SELECT *
FROM ML.CENTROIDS(MODEL `mosefadata.mymodel`);


-- ============================================
-- Vue analytique : CA par zone et type de produit
-- ============================================
CREATE OR REPLACE VIEW `mosefadata.v_chiffre_affaire_par_centroid_type` AS
WITH base AS (
  SELECT
    CAST(SPLIT(location, ',')[OFFSET(0)] AS FLOAT64) AS longitude,
    CAST(SPLIT(location, ',')[OFFSET(1)] AS FLOAT64) AS latitude,
    prix,
    typeproduit
  FROM `mosefadata.streamingsell`
),
pred AS (
  SELECT *
  FROM ML.PREDICT(MODEL `mosefadata.mymodel`, TABLE base)
)
SELECT
  CONCAT('Zone ', CAST(centroid_id + 1 AS STRING)) AS zone,
  typeproduit,
  SUM(prix) AS chiffre_affaire_total,
  COUNT(*) AS nombre_ventes,
  AVG(prix) AS prix_moyen
FROM pred
GROUP BY zone, typeproduit;


-- ============================================
-- Consultation des resultats
-- ============================================
SELECT *
FROM `mosefadata.v_chiffre_affaire_par_centroid_type`
ORDER BY zone, chiffre_affaire_total DESC;
