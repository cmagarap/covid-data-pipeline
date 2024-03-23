import csv
import logging
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
    # exec_date = '03-22-2021'
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
        
        # Define data types and column mapping
        data_types = {
            'FIPS': pd.UInt32Dtype(),
            'Admin2': str,
            'Province_State': str,
            'Country_Region': str,
            'Lat': float,
            'Long_': float,
            'Confirmed': pd.Int64Dtype(),
            'Deaths': pd.Int64Dtype(),
            'Recovered': pd.Int64Dtype(),
            'Active': pd.Int64Dtype(),
            'Combined_Key': str,
            'Incident_Rate': 'float64',
            'Case_Fatality_Ratio': 'float64'
        }
        
        # Read the CSV content from the response text 
        df = pd.read_csv(StringIO(response.text), sep=',',
            dtype=data_types, parse_dates=parse_dates,
            na_values=[''], keep_default_na=False)

        # # Rename columns using COLUMN_MAPPING
        # df.rename(columns=COLUMN_MAPPING, inplace=True)

        # # Check for missing columns and add them with None values
        # missing_columns = {col: None for col in MISSING_COLUMNS if col not in df.columns}
        # df = df.assign(**missing_columns)

        return df


@test
def test_output(*args) -> None:
    """
    Template code for testing the output of the block.
    """
    if args:
        output = args[0]
        assert output is not None, 'The output is undefined'
