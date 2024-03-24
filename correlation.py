import pandas as pd
import psycopg2
import logging
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO)

# Database connection parameters
dbname = 'JHU'
user = 'root'
password = 'root123'
host = 'localhost'  # or '127.0.0.1' if it's the same machine
port = '5432'  # Default PostgreSQL port

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    logging.info('Connected to the database.')
except psycopg2.Error as e:
    logging.error('Unable to connect to the database:', e)
    exit(1)

query = f"""SELECT *
        FROM covid.daily_reports;"""

# Execute the SQL query and fetch all rows
try:
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    # Fetch column names from the cursor description
    col_names = [desc[0] for desc in cursor.description]

    cursor.close()
    logging.info("Query executed successfully.")

except psycopg2.Error as e:
    logging.error("Error executing the query:", e)
    conn.close()
    exit(1)

conn.close()
logging.info("Connection to the database closed.")

# Convert the fetched rows into a pandas DataFrame
df = pd.DataFrame(rows, columns=col_names)

incident_rate = 'incident_rate'
case_fatality_ratio = 'case_fatality_ratio'
recovered = 'recovered'
confirmed = 'confirmed'
active = 'active'
deaths = 'deaths'

column1 = confirmed
column2 = deaths

# Generate a histogram to check for normal distribution
# df.hist(column=confirmed)
# plt.show()

# Calculate Spearman correlation coefficient
spearman_corr = df[[column1, column2]].corr(method='spearman').iloc[0, 1]
print(f"Spearman correlation coefficient between {column1} and {column2}: {spearman_corr}")
