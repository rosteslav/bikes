from pandas.core.frame import DataFrame
from helpers.data_load import load_weather, load_bikes, load_bikes_day_counts, load_combine


class DayTraffic:
    """Class for loading the data, making models and keeping them

    Models for:
    - df_weather - data for the weather on the time period for the trips
    - df_bikes - data for the bikes from the bikes rental company
    - df_bike_day_counts - data that stores how many trips are made total for every day
    - df_combine - data, that combines and maps the number of trips to the weather, the date is the index
    """

    def __init__(self) -> None:
        """Initialize the class and calls load_data method"""

        self.load_data()

    def load_data(self) -> None:
        """Loads all the data, calling helper to get it"""

        self.__df_weather = load_weather()
        self.__df_bikes = load_bikes()
        self.__df_bike_day_counts = load_bikes_day_counts(self.df_bikes)
        self.__df_combine = load_combine(self.df_bike_day_counts, self.df_weather)

    @property
    def df_weather(self) -> DataFrame:
        """Getter property for weather DataFrame, does not have a setter, since it's only loaded on init"""

        return self.__df_weather

    @property
    def df_bikes(self) -> DataFrame:
        """Getter property for bikes DataFrame, does not have a setter, since it's only loaded on init"""

        return self.__df_bikes

    @property
    def df_bike_day_counts(self) -> DataFrame:
        """Getter property for bike_day_counts DataFrame, does not have a setter, since it's only loaded on init"""

        return self.__df_bike_day_counts

    @property
    def df_combine(self) -> DataFrame:
        """Getter property for combine DataFrame, does not have a setter, since it's only loaded on init"""

        return self.__df_combine
