import logging
from datetime import datetime, timedelta

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

logging.basicConfig(level=logging.INFO)

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

@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    if len(data) > 0:
        # last_update = kwargs.get('execution_date')
        # last_update = datetime.strptime('2020-01-22', '%Y-%m-%d')
        # last_update += timedelta(days=1)
        # last_update_str = last_update.strftime('%Y-%m-%d')
        # print(last_update_str)

        # Rename columns using COLUMN_MAPPING
        data = data.rename(columns=COLUMN_MAPPING)

        # Check for missing columns and add them with None values
        missing_columns = {col: None for col in MISSING_COLUMNS if col not in data.columns}
        data = data.assign(**missing_columns)

        # Remove duplicate rows
        data = data.drop_duplicates()

        # data['Last_Update'] = data['Last_Update'].astype(str)
        # Only get the last_update for the [current date]
        # data = data[data['Last_Update'].str.split(' ').str[0] == last_update_str]

        logging.info('Data successfully transformed.')

        return data
    
    else:
        logging.info('No data was passed from the data loader.')
        print('No data was passed from the data loader.')
        return None


@test
def test_output(*args) -> None:
    """
    Template code for testing the output of the block.
    """

    if args:
        output = args[0]
        assert output is not None, 'The output is undefined'
