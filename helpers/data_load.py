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

    if(df_waether.isna().values.any()):
        # partly-cloudy-day is most common and normal for March
        if(df_waether['summary'].isna().values.any()):
            df_waether['summary'].fillna('partly-cloudy-day')

        if(df_waether['temperatureMin'].isna().values.any()):
            df_waether['temperatureMin'].fillna(df_waether['temperatureMin'].mean())

        if(df_waether['temperatureMax'].isna().values.any()):
            df_waether['temperatureMax'].fillna(df_waether['temperatureMax'].mean())

        if(df_waether['humidity'].isna().values.any()):
            df_waether['humidity'].fillna(df_waether['humidity'].mean())

        if(df_waether['windSpeed'].isna().values.any()):
            df_waether['windSpeed'].fillna(df_waether['windSpeed'].mean())

        if(df_waether['cloudCover'].isna().values.any()):
            df_waether['cloudCover'].fillna(df_waether['cloudCover'].mean())

        # we can't assume fogginess
        if(df_waether['visibility'].isna().values.any()):
            df_waether['visibility'].fillna(10)

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

    if(df_bikes.isna().values.any()):
        # most common
        if(df_bikes['usertype'].isna().values.any()):
            df_bikes['usertype'].fillna('Subscriber')

        if(df_bikes['birth year'].isna().values.any()):
            df_bikes['birth year'].fillna(df_bikes['birth year'].mean())

        # more than 70% are male
        if(df_bikes['gender'].isna().values.any()):
            df_bikes['gender'].fillna(1)

    return df_bikes


def load_bikes_day_counts(df_bikes: DataFrame) -> DataFrame:
    df_bike_counts = df_bikes[['time', 'bikeid']].groupby(['time']).count()
    df_bike_counts = df_bike_counts.rename(columns={'bikeid': 'count'})

    return df_bike_counts


def load_combine(df_bike_counts: DataFrame, df_waether: DataFrame) -> DataFrame:
    df = pd.concat([df_bike_counts, df_waether], axis=1)

    return df
