from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import pmdarima as pm
import pymongo
import pickle
from datetime import datetime, timedelta
import requests
import os
import zipfile
import time
os.environ['KMP_DUPLICATE_LIB_OK']='True'
from zipfile import ZipFile


class Modelo:
    def __init__(self):
        client = pymongo.MongoClient(
            "mongodb+srv://"+"pepitoenpeligro"+":"+"QDGzSuG1Wv9QtQ6Z"+"@cluster0.xoro9.mongodb.net/test?retryWrites=true&w=majority")
        self.data = client.p2Airflow['sanfrancisco']

    def create_export_model(self):
        dataframe = pd.DataFrame(list(self.data.find()))
        print(dataframe)
        dataframe = dataframe.dropna()
        #print(dataframe.columns)

        modelo_temp = pm.auto_arima(
            dataframe['TEMP'].dropna(),
            start_p=1, start_q=1,
            test='adf',       # use adftest to find optimal 'd'
            max_p=3, max_q=3, # maximum p and q
            m=1,              # frequency of series
            d=None,           # let model determine 'd'
            seasonal=False,   # No Seasonality
            start_P=0,
            D=0,
            trace=True,
            error_action='ignore',
            suppress_warnings=True,
            stepwise=True)

        pickle.dump(modelo_temp, open("./model__temp.p", "wb" ) )

        modelo_temp = pm.auto_arima(
            dataframe['HUM'].dropna(),
            start_p=1, start_q=1,
            test='adf',       # use adftest to find optimal 'd'
            max_p=3, max_q=3, # maximum p and q
            m=1,              # frequency of series
            d=None,           # let model determine 'd'
            seasonal=False,   # No Seasonality
            start_P=0,
            D=0,
            trace=True,
            error_action='ignore',
            suppress_warnings=True,
            stepwise=True)
        
        pickle.dump(modelo_temp, open("./model__hum.p", "wb" ) )

    def compress(self):
        with ZipFile('./modelos/model__temp.p.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
            zip.write('./modelos/model__temp.p')

        with ZipFile('./modelos/model__hum.p.zip', 'w', zipfile.ZIP_DEFLATED) as zip:
            zip.write('./modelos/model__hum.p')


if __name__ == "__main__":
    m = Modelo()
    #m.create_export_model()
    m.compress()