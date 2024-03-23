import logging
import psycopg2
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.postgres import Postgres
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_postgres(df: DataFrame, **kwargs) -> None:
    """
    Template for exporting data to a PostgreSQL database.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#postgresql
    """

    if len(df) > 0:
        schema_name = 'covid'  # Specify the name of the schema to export data to
        table_name = 'daily_reports'  # Specify the name of the table to export data to
        config_path = path.join(get_repo_path(), 'io_config.yaml')
        config_profile = 'dev'

        # Define column data types
        column_data_types = {
            'FIPS': 'bigint',
            'Admin2': 'varchar(100)',
            'Province_State': 'varchar(100)',
            'Country_Region': 'varchar(100)',
            'Lat': 'float8',
            'Long_': 'float8',
            'Confirmed': 'bigint',
            'Deaths': 'bigint',
            'Recovered': 'bigint',
            'Active': 'bigint',
            'Combined_Key': 'varchar(100)',
            'Incident_Rate': 'float8',
            'Case_Fatality_Ratio': 'float8'
        }

        try:
            with Postgres.with_config(ConfigFileLoader(config_path, config_profile)) as loader:
                loader.export(
                    df,
                    schema_name,
                    table_name,
                    index=False,  # Specifies whether to include index in exported table
                    if_exists='append' # Specify resolution policy if table name already exists
                )
        except psycopg2.Error as dce:
            logging.error(f'Database connection failed: {dce}')
        except (psycopg2.IntegrityError, psycopg2.DataError) as de:
            logging.error(f'Data export failed: {dce}')
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
    
    else:
        logging.info('No data was passed from the data transformer')
        print('No data was passed from the data loader.')
