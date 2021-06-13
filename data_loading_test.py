import unittest
import datetime
import pandas as pd
from helpers.data_load import weather_model, bikes_model, load_bikes_day_counts, load_combine


class TestDayTraffic(unittest.TestCase):

    def test_weather_correct(self):
        # arrange
        d = {
            'time': ['2020-01-01', '2021-01-01'],
            'summary': ['test', 'test'],
            'icon': ['sunny', 'cloudy'],
            'precipType': ['sunny', 'cloudy'],
            'test': ['test', 'test'],
            'temperatureMin': [20, 25],
            'temperatureMax': [30, 35],
            'humidity': ['20%', '30%'],
            'windSpeed': [30, 40],
            'cloudCover': ['0%', '10%'],
            'visibility': [10, 9],
            'test2': ['test2', 'test2']
        }

        # act
        df = pd.DataFrame(data=d)
        df = weather_model(df)

        # assert
        self.assertEqual(df.index.name, 'time', 'Index is time')
        self.assertEqual(df.size, 2*9, 'size is 2 rows * 9 cols')

    def test_weather_incorrect_date_type(self):
        # arrange
        d = {
            'time': ['2020-01-01', 20],
            'summary': ['test', 'test'],
            'icon': ['sunny', 'cloudy'],
            'precipType': ['sunny', 'cloudy'],
            'test': ['test', 'test'],
            'temperatureMin': [20, 25],
            'temperatureMax': [30, 35],
            'humidity': ['20%', '30%'],
            'windSpeed': [30, 40],
            'cloudCover': ['0%', '10%'],
            'visibility': [10, 9],
            'test2': ['test2', 'test2']
        }

        # act
        df = pd.DataFrame(data=d)

        # assert
        with self.assertRaises(TypeError):
            df = weather_model(df)

    def test_weather_incorrect_date_format(self):
        # arrange
        d = {
            'time': ['2020-01-01', '20'],
            'summary': ['test', 'test'],
            'icon': ['sunny', 'cloudy'],
            'precipType': ['sunny', 'cloudy'],
            'test': ['test', 'test'],
            'temperatureMin': [20, 25],
            'temperatureMax': [30, 35],
            'humidity': ['20%', '30%'],
            'windSpeed': [30, 40],
            'cloudCover': ['0%', '10%'],
            'visibility': [10, 9],
            'test2': ['test2', 'test2']
        }

        # act
        df = pd.DataFrame(data=d)

        # assert
        with self.assertRaises(ValueError):
            df = weather_model(df)

    def test_bikes_correct(self):
        # arrange
        d = {
            'starttime': ['2020-01-02 00:00', '2020-01-03 00:00', '2020-01-04 00:00'],
            'stoptime': ['2020-01-02 01:00', '2020-01-03 01:00', '2020-01-04 00:50'],
            'tripduration': [60, 60, 50],
            'bikeid': [1, 2, 3],
            'usertype': ["subscriber", "subscriber", "subscriber"],
            'birth year': [1985, 2000, 1945],
            'gender': [1, 2, 2]
        }

        # act
        df = pd.DataFrame(data=d)
        df = bikes_model(df)

        # assert
        self.assertEqual(df.size, 8*3, 'size is 3 rows * 7 cols')
        self.assertListEqual(df['age'].to_list(), [35, 20, 75], 'ages are 35, 20, 75')

    def test_bikes_incorrect_date_format(self):
        # arrange
        d = {
            'starttime': ['2020-01-0', '2020-01-03 00:00', '2020-01-04 00:00'],
            'stoptime': ['2020-01-02 01:00', '2020-01-03 01:00', '2020-01-04 00:50'],
            'tripduration': [60, 60, 50],
            'bikeid': [1, 2, 3],
            'usertype': ["subscriber", "subscriber", "subscriber"],
            'birth year': [1985, 2000, 1945],
            'gender': [1, 2, 2]
        }

        # act
        df = pd.DataFrame(data=d)

        # assert
        with self.assertRaises(ValueError):
            df = bikes_model(df)

    def test_bikes_day_counts_correct(self):
        # arrange
        d = {
            'starttime': ['2020-01-02 00:00', '2020-01-03 00:00', '2020-01-04 00:00'],
            'stoptime': ['2020-01-02 01:00', '2020-01-03 01:00', '2020-01-04 00:50'],
            'tripduration': [60, 60, 50],
            'bikeid': [1, 2, 3],
            'usertype': ["subscriber", "subscriber", "subscriber"],
            'birth year': [1985, 2000, 1945],
            'gender': [1, 2, 2]
        }

        # act
        df_bikes = pd.DataFrame(data=d)
        df_bikes = bikes_model(df_bikes)
        df = load_bikes_day_counts(df_bikes)

        # assert
        self.assertEqual(df.size, 3, '3 redis - one per day')
        self.assertEqual(df.index.tolist()[0], datetime.date(2020, 1, 2), 'first date is 2020-01-02')

    def test_combine(self):
        # arrange
        d_bikes = {
            'starttime': ['2020-01-02 00:00', '2020-01-03 00:00', '2020-01-04 00:00'],
            'stoptime': ['2020-01-02 01:00', '2020-01-03 01:00', '2020-01-04 00:50'],
            'tripduration': [60, 60, 50],
            'bikeid': [1, 2, 3],
            'usertype': ["subscriber", "subscriber", "subscriber"],
            'birth year': [1985, 2000, 1945],
            'gender': [1, 2, 2]
        }

        d_weather = {
            'time': ['2020-01-02', '2020-01-03', '2020-01-04'],
            'summary': ['test', 'test', 'test'],
            'icon': ['sunny', 'cloudy', 'cloudy'],
            'precipType': ['sunny', 'cloudy', 'cloudy'],
            'test': ['test', 'test', 'test'],
            'temperatureMin': [20, 25, 35],
            'temperatureMax': [30, 35, 40],
            'humidity': ['20%', '30%', '40%'],
            'windSpeed': [30, 40, 10],
            'cloudCover': ['0%', '10%', '8%'],
            'visibility': [10, 9, 10],
            'test2': ['test2', 'test2', 'test2']
        }

        # act
        df_bikes = pd.DataFrame(data=d_bikes)
        df_bikes = bikes_model(df_bikes)
        df_day_counts = load_bikes_day_counts(df_bikes)
        df_weather = pd.DataFrame(data=d_weather)
        df_weather = weather_model(df_weather)
        df = load_combine(df_day_counts, df_weather)

        # assert
        self.assertEqual(df.index.name, 'time', 'Index is time')
        self.assertEqual(df.size, 3*10, 'size is 3 rows * 10 cols')


if __name__ == '__main__':
    pd.set_option('mode.chained_assignment', None)
    unittest.main()
