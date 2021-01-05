import streamlit as st

import pytz
import time
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from binance.client import Client
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from bokeh.io import output_file, show
from bokeh.layouts import column
from bokeh.layouts import layout
from bokeh.plotting import figure
from bokeh.models import Toggle, BoxAnnotation
from bokeh.models import Panel, Tabs
from bokeh.palettes import Set3
from datetime import datetime
from stockstats import StockDataFrame as Sdf






st.title('Coin Trader')

def color(x):
    if x < 30:
        color = 'red'
    else:
        color = 'white'
    return 'background-color: %s' % color


class Controller:


    def __init__(self):
        historic_data = None
        stockstats_df = None

    # Find history for one coin
    def find_history(self, coin):
        try:
            klines = client.get_historical_klines(coin, Client.KLINE_INTERVAL_1DAY, "60 day ago UTC")
            klines = np.array(klines)
        except Exception as e:
            st.text(e)
            print(e)


        df = pd.DataFrame(data=klines, columns=["Open time", "Open", "High", "Low", "Close", "Volume",
        "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume"
        , "Taker buy quote asset volume", "Ignore"])

        return df

    def find_history_all(self, coin_list):
        total_df = pd.DataFrame(columns=["Coin", "Open time", "Open", "High", "Low", "Close", "Volume",
        "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume"
        , "Taker buy quote asset volume", "Ignore"])
        
        for coin in coin_list:
            try:
                df = self.find_history(coin)
                df['Coin'] = coin
                total_df = total_df.append(df)
                if len(df) == 0:
                    continue
            except Exception as e:
                continue

        return total_df    

    def calculate_metrics(self, metric):
        metric = self.stockstats_df[metric]
        return metric

    def prepare_data(self):
        data = self.historic_data[['Open', 'High', 'Low', 'Close', 'Volume', 'Quote asset volume']]
        data.index = self.historic_data['Open time']
        for col in data.columns:
            data[col] = data[col].astype(float)
        self.historic_data = data

    def preprare_Sdf_data(self):
        stockstats_df = Sdf.retype(self.historic_data)
        self.stockstats_df = stockstats_df
        
if __name__ == "__main__":

    controller = Controller()
# Enter your api key and secret key here
    client = Client("","")
    coin_list = ["TRXBNB","ETHBTC","TRXBTC","IOSTBTC","VENBTC","XRPBTC","LTCBTC"]
    
    selected_coin = st.sidebar.selectbox(
        "Choose a coin",
        ("TRXBNB","ETHBTC","TRXBTC","IOSTBTC","BCHBTC","XRPBTC","LTCBTC" )
    )
    selected_metrics = st.sidebar.multiselect(
        'Choose metrics to observe',
        ["TRXBNB","ETHBTC","TRXBTC","IOSTBTC","BCHBTC","XRPBTC","LTCBTC"])








    
    # stats_df.index = 
    # stats_df['RSI_14'] = metric_list_dict.values()
    # history_data = controller.find_history("TRXBNB")
    # data = history_data[['Open', 'High', 'Low', 'Close', 'Volume', 'Quote asset volume']]
    # data.index = history_data['Open time']
    # for col in data.columns:
    #     data[col] = data[col].astype(float)

    # stockstats_df = Sdf.retype(data)
    # stockstats_df['rsi_14']

    
    # s1 = figure(plot_width=800, plot_height=400,  x_axis_type='datetime', background_fill_color="#fafafa")
    # s1.left[0].formatter.use_scientific = False
    # #s1.below[0].formatter.use_scientific = False


    # s1.line(controller.history_data['Open time converted'], controller.history_data['Close'],  color="Black", alpha=1, legend_label = selected_coin)

    # st.bokeh_chart(s1)

    # multi_data = controller.find_history_all(selected_metrics)
    is_button_pressed = st.sidebar.button('Show stats for various coins')
    if(is_button_pressed):
        metric_list_dict = {}
        stats_df = pd.DataFrame(columns = ['rsi_14'])
        for index, coin in enumerate(selected_metrics):
            controller.historic_data = controller.find_history(coin)
            controller.historic_data['Open time converted'] = controller.historic_data.index.astype("int64")/1000
            controller.historic_data['Open time converted'] = controller.historic_data['Open time converted'].apply(lambda x: datetime.fromtimestamp(x))

            controller.prepare_data()
            controller.preprare_Sdf_data()
            metric = controller.calculate_metrics('rsi_14')
            metric_list_dict[coin] = metric.iloc[-1:][0]
            stats_df = stats_df.append({'rsi_14' : metric.iloc[-1:][0] }, ignore_index=True)
        stats_df.index = selected_metrics
        st.dataframe(stats_df.style.applymap(color))
        
