import quandl
import pandas as pd
import matplotlib.pyplot as plt


if __name__ =='__main__':
    quandl.ApiConfig.api_key = 'aaaa'

    brand = "TSE/2737"
    quandl_data = quandl.get(dataset=brand, returns='pandas')

    quandl_data.to_csv('sotock_price_data.csv')

    print('fin')