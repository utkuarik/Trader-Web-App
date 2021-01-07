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

def color_rsi(x):
    if x < 30:
        color = 'red'
    else:
        color = 'white'
    return 'background-color: %s' % color

def color_wr(x):
    if x >= 80:
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
            st.text(coin)
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
    coin_list = ["BTCUSDT", "ETHUSDT"
    ,"BTCBUSD","ETHBUSD","ETHBTC","LTCUSDT","BUSDUSDT","DOGEUSDT","XRPUSDT","BCCUSDT","BTCEUR",
    "ADAUSDT","USDCUSDT","LINKUSDT","BNBUSDT","BTCUSDC","VENUSDT","LTCBTC","DOGEBTC","THETAUSDT","EOSUSDT","ETHUSDC","XRPBTC",
    "ETHEUR","TRXUSDT","ZILUSDT","XLMUSDT","LINKBTC","ADABTC","BNBBTC","LTCBUSD","BNBBUSD","VENBTC","THETABTC","ETCUSDT","XMRUSDT",
    "ZILBTC","ALGOUSDT","ATOMUSDT","NEBLBTC","NEOUSDT","WAVESUSDT","EOSBTC","XTZUSDT","ZECUSDT","DASHUSDT","XRPBUSD","XMRBTC",
    "BANDUSDT","OMGUSDT","XEMBTC","BTCTUSD","TUSDUSDT","HOTUSDT","FUNUSDT","XLMBTC","BTCTRY","CHZUSDT","BTCNGN","ADABUSD","BTCPAX",
    "BNBETH","XVGBTC","TRXBTC","TFUELUSDT","RENUSDT","LINKBUSD","EOSBUSD","ALGOBTC","ONTUSDT","SCBTC","BCHABCBUSD","XRPETH","WAVESBTC",
    "PAXUSDT","ATOMBTC","TOMOUSDT","NANOUSDT","XTZBTC","LTCETH","BTTUSDT","STXUSDT","QTUMUSDT","IOTAUSDT","ETHPAX","ICXUSDT","FUNBTC",
    "TFUELBTC","BATUSDT","NEOBTC","XRPEUR","ETCBTC","VENETH","DASHBTC","ETHTUSD","ZECBTC","MATICUSDT","SOLBTC","USDTTRY","ADAETH","BANDBTC",
    "ZRXUSDT","LTCUSDC","VETBUSD","IOSTUSDT","CHZBTC","OMGBTC","ADXBTC","RENBTC","BNBEUR","TRXETH","ONEUSDT","THETAETH","FTTUSDT",
    "KAVAUSDT","STXBTC","NANOBTC","ETHTRY","ARPAUSDT","LINKUSDC","LINKETH","SCETH","CVCUSDT","FTMUSDT","QTUMBTC","XMRETH","TOMOBTC"
    ,"BTCRUB","RVNUSDT","BTSUSDT","BATBTC","GRSBTC","MDABTC","ZILETH","IOSTBTC","DCRBTC","LRCBTC","MATICBTC","PPTBTC",
    "ENJUSDT","HOTETH","XRPUSDC","XVGETH","ICXBTC","BCHABCUSDC","ETCBUSD","MITHUSDT","XLMBUSD","LTCBNB","DREPUSDT","BNTUSDT","EOSETH"



    # "HBARUSDT","ZRXBTC","ANKRBTC","XLMETH","NEBLETH","SOLBUSD","CVCBTC","ONEBTC","ZENBTC","XEMETH","ANKRUSDT","TRXBUSD","ONTBTC","BUSDTRY",
    # "VENBNB","RLCUSDT","TRXXRP","TRXUSDC","XRPBNB","FTMBTC","ENJBTC","EOSUSDC","BUSDNGN","RVNBTC","ADAUSDC","LTOUSDT","BTSBTC","DREPBTC",
    # "FUNETH","OAXBTC","USDTRUB","SCBNB","SNTBTC","SYSBTC","ADABNB","BNBUSDC","POLYBTC","KNCBTC","FETUSDT","XTZBUSD","OGNUSDT","CELRUSDT",
    # "GTOUSDT","LTOBTC","LSKBTC","HBARBTC","DASHETH","BQXBTC","NXSBTC","WINUSDT","NANOBUSD","QKCBTC","WANUSDT","DOCKBTC",
    # "FTTBTC","RLCBTC","MFTUSDT","BTTTRX","FETBTC","BNTBTC","TRXBNB","WAVESBUSD","OMGETH","KAVABTC","OSTBTC","CELRBTC","ARPABTC","ASTBTC",
    # "REPBTC","ZECETH","PIVXBTC","NPXSUSDT","MANABTC","WANBTC","WABIBTC","ATOMBUSD","ENJETH","LSKUSDT","GVTBTC","HOTBNB","AGIBTC","ARDRBTC",
    # "THETABNB","PERLUSDT","OGNBNB","LOOMBTC","BTGBTC","ZILBNB","NEOETH","NEOBUSD","STORJBTC","ARKBTC","BCDBTC","STXBNB","CTSIUSDT","BLZBTC",
    # "NANOETH","DASHBUSD","WAVESETH","DLTBTC","DNTBTC","DOCKUSDT","ONGBTC","AIONUSDT","LTCTUSD","HOTBTC","OGNBTC","KEYUSDT","LRCETH","AIONBTC",
    # "EOSBNB","WINTRX","ICXETH","DATABTC","SNGLSBTC","BRDBTC","ONGUSDT","BNBTRY","WRXUSDT","GTOBTC","PHBBTC","BNBTUSD","CTSIBTC",
    # "XRPTUSD","SOLBNB","SKYBTC","MTLBTC","KMDBTC","TROYBTC","ALGOBNB","VIBBTC","YOYOBTC","XRPTRY","XZCBTC","POWRBTC","CTXCUSDT","ADXETH",
    # "PERLBTC","KNCETH","MTLUSDT","GASBTC","AMBBTC","BEAMUSDT","BTTBNB","CHZBNB","STEEMBTC","ENJBNB","EOSTUSD","REQBTC","ETCETH","IOTXUSDT",
    # "MBLUSDT","WTCBTC","ICXBUSD","GOBTC","CTXCBTC","ELFBTC","NPXSETH","NULSUSDT","COSUSDT","DUSKUSDT","SNMBTC","TROYUSDT","TCTBTC","IOTXBTC",
    # "EVXBTC","ONTETH","XMRBNB","NASETH","BATBUSD","ZECUSDC","OSTETH","POABTC","DENTUSDT","IOSTETH","COSBTC","SNTETH","TCTUSDT","ADATUSD",
    # "XLMBNB","NEOBNB","RCNBTC","BNBNGN","ZENETH","BEAMBTC","TRXTUSD","MFTETH","GXSBTC","BATETH","ONTBNB","ZRXETH","IOTXETH","NEOUSDC","WPRBTC",
    # "VIABTC","QSPBTC","WRXBTC","MITHBNB","ATOMBNB","DUSKBTC","MTHBTC","PHBTUSD","VIBETH","HIVEUSDT","ATOMUSDC","CDTBTC","NCASHETH","QLCBTC",
    # "NAVBTC","NASBTC","RVNBUSD","GXSETH","QKCETH","CNDBTC","CTSIBUSD","STEEMETH","ICXBNB","WAVESBNB","DASHBNB","BCPTBTC","ZECBNB","HIVEBTC",
    # "COCOSUSDT","NULSBTC","CMTBTC","LINKTUSD","WINBNB","VIBEBTC","WABIBNB","LSKETH","ENJBUSD","BANDBNB","KEYETH","CELRBNB","BCHABCPAX","RLCETH",
    # "NKNBTC","TOMOBNB","LTCPAX","DENTETH","WANETH","QSPETH","APPCBTC","RDNBTC","LOOMETH","COCOSBNB","RVNBNB","AIONETH","BQXETH","ETCBNB",
    # "XRPRUB","XTZBNB","VITEUSDT","NKNUSDT","PIVXETH","ONEBNB","IOTABNB","KAVABNB","BNTETH","FETBNB","TRXPAX","QTUMBUSD","QLCETH",
    # "FTTBNB","XZCETH","MANAETH","REPETH","CDTETH","BLZETH","ALGOTUSD","ZENBNB","CVCETH","QTUMETH","BLZBNB","VITEBTC","DATAETH","HBARBNB",
    # "MTLETH","BNBRUB","WTCETH","BTTTUSD","POWRETH","BTTUSDC","BRDETH","STORJETH","MFTBNB","BUSDRUB","KMDETH","BATUSDC","ELFETH",
    # "IOSTBNB","FTMBNB","MATICBNB","BNTBUSD","WINUSDC","STEEMBNB","PERLBNB","TNBBTC","BATBNB","CMTETH","WTCBNB","TROYBNB",
    # "XRPPAX","WANBNB","MBLBTC","ZRXBNB","CTSIBNB","BNBPAX","MBLBNB","WRXBNB","BCCBNB","BCHBTC","BCHTUSD"

    ]

    
    # selected_coin = st.sidebar.selectbox(
    #     "Choose a coin",
    #     coin_list
    # )
    # selected_metrics = st.sidebar.multiselect(
    #     'Choose metrics to observe',
    #     coin_list)

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

        columns = ['rsi_7', 'rsi_14', 'wr_6', 'wr_10', 'macd', 'cci', 'cci_20']
        stats_list = []
        success_coin_list = []

        for index, coin in enumerate(coin_list):
            try:
                controller.historic_data = controller.find_history(coin)
                controller.historic_data['Open time converted'] = controller.historic_data.index.astype("int64")/1000
                controller.historic_data['Open time converted'] = controller.historic_data['Open time converted'].apply(lambda x: datetime.fromtimestamp(x))

                controller.prepare_data()
                controller.preprare_Sdf_data()
                temp_list = []
                for col in columns:

                    metric = controller.calculate_metrics(col)
                    temp_list.append(metric.iloc[-1:][0])

                metric_list_dict[coin] = temp_list
                stats_list.append(temp_list)
                success_coin_list.append(coin)
            except Exception as e:
                print(e)
                continue
        stats_df = pd.DataFrame(columns = columns, data = stats_list)
        stats_df.index = success_coin_list

        # wr_collist = [x for x in columns if "wr" in x]
        # rsi_collist = [x for x in columns if "rsi" in x]
        # for i in wr_collist:
        #     stats_df[i].style.applymap(color_wr)
        
        # for i in rsi_collist:
        #     stats_df[i].style.applymap(color_rsi)

        st.dataframe(stats_df)
        
