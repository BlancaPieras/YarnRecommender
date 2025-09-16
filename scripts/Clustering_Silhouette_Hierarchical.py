import sqlite3 as sql
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
import random
import numpy as np

#Because centroid initialization is random, we’ll fix a seed to ensure reproducibility.
random.seed(42)
np.random.seed(42)

#after previous exploration with kmeans and elbow method, let's try

conn = sql.connect('yarn.db')
cursor = conn.cursor()

cursor.execute('''DROP TABLE IF EXISTS main_columns''')
cursor.execute('''CREATE TABLE main_columns AS SELECT grams, yardage, yarn_weight_wpi, ratio FROM yarn_clean''') #create table
main_columns2 = pd.read_sql_query("SELECT * FROM main_columns", conn) # convert to df
main_columns2.to_csv('../data/main_columns2.csv', index=False) #save as csv

#NORMALIZE THE DATA
scaler = StandardScaler()
main_columns2_scaled = scaler.fit_transform(main_columns2)

# let's get the silhouette score in order to get the mean of
# s(i)=(b(i)−a(i))/max{a(i),b(i)} \in [-1,1] and decide which is the optimal k (the one that maximizes it)
# let's choose range 2,11 in order to prevent O(n^2) getting really high
k_range = range(2, 11)
best_k = k_range[0]
best_score = -1
sscores = []
for k in k_range:
    labels = AgglomerativeClustering(n_clusters=k, linkage='ward').fit_predict(main_columns2_scaled)
    score = silhouette_score(main_columns2_scaled, labels)
    scores.append([k,score])
    if score > best_score:
        best_score = score
        best_k = k

print('Best k = ', best_k, 'with score = ', best_score)

#create the model and labels
model = AgglomerativeClustering(n_clusters=best_k, linkage='ward')
cluster_labels = model.fit_predict(main_columns2_scaled)

#let's save it as csv and db
df2 = pd.DataFrame(main_columns2_scaled,columns=['grams_scaled','yardage_scaled','yarn_weight_wpi_sccaled','ratio_scaled'])
df2['cluster_labels'] = cluster_labels
df2.to_csv('../data/main_columns2_scaled_clustered.csv', index=False)

cursor.execute('''DROP TABLE IF EXISTS main_columns2_scaled_clustered''')
conn.commit()
df2.to_sql('main_columns2_scaled_clustered', conn, index=False, if_exists='replace')

#now we want to save cluster numbers in yarn_clean

#create the list of rowid
row_id = pd.read_sql_query('SELECT rowid AS rowid_mc2 FROM main_columns2', conn)
row_id['cluster'] = cluster_labels
row_id.to_sql('aux', conn, index=False, if_exists='replace')