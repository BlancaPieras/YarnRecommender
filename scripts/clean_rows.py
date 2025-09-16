import pandas as pd
import sqlite3

# This script removes rows from 'yarn_clean' where critical fields are NULL

conn = sqlite3.connect("yarn.db")
cursor = conn.cursor()

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

final_rows = cursor.execute("SELECT COUNT(*) FROM yarn_clean").fetchall() #total rows after cleaning.

print('Rows from yarn_clean where required fields were NULL deleted successfully')
print('Now the remaining # of rows is:', final_rows)
print('clean_rows CSV created successfully')

# the same yarn could be presented in skeins with the following format: 50g/200yards, 100g/400yards.
# To avoid this being interpreted as different, we add the ratio column; yards per grams:
cursor.execute("ALTER TABLE yarn_clean ADD COLUMN ratio REAL")
cursor.execute("UPDATE yarn_clean SET ratio = yardage/grams")
print("yarn_clean ratio column added successfully")

df = pd.read_sql_query("SELECT * FROM yarn_clean", conn)
df.to_csv('../data/clean_rows.csv', index=False)

conn.commit()
conn.close()