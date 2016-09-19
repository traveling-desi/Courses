import sqlite3
 
conn = sqlite3.connect("mydatabase.db") # or use :memory: to put it in RAM
 
cursor = conn.cursor()
 
# create a table
cursor.execute("DROP TABLE IF EXISTS asia")
cursor.execute("""CREATE TABLE asia 
                  (asia text, prob real)
               """)

cursor.execute("INSERT INTO asia VALUES ('Y', 0.01)")
cursor.execute("INSERT INTO asia VALUES ('N', 0.99)")

cursor.execute("DROP TABLE IF EXISTS tub_asia")
cursor.execute("""CREATE TABLE tub_asia 
                  (tub text, asia text, prob real)
               """)

cursor.execute("INSERT INTO tub_asia VALUES ('Y', 'Y', 0.05)")
cursor.execute("INSERT INTO tub_asia VALUES ('N', 'Y', 0.95)")
cursor.execute("INSERT INTO tub_asia VALUES ('Y', 'N', 0.01)")
cursor.execute("INSERT INTO tub_asia VALUES ('N', 'N', 0.99)")

cursor.execute("DROP TABLE IF EXISTS smoking")
cursor.execute("""CREATE TABLE smoking
                  (smoking text, prob real)
               """)

cursor.execute("INSERT INTO smoking VALUES ('Y', 0.50)")
cursor.execute("INSERT INTO smoking VALUES ('N', 0.50)")

cursor.execute("DROP TABLE IF EXISTS lung_smoking")
cursor.execute("""CREATE TABLE lung_smoking
                  (lung text, smoking text, prob real)
               """)

cursor.execute("INSERT INTO lung_smoking VALUES ('Y', 'Y', 0.1)")
cursor.execute("INSERT INTO lung_smoking VALUES ('N', 'Y', 0.9)")
cursor.execute("INSERT INTO lung_smoking VALUES ('Y', 'N', 0.01)")
cursor.execute("INSERT INTO lung_smoking VALUES ('N', 'N', 0.99)")


cursor.execute("DROP TABLE IF EXISTS bronc_smoking")
cursor.execute("""CREATE TABLE bronc_smoking
                  (bronc text, smoking text, prob real)
               """)

cursor.execute("INSERT INTO bronc_smoking VALUES ('Y', 'Y', 0.6)")
cursor.execute("INSERT INTO bronc_smoking VALUES ('N', 'Y', 0.4)")
cursor.execute("INSERT INTO bronc_smoking VALUES ('Y', 'N', 0.3)")
cursor.execute("INSERT INTO bronc_smoking VALUES ('N', 'N', 0.7)")


cursor.execute("DROP TABLE IF EXISTS either_lung_tub")
cursor.execute("""CREATE TABLE either_lung_tub
                  (either text, lung text, tub, prob real)
               """)

cursor.execute("INSERT INTO either_lung_tub VALUES ('Y', 'Y', 'Y', 1)")
cursor.execute("INSERT INTO either_lung_tub VALUES ('N', 'Y', 'Y', 0)")
cursor.execute("INSERT INTO either_lung_tub VALUES ('Y', 'Y', 'N', 1)")
cursor.execute("INSERT INTO either_lung_tub VALUES ('N', 'Y', 'N', 0)")
cursor.execute("INSERT INTO either_lung_tub VALUES ('Y', 'N', 'Y', 1)")
cursor.execute("INSERT INTO either_lung_tub VALUES ('N', 'N', 'Y', 0)")
cursor.execute("INSERT INTO either_lung_tub VALUES ('Y', 'N', 'N', 0)")
cursor.execute("INSERT INTO either_lung_tub VALUES ('N', 'N', 'N', 1)")


cursor.execute("DROP TABLE IF EXISTS xray_either")
cursor.execute("""CREATE TABLE xray_either
                  (xray text, either text, prob real)
               """)

cursor.execute("INSERT INTO xray_either VALUES ('Y', 'Y', 0.98)")
cursor.execute("INSERT INTO xray_either VALUES ('N', 'Y', 0.02)")
cursor.execute("INSERT INTO xray_either VALUES ('Y', 'N', 0.05)")
cursor.execute("INSERT INTO xray_either VALUES ('N', 'N', 0.95)")

cursor.execute("DROP TABLE IF EXISTS dysp_either_bronc")
cursor.execute("""CREATE TABLE dysp_either_bronc
                  (dysp text, either text, bronc text, prob real)
               """)

cursor.execute("INSERT INTO dysp_either_bronc VALUES ('Y', 'Y', 'Y', 0.90)")
cursor.execute("INSERT INTO dysp_either_bronc VALUES ('N', 'Y', 'Y', 0.10)")
cursor.execute("INSERT INTO dysp_either_bronc VALUES ('Y', 'Y', 'N', 0.70)")
cursor.execute("INSERT INTO dysp_either_bronc VALUES ('N', 'Y', 'N', 0.30)")
cursor.execute("INSERT INTO dysp_either_bronc VALUES ('Y', 'N', 'Y', 0.80)")
cursor.execute("INSERT INTO dysp_either_bronc VALUES ('N', 'N', 'Y', 0.20)")
cursor.execute("INSERT INTO dysp_either_bronc VALUES ('Y', 'N', 'N', 0.10)")
cursor.execute("INSERT INTO dysp_either_bronc VALUES ('N', 'N', 'N', 0.90)")



conn.commit()

## Nothing particularly useful
cursor.execute("SELECT tub_asia.tub, SUM(prob) FROM tub_asia GROUP BY tub_asia.tub")
print cursor.fetchall()

## Joint Probability of Tub and Asia
cursor.execute("SELECT tub_asia.tub, tub_asia.asia, SUM(tub_asia.prob*asia.prob) FROM tub_asia, asia WHERE tub_asia.asia=asia.asia GROUP BY tub_asia.tub, tub_asia.asia")
print cursor.fetchall()

## A-posterior probability of asia given evidence of tub='Y'
cursor.execute("SELECT tub_asia.asia, SUM(tub_asia.prob*asia.prob) FROM tub_asia, asia WHERE tub_asia.tub = 'Y' AND tub_asia.asia=asia.asia GROUP BY asia.asia")
print cursor.fetchall()
