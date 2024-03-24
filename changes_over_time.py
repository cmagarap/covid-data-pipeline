import os
import pandas as pd
import plotly.express as px
import psycopg2
import logging

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

# Choose the metric of interest (e.g., confirmed, deaths, recovered,
# active, incident_rate, case_fatality_ratio)
metric = 'confirmed'

# Choose area from 'admin2' (e.g. Los Angeles, Dallas, Queens)
admin2 = 'Los Angeles'

# Choose state (e.g. California, Texas, New York)
province_state = 'California'

# Choose country (e.g. US, China, Russia)
country_region = 'US'

query = f"""SELECT {metric}, last_update 
        FROM covid.daily_reports dr 
        WHERE admin2 = '{admin2}'
           AND province_state = '{province_state}'
           AND country_region = '{country_region}'
        ORDER BY last_update ASC;
        """

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

# Close the database connection
conn.close()
logging.info("Connection to the database closed.")

# Convert the fetched rows into a pandas DataFrame
df = pd.DataFrame(rows, columns=col_names)

# Aggregate data by date and calculate the daily metric
df.set_index('last_update', inplace=True)

# Line Chart
fig = px.line(df, title=f'Cumulative Daily {metric.capitalize()} COVID-19 cases '
                        f'in {admin2}, {province_state} {country_region}')
# Update x-axis label
fig.update_xaxes(title_text='Date')

# Update y-axis label
fig.update_yaxes(title_text='Number of confirmed cases')
fig.show()
logging.info('Figure generated!')

if not os.path.exists('figures'):
    os.mkdir('figures')

logging.info('Saving Data Figure as HTML file...')
# Save the Figure into an HTML File
fig.write_html(f'figures/covid19-{metric.upper()}-{admin2}_{province_state}_{country_region}.html')
logging.info('Figure saved!')
