import io
import logging
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

logging.basicConfig(level=logging.INFO)


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    # exec_date = kwargs.get('execution_date').strftime('%m-%d-%Y')
    exec_date = '06-07-2020'
    print(exec_date)
    url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{exec_date}.csv'
    response = requests.get(url)

    if response.status_code == 404:
        logging.info('The requested resource was not found (404).')
        print('The requested resource was not found (404).')

        return None
    else:
        logging.info('Data extraction successful.')

        data_types = {
            'FIPS': pd.Int64Dtype(),
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

        parse_dates = ['Last_Update']
        
        df = pd.read_csv(io.StringIO(response.text), sep=',',
        dtype=data_types, parse_dates=parse_dates,
        na_values=[''], keep_default_na=False)

        if 'Incidence_Rate' in df.columns:
            df.rename(columns={'Incidence_Rate': 'Incident_Rate'}, inplace=True)

        return df


@test
def test_output(*args) -> None:
    """
    Template code for testing the output of the block.
    """
    if args:
        output = args[0]
        assert output is not None, 'The output is undefined'

