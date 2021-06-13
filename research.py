# %%
# init imports
import pandas as pd
from datetime import date
from config import constants
import os
from dotenv import load_dotenv
import seaborn as sns
from matplotlib import pyplot as plt

# %%
# load data and cache it, in order to download large file just once
load_dotenv()
df_waether = pd.read_csv(constants.WEATHER_FILE_PATH)
df_bikes = pd.read_csv(constants.BIKES_FILE_PATH + os.getenv('API_KEY'))

# %%
# set DataFrame with usefull information about the weather
# set 'time' column to be index, since it is the key
df_waether = df_waether[['time', 'summary', 'icon', 'precipType', 'temperatureMin',
                        'temperatureMax', 'humidity', 'windSpeed', 'cloudCover', 'visibility']]
df_waether['time'] = df_waether['time'].apply(lambda x: date.fromisoformat(x))
df_waether = df_waether.set_index('time')
df_waether.head()

# %%
# analyse 'icon' column
# we have various conditions, most common being 'partly-cloudy-day'
# following 'rain' and 'clear-day', which is normal, since we are doing March
df_waether.icon.value_counts()

# %%
# analyse 'temperatureMax' column:
# Max: 64.96, Min: 32.16 (values in Fahrenheit)
df_waether.temperatureMax.describe()

# %%
# 'visibility, from 0 to 10, 10 being absolutely clear'
# Min is 6.435, for our data
df_waether.visibility.describe()

# %%
# set DataFrame with usefull information about the bike trips
# 'starttime' and 'stoptime' are dates
df_bikes = df_bikes[['starttime', 'stoptime', 'tripduration', 'bikeid', 'usertype', 'birth year', 'gender']]
df_bikes = df_bikes.rename(columns={'starttime': 'time'})
df_bikes['time'] = df_bikes['time'].apply(lambda x: date.fromisoformat(x[:10]))
df_bikes['stoptime'] = df_bikes['stoptime'].apply(lambda x: date.fromisoformat(x[:10]))
df_bikes['age'] = df_bikes['birth year'].apply(lambda x: 2020 - x)
df_bikes.head()

# %%
# we have about 90% subscribers
df_bikes.usertype.value_counts()

# %%
# visualize ages for subscribers
df_bikes.age.hist(range=(15, 100))

# %%
# about 70% of subscribers are male (1: male, 2: female, 0: unknown)
df_bikes.gender.value_counts()

# %%
# tracks the most used bikes
df_bikes.bikeid.value_counts().head()

# %%
# new table that calculates how many trips are made for each day
df_bike_counts = df_bikes[['time', 'bikeid']].groupby(['time']).count()
df_bike_counts = df_bike_counts.rename(columns={'bikeid': 'count'})
df_bike_counts.head()

# %%
# new table for how many trips are made on which weather conditions
df = pd.concat([df_bike_counts, df_waether], axis=1)
df.head(5)

# %%
df.isna()
# %%
df['count'].isna().values.any()

# %%
sns.heatmap(df.corr())
# %%
plt.scatter(df.index, df["count"])
