import csv
import logging
import numpy as np
import pandas as pd
import requests
from io import StringIO
from sqlalchemy import Column, Integer, String, Float

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


logging.basicConfig(level=logging.INFO)
LAST_UPDATE = 'Last_Update'

FIPS = 'FIPS'
ADMIN2 = 'Admin2'
PROVINCE_STATE = 'Province_State'
COUNTRY_REGION = 'Country_Region'
LAT = 'Lat'
LONG_ = 'Long_'
CONFIRMED = 'Confirmed'
DEATHS = 'Deaths'
RECOVERED = 'Recovered'
ACTIVE = 'Active'
COMBINED_KEY = 'Combined_Key'
INCIDENT_RATE = 'Incident_Rate'
CASE_FATALITY_RATIO = 'Case_Fatality_Ratio'
LAST_UPDATE = 'Last_Update'
# These are the columns not included in the earlier batch of data:
MISSING_COLUMNS = [FIPS, ADMIN2, LAT, LONG_, ACTIVE, COMBINED_KEY, INCIDENT_RATE, CASE_FATALITY_RATIO]
COLUMN_MAPPING = {
    'Province/State': PROVINCE_STATE,
    'Country/Region': COUNTRY_REGION,
    'Last Update': LAST_UPDATE,
    'Latitude': LAT,
    'Longitude': LONG_,
    'Confirmed': CONFIRMED,
    'Deaths': DEATHS,
    'Recovered': RECOVERED,
    'Incidence_Rate': INCIDENT_RATE,
    'Case-Fatality_Ratio': CASE_FATALITY_RATIO
}


def read_csv_headers(csv_content):
    """
    Reads headers from a CSV content.

    Args:
    - csv_content (str): CSV content as a string.

    Returns:
    - headers (list): List of header names.
    """
    csv_file = StringIO(csv_content)
    csv_reader = csv.reader(csv_file)
    return next(csv_reader)


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Loads data from an API endpoint.

    This function constructs a URL based on the provided execution date (exec_date) and fetches
    data from the corresponding CSV file. The CSV content is then parsed into a DataFrame.

    Args:
    - execution_date (str): The execution date in the format 'MM-DD-YYYY'.

    Returns:
    - df (DataFrame or None): The DataFrame containing the loaded data if successful,
      otherwise returns None.

    Raises:
    - None.
    """
    exec_date = kwargs.get('execution_date').strftime('%m-%d-%Y')
    # exec_date = '01-26-2020'
    # exec_date = '03-24-2020'
    # exec_date = '08-22-2022'
    print('execution_date -->', exec_date)
    url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{exec_date}.csv'
    response = requests.get(url)

    if response.status_code == 404:
        logging.info('The requested resource was not found (404).')
        print('The requested resource was not found (404).')

        return None
    else:
        logging.info('Data extraction successful.')

        # Read CSV headers and determine parse dates
        csv_headers = read_csv_headers(response.text)
        parse_dates = [LAST_UPDATE] if LAST_UPDATE in csv_headers else ['Last Update']

        # Read the CSV content from the response text 
        df = pd.read_csv(StringIO(response.text), sep=',',
            parse_dates=parse_dates,
            na_values=[''])

        # Rename columns using COLUMN_MAPPING
        df = df.rename(columns=COLUMN_MAPPING)
        
        # missing_columns = {col: np.nan for col in MISSING_COLUMNS if col not in df.columns}

        # Check for missing columns and add them with '' or NaN values
        missing_columns = {}
        for col in MISSING_COLUMNS:
            if col not in df.columns:
                if col == ADMIN2 or col == COMBINED_KEY:
                    missing_columns[col] = ''
                else:    
                    missing_columns[col] = np.nan
        print(missing_columns)

        df = df.assign(**missing_columns)

        data_types = {
            'FIPS': 'float64',
            'Admin2': str,
            'Province_State': str,
            'Country_Region': str,
            'Lat': 'float64',
            'Long_': 'float64',
            'Confirmed': 'float64',
            'Deaths': 'float64',
            'Recovered': 'float64',
            'Active': 'float64',
            'Combined_Key': str,
            'Incident_Rate': 'float64',
            'Case_Fatality_Ratio': 'float64'
        }

        df['Admin2'] = df['Admin2'].replace(np.nan, '')
        df['Province_State'] = df['Province_State'].replace(np.nan, '')
        df['Country_Region'] = df['Country_Region'].replace(np.nan, '')
        df['Combined_Key'] = df['Combined_Key'].replace(np.nan, '')
        
        # Convert column data types
        df = df.astype(data_types, errors='ignore')

        # Remove duplicate rows
        df = df.drop_duplicates()

        # print(df.dtypes)
        
        return df


@test
def test_output(*args) -> None:
    """
    Template code for testing the output of the block.
    """
    if args:
        output = args[0]
        assert output is not None, 'The output is undefined'
