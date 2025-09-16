import sqlite3

import pandas as pd

conn = sqlite3.connect('yarn.db')
cursor = conn.cursor()

#--------How many brands are there?------------
print("-----HOW MANY BRANDS ARE THERE?-----")
    #SQLite
cursor.execute("SELECT COUNT (DISTINCT yarn_company_name) FROM yarn_clean")
no_brands = cursor.fetchall()
print('SQLite -> There are', no_brands, 'unique brands')

    #PANDAS
df = pd.read_sql_query("SELECT * FROM yarn_clean", conn)

print('PANDAS -> There are', df['yarn_company_name'].nunique(), ' unique brands')

#---------How many yarns per brand?---------
print("-----HOW MANY YARNS PER BRAND?-----")
    #SQLite
print('SQLite ->')
cursor.execute("""SELECT yarn_company_name, 
COUNT(*) AS no_total_yarns 
FROM yarn_clean 
GROUP BY yarn_company_name 
ORDER BY no_total_yarns DESC
""") #counts the nº of unique yarns that each brand has

for i in cursor.fetchmany(10): #let's print just 10 of them
   print(i)
print('...')

    #PANDAS
print('PANDAS ->')
print(df['yarn_company_name'].value_counts())


#--------How many yarn weights are there?-------
print('---------HOW MANY YARN WEIGHTS, WHICH ONES, AND HOW MANY YARNS PER WEIGHT?------------')
print('SQLite ->')

cursor.execute("""SELECT COUNT (DISTINCT yarn_weight_name) FROM yarn_clean""")
print('There are', cursor.fetchone()[0], 'unique yarn weights with (Name, total yarns):')

cursor.execute("""SELECT yarn_weight_name, 
COUNT(*) AS no_total_yarns
FROM yarn_clean
GROUP BY yarn_weight_name 
ORDER BY no_total_yarns DESC
""")
print(cursor.fetchall()) #SQLite shows NULL values (None, 12) and pandas doesn't

print('PANDAS ->')
print('There are', df['yarn_weight_name'].nunique(), 'unique weights. With names and yarn counts:')
print(df['yarn_weight_name'].value_counts())

conn.commit()
conn.close()