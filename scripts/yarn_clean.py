import pandas as pd
import sqlite3

df = pd.read_csv('../data/yarn.csv', low_memory=False)

#establish connection with db
conn = sqlite3.connect("yarn.db")
cursor = conn.cursor()

#create raw table from df
df.to_sql("yarn_raw", conn, if_exists='replace', index=False)
print("db yarn_raw created successfully")

#create table with just wanted columns
cursor.execute("""
DROP TABLE IF EXISTS yarn_clean;
""")

cursor.execute("""
CREATE TABLE yarn_clean AS
SELECT 
    name,
    yarn_company_name,
    grams,
    yardage,
    yarn_weight_wpi,
    yarn_weight_name,
    yarn_weight_knit_gauge,
    rating_average,
    rating_count,
    machine_washable,
    discontinued
FROM yarn_raw;
""")
print("yarn_clean table created successfully")

initial_rows = cursor.execute("SELECT COUNT(*) FROM yarn_clean").fetchall() #total rows before cleaning
print("The # of initial rows is:", initial_rows)

cursor.execute("""
               DELETE FROM yarn_clean WHERE
                   name is NULL or
                   yarn_company_name is NULL or
                   grams is NULL or
                   grams == 0 or
                   yardage is NULL or
                   yardage == 0 or
                   yarn_weight_wpi is NULL or
                   CAST(yarn_weight_wpi AS INTEGER) IS NULL OR
                   CAST(CAST(yarn_weight_wpi AS INTEGER) AS TEXT) != TRIM(yarn_weight_wpi);""") #to avoid wpi like 5-6



print('Rows from yarn_clean where required fields were NULL or inaccurate deleted successfully')

# the same yarn could be presented in skeins with the following format: 50g/200yards, 100g/400yards.
# To avoid this being interpreted as different, we add the ratio column; yards per grams:
cursor.execute("ALTER TABLE yarn_clean ADD COLUMN ratio REAL")
cursor.execute("UPDATE yarn_clean SET ratio = yardage/grams")
print("yarn_clean ratio column added successfully")

#we're also merging both rating columns
cursor.execute('''poner aqui la media de ambas''')

#OUTLIER FINDER------------------------------------------------------------------------------------------------------
#We want yarns that fit the following standards:
# 1 LACE                      550 - 800 YARDS PER 100G
# 2 FINGERING                 380 - 460 YARDS PER 100G
# 3 SPORT                     300 - 360 YARDS PER 100G
# 4 DK                        240 - 280 YARDS PER 100G
# 5 WORSTED                   200 - 240 YARDS PER 100G
# 6 ARAN                      120 -180 YARDS PER 100G
# 7 BULKY                     100 - 120 YARDS PER 100G
# 8 SUPER BULKY               <100 YARDS PER 100G
#____________________________________________________________________________________________________________________
outliers = cursor.execute('''SELECT * FROM yarn_clean WHERE ratio > 80''').fetchall()
print('There are', len(outliers), 'outliers')
#for i in outliers: print(i)
#After reviewing the data with external sources, it's clear that values with a ratio over 80
# do not fit on the lace to super bulky spectrum, so we'll remove them from the dataset.

cursor.execute('''DELETE FROM yarn_clean WHERE ratio > 80''').fetchall()
print('Outliers successfully deleted from yarn clean')

final_rows = cursor.execute("SELECT COUNT(*) FROM yarn_clean").fetchall() #total rows after cleaning.
print('Now the remaining # of rows is:', final_rows)


df2 = pd.read_sql_query("SELECT * FROM yarn_clean", conn)
df2.to_csv('../data/yarn_clean.csv', index=False) #saving yarn clean as csv
print("yarn_clean saved as CSV successfully")
conn.commit()
conn.close()
