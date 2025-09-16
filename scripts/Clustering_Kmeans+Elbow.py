import sqlite3 as sql
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import random
import numpy as np

#Because centroid initialization is random, we’ll fix a seed to ensure reproducibility.
random.seed(42)
np.random.seed(42)

#preliminary exploration of clustering with k-means and elbow method

conn = sql.connect('yarn.db')
cursor = conn.cursor()

#CREATE THE MAIN COLUMNS TABLE FOR CLUSTERING
cursor.execute('''DROP TABLE IF EXISTS main_columns''')
cursor.execute('''CREATE TABLE main_columns AS SELECT grams, yardage, yarn_weight_wpi, ratio FROM yarn_clean''') #create table
main_columns = pd.read_sql_query("SELECT * FROM main_columns", conn) # convert to df
main_columns.to_csv('../data/main_columns.csv', index=False) #save as csv

#NORMALIZE THE DATA
scaler = StandardScaler()
main_columns_scaled = scaler.fit_transform(main_columns)

#Clusters we're looking for:--------------------------------------------------------------------------------------------

# 1 LACE                      550 - 800 YARDS PER 100G
# 2 FINGERING                 380 - 460 YARDS PER 100G
# 3 SPORT                     300 - 360 YARDS PER 100G
# 4 DK                        240 - 280 YARDS PER 100G
# 5 WORSTED                   200 - 240 YARDS PER 100G
# 6 ARAN                      120 -180 YARDS PER 100G
# 7 BULKY                     100 - 120 YARDS PER 100G
# 8 SUPER BULKY               <100 YARDS PER 100G

#Therefore ideal k is 8
#-----------------------------------------------------------------------------------------------------------------------

#Let's see how many clusters are there with the elbow curve
wcss = []
for i in range(2, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0).fit(main_columns_scaled)
    wcss.append(kmeans.inertia_)
#Plot the elbow curve
plt.plot(range(2, 11), wcss, marker='o')
plt.title('The Elbow Module Plot')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.show()
#conclussion: Between 5 and 7 clusters is the optimal number.


#START CLUSTERING, fit kmeans with 6 clusters
km = KMeans(n_clusters = 6, init='k-means++', max_iter=300, n_init=10, random_state = 0).fit(main_columns_scaled)
#cluster labels
cluster_labels = km.labels_
#visualize clusters in 2D using last 2 features, wpi and ratio
plt.scatter(main_columns_scaled[:, 2], main_columns_scaled[:, 3], c = cluster_labels, cmap = 'viridis', s = 50, alpha = 0.5)
plt.scatter(km.cluster_centers_[:, 2], km.cluster_centers_[:, 3], c = 'red', marker = 'x', s = 200, label = 'Center', alpha = 0.5)
plt.xlabel('x: wpi standarized')
plt.ylabel('y: ratio standarized')
plt.title('Clustering Results k=6')
plt.legend()
plt.show()
#Obviously, wpi is a discrete number that differenciates yarn thicknesses -> clusters appear in columns

df = pd.DataFrame(main_columns_scaled, columns = ['grams scaled', 'yards scaled', 'wpi scaled', 'ratio scaled'])
df['cluster'] = cluster_labels
df.to_csv('../data/main_columns_scaled_clustered.csv', index=False)

conn.commit()
conn.close()
