import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from classes.day_traffic import DayTraffic
import pandas as pd
from helpers.research import research_bikes

global_from_time = datetime.now()

load_dotenv()
pd.set_option('mode.chained_assignment', None)
if not os.path.isdir('log'):
    os.mkdir('log')
datetime_now_str = datetime.utcnow().strftime('%Y%m%d')
logging.basicConfig(filename=f'log/main_{datetime_now_str}.log',
                    filemode='a', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

data = DayTraffic()
df = pd.DataFrame(data.df_combine)
research_bikes(df)

global_time_delta = datetime.now() - global_from_time
logging.info(f'Total time: {global_time_delta}')
