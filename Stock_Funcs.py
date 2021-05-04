# Stock_Funcs
# realtimestockdata
import datetime
import yfinance
import matplotlib.pyplot as plt
import base64
from io import BytesIO


def calculate(tickers, start, amount):
    tickers = [str(i) for i in tickers if len(i)>0]

    amount = int(amount)

    #----------USE DATETIME AND SPLIT TO PULL JUST TODAY'S DATE IN FORMAT "YYY-MM-DD"
    today = str(datetime.datetime.today())
    today_as_date = today.split()
    this_day = today_as_date[0]

    #----------FUNCTION TO USE YFINANCE TO DOWNLOAD RELEVANT DATA
    def pulldata_tochart(ticker,startdate,enddate=this_day):
        data = yfinance.download(ticker, startdate, enddate, progress=False)
        return data


    #----------FUNCTION TO TAKE DOWNLOADED DATA AND CREATE DICTIONARY OF TICKER:INVESTMENT AFTER TIME - HAS LISTS FOR ALL COLUMNS IN DOWNLOADED DATASET
    #----------OUTPUTS A TUPLE OF DICTIONARIES- ticker_dictionary[0] is the dictionary, ticker_dictionary[1] is the number of shares purchasable with the input amount
    def ticker_dictionary(yfinancedata,tickerdic,investment):

        num_shares = {k:v for k,v in tickerdic.items()}
        adj_price = {k:v for k,v in tickerdic.items()}

        if len(tickerdic.items()) > 1:                                               #NEED SECOND INDEX FOR LIST COMPREHENDING THE DATASET, BUT THIS BREAKS IF THERE IS ONLY ONE TICKER, FIXED WITH CONDITIONAL
            for ticker,vested in tickerdic.items():
                open = []
                high = []

                open = [round(i,2) for i in yfinancedata['Open'][ticker]]
                high = [round(i,2) for i in yfinancedata['High'][ticker]]
                
                num_shares[ticker] = round(investment/ open[0],2)
                if open[0] < high[-1]:                                               #MATH FOR INCREASING PERCENTAGE IS DIFFERENT THAN DECREASING
                    adj_price[ticker] *= round((((high[-1] - open[0])/open[0])),2)
                else:
                    adj_price[ticker] = round((((open[0] - high[1])/open[0])*100),2)
        else:
            for ticker,vested in tickerdic.items():
                open = []
                high = []

                open = [round(i,2) for i in yfinancedata['Open']]
                high = [round(i,2) for i in yfinancedata['High']]

                num_shares[ticker] = round(investment/ open[0],2)

                if open[0] < high[-1]:
                    adj_price[ticker] *= round((((high[-1] - open[0])/open[0])),2)
                else:
                    adj_price[ticker] = round((((open[0] - high[1])/open[0])*100),2)
            
        return (adj_price, num_shares)

    ticker_and_investment = {}

    #----------INITIALIZE TICKER AND INVESTMENT DICTIONARY
    for i in tickers:
        ticker_and_investment[i.upper()] = amount

    globaldata = pulldata_tochart(tickers, start)

#---------RUN FUNCTIONS TO COLLECT OUR DICTIONARIES
    adj_price = ticker_dictionary(globaldata, ticker_and_investment, amount)[0]
    num_of_shares = ticker_dictionary(globaldata, ticker_and_investment, amount)[1]
    
    # single_stock = [k if len(adj_price.keys())==0 else 'Searched Stock' for k in adj_price.keys()]
    # cached_chart = showchart(globaldata,single_stock)
    output = []
    for i,j in adj_price.items():
        output.append(f"Your {num_of_shares[i]} shares of {i} would now be worth ${j:,}")
#---------OUTPUT THE DATA!!!
    return output, globaldata
