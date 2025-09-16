# YarnRecommender
*Project status: Work in progress*

This repository contains a yarn recommendation engine using Python, scikit-learn, and SQLite. The system helps knitters and crocheters find the closest matching yarn to the one specified in a pattern. Recommendations are based on yarn characteristics, clustering, and user ratings.

**It is designed as a portfolio project to showcase skills in data analysis, machine learning, and software engineering for recommender systems.**

## Project overview
1. **Data cleaning**
   - Load raw yarn data (`yarn.csv`) into SQLite.
   - Clean inconsistencies.
   - Compute **yards per gram ratio** feature.
   - Save cleaned dataset: `yarn_clean`.

2. **Features and clustering**
   - Extract relevant features: `grams`, `yardage`, `yarn_weight_wpi`, `ratio`.
   - Standardize with `StandardScaler`.
   - Find the optimal number of clusters k.
   - Apply Agglomerative Clustering.
   - Assign each yarn to a cluster and apply labels to `yarn_clean`.

3. **Recommendation engine**
   - User provides yarn details (grams and yardage per skein) by console.
   - The system:
     - Normalizes the input
     - Assigns it to the closest cluster
     - Computes optimized distances to all yarns in that cluster
     - Ranks candidates using a **KPI** that combines distance and user ratings
   - Returns the top-3 best yarn matches.

## Tech
- Python (pandas, numpy, scikit-learn, matplotlib)
- SQLite (structured storage, SQL queries)
- scikit-learn (clustering, scaling, similarity)

## Key Features
- Deterministic results (random seed fixed to 42).
- Hierarchical clustering with optimal k chosen by Silhouette score.
- Bayesian rating adjustment to balance quality vs popularity.
- KPI combining similarity distance and ratings for meaningful recommendations.

## This project demonstrates:
- Data cleaning and preprocessing pipelines (ETL).
- Database integration with SQLite.
- Unsupervised machine learning (KMeans vs Agglomerative).
- Model selection using Silhouette analysis.
- Practical recommendation system design.
- Code structuring and reproducibility best practices.

### This project is not finished yet.  
Some scripts are exploratory, and the recommendation engine is still being improved.  
Future work includes:
- KPI scoring function
- Finalizing cluster evaluation
- Cleaning the database pipeline
