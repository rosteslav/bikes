import logging
import pydotplus
from pandas.core.frame import DataFrame
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import export_graphviz
from sklearn.metrics import accuracy_score


def research_bikes(df: DataFrame) -> None:
    """Get data frame with only numerical data in order to run DecisionTreeClassifier
    Gets to data fremes:
    - for high usage (> 50k trips)
    - for low usage (< 30k trips)
    Runs two algorithms


    Parameters
    ----------
    df : DataFrame
        Data for trips and weather
    """

    df_research = df
    df_research = df_research.drop(columns='summary')
    df_research = df_research.drop(columns='precipType')
    df_research["icon"] = df_research["icon"].map(
        {'clear-day': 1,
         'partly-cloudy-day': 2,
         'wind': 3,
         'rain': 4,
         'snow': 5
         })

    df['high_usage'] = df['count'].apply(lambda x: True if x >= 50000 else False)
    df['low_usage'] = df['count'].apply(lambda x: True if x < 30000 else False)

    df_research_high = df_research
    df_research_high['high_usage'] = df_research_high['count'].apply(lambda x: True if x >= 50000 else False)
    df_research_high = df_research_high.drop(columns='count')
    get_dt_classifier(df_research_high, 'high_usage')

    df_research_low = df_research
    df_research_low['low_usage'] = df_research_low['count'].apply(lambda x: True if x < 30000 else False)
    df_research_low = df_research_low.drop(columns='count')
    get_dt_classifier(df_research_low, 'low_usage')


def get_dt_classifier(df: DataFrame, result_column: str) -> None:
    TEST_SIZE = 0.2
    X = df[['icon', 'temperatureMin', 'temperatureMax', 'humidity',
            'windSpeed', 'cloudCover', 'visibility']]
    y = df[result_column]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE)
    dt = DecisionTreeClassifier()
    dt.fit(X_train, y_train)
    y_pred = dt.predict(X_test)
    tree_graph_to_png(dt=dt, feature_names=X_train.columns,
                      png_file_to_save=f'dt_result_{result_column}.png')
    score = accuracy_score(y_pred, y_test)
    print(score)
    logging.info(score)


def tree_graph_to_png(dt: DecisionTreeClassifier, feature_names: any, png_file_to_save: str) -> None:
    """Generates an image and saves it

    Parameters
    ----------
    dt : DecisionTreeClassifier
        DecisionTreeClassifier to draw
    feature_names : any
        Name of the features to draw
    png_file_to_save : str
        Name of the picture to save
    """

    tree_str = export_graphviz(dt, feature_names=feature_names,
                               filled=True, out_file=None)
    graph = pydotplus.graph_from_dot_data(tree_str)
    graph.write_png(png_file_to_save)
