import logging
from pandas.core.frame import DataFrame
from config import constants
from datetime import date
import pandas as pd
import os


def load_weather() -> DataFrame:
    try:
        df_waether = pd.read_csv(constants.WEATHER_FILE_PATH)
        df_waether = weather_model(df_waether)
    except Exception as ex:
        logging.exception(ex)

    return df_waether


def weather_model(init_mode: DataFrame) -> DataFrame:
    df_waether = init_mode[['time', 'summary', 'icon', 'precipType', 'temperatureMin',
                            'temperatureMax', 'humidity', 'windSpeed', 'cloudCover', 'visibility']]
    df_waether['time'] = df_waether['time'].apply(date.fromisoformat)
    df_waether = df_waether.set_index('time')

    return df_waether


def load_bikes() -> DataFrame:
    try:
        df_bikes = pd.read_csv(constants.BIKES_FILE_PATH + os.getenv('API_KEY'))
        df_bikes = bikes_model(df_bikes)
    except Exception as ex:
        logging.exception(ex)

    return df_bikes


def bikes_model(init_mode: DataFrame) -> DataFrame:
    df_bikes = init_mode[['starttime', 'stoptime', 'tripduration', 'bikeid', 'usertype', 'birth year', 'gender']]
    # the column 'starttime' is renamed to 'time' for consistency with df_waether
    # in order to join them later
    df_bikes = df_bikes.rename(columns={'starttime': 'time'})
    df_bikes['time'] = df_bikes['time'].apply(lambda x: date.fromisoformat(x[:10]))
    df_bikes['stoptime'] = df_bikes['stoptime'].apply(lambda x: date.fromisoformat(x[:10]))
    df_bikes['age'] = df_bikes['birth year'].apply(lambda x: 2020 - x)

    return df_bikes


def load_bikes_day_counts(df_bikes: DataFrame) -> DataFrame:
    df_bike_counts = df_bikes[['time', 'bikeid']].groupby(['time']).count()
    df_bike_counts = df_bike_counts.rename(columns={'bikeid': 'count'})

    return df_bike_counts


def load_combine(df_bike_counts: DataFrame, df_waether: DataFrame) -> DataFrame:
    df = pd.concat([df_bike_counts, df_waether], axis=1)

    return df
