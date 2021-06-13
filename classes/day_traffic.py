from pandas.core.frame import DataFrame
from helpers.data_load import load_weather, load_bikes, load_bikes_day_counts, load_combine


class DayTraffic:
    def __init__(self) -> None:
        self.load_data()

    def load_data(self) -> None:
        self.__df_weather = load_weather()
        self.__df_bikes = load_bikes()
        self.__df_bike_day_counts = load_bikes_day_counts(self.df_bikes)
        self.__df_combine = load_combine(self.df_bike_day_counts, self.df_weather)

    @property
    def df_weather(self) -> DataFrame:
        return self.__df_weather

    @property
    def df_bikes(self) -> DataFrame:
        return self.__df_bikes

    @property
    def df_bike_day_counts(self) -> DataFrame:
        return self.__df_bike_day_counts

    @property
    def df_combine(self) -> DataFrame:
        return self.__df_combine
