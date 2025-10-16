'''_summary_
Deals with the SIMCOSTA's API.
See get_data function for an overview of this file.
'''

import requests
from datetime import datetime
import pandas as pd


def create_request(data_id):
    '''_summary_
    Creates the request for the Simcosta's API

    Args:
        data_id (_str_): String containing the data ID of the buoy.

    Returns:
        _str_: url that will be used on the API request
    '''
    now = datetime.now().replace(minute=0, second=0, microsecond=0)
    now = int(now.timestamp()) + 3 * 60 * 60
    ini = 0
    # ini = now -5184000

    url = f'https://simcosta.furg.br/api/intrans_data?boiaID={data_id}&type=json&time1={ini}&time2={now}&params=water_l1'
    # print(f'ini: {datetime.fromtimestamp(ini)}')
    # print(f'fim: {datetime.fromtimestamp(now)}')

    return url


def resample_data(data):
    '''_summary_
    Proccesses the JSON data obtained by the API and returns it into a pandas DataFrame


    Args:
        data (_list_): JSON obtained via the SIMCOSTA's API

    Returns:
        _pandas.DataFrame_: DataFrame with the JSON data with only 1 column and hourly outputs
    '''
    df = pd.DataFrame(data)
    df.index = pd.to_datetime(df['timestamp'])
    df = df.drop(['timestamp', 'YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'SECOND'], axis=1)

    df = df.resample('H').median()
    df = df.rename(columns={'water_l1':'ssh'})
    # precisa ainda reamostrar horario aqui
    return df


def get_data(id):
    '''_summary_
    Integrates the functions in this file in order to make the data available.

    Args:
        id (_str_): ID of the buoy of interest

    Returns:
        _pandas.DataFrame_: DataFrame with the hourly ssh data DataFrame from 2 months ago until now
    '''


    URL = create_request(id)
    response = requests.get(URL)
    response.raise_for_status()

    data = resample_data(response.json())
    
    return data
