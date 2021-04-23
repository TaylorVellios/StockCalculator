# realtimestockdata
import datetime
import yfinance
import matplotlib.pyplot as plt


#----------USE DATETIME AND SPLIT TO PULL JUST TODAY'S DATE IN FORMAT "YYY-MM-DD"
today = str(datetime.datetime.today())
today_as_date = today.split()
this_day = today_as_date[0]

#----------HEADER FOR TERMINAL OUTPUT
print(
'\n---------------------------\n'
'--Stock Regret Calculator--\n'
'---------------------------\n'
)

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


    # low = [round(i,2) for i in yfinancedata['Low']]
    # close = [round(i,2) for i in yfinancedata['Close']]
    # adj_close = [round(i,2) for i in yfinancedata['Adj Close']]
    # volume = [round(i,2) for i in yfinancedata['Volume']]
        
    return (adj_price, num_shares)

#----------FUNCTION TO USE MATPLOTLIB TO CHART GIVEN TICKERS
def showchart(data,single_stock):

    data_to_plot = data.reset_index()
    for_xticks = len([i for i in data_to_plot['Date']])//10
    x_vals = data_to_plot['Date']

    multi = False
    try:
        [float(x) for x in data_to_plot['High']]
    except:
        multi=True


    plt.figure(figsize=(12,8))
    if multi==True:
        for i in data_to_plot['High']:
            y_val = data_to_plot['High'][i]
            plt.plot(x_vals, y_val, linewidth=2.5)
            plt.legend([i for i in data_to_plot['High']], loc='upper left')
    else:
        plt.plot(x_vals, data_to_plot['High'], linewidth=2.5)
        plt.legend(single_stock, loc='upper left')

    plt.xticks([j for i,j in enumerate(x_vals) if i%for_xticks==0], rotation=50)
    plt.xlim(min([j for i,j in enumerate(x_vals) if i%for_xticks==0]),max([j for i,j in enumerate(x_vals) if i%for_xticks==0]))
    plt.ylabel('Price ($USD)')
    plt.grid(zorder=3)
    plt.title('Close Chart to See Results')
    plt.show()

#----------SETTING UP OUR MAIN RUNLOOP WITH BREAK SEQUENCE + Global Variables
run = True
while run:
    ticker_and_investment = {}

#----------COLLECT TICKER NAMES/Date/INVEST AMT
    print(
        '---------------------------------------------\n'
        '---Separate Multiple Tickers by Whitespace---\n'
        '---------------------------------------------'
    )
    ticker = str(input("Enter Ticker Name(s): ")).upper()
    print()

    buy_date = input('What Date Did You Want To Buy On?\n"YYYY-MM-DD"\n ')
    print()

    investment = int(input('How Much Would You Have Invested? '))
    print()

#----------INITIALIZE TICKER AND INVESTMENT DICTIONARY
    for i in ticker.split():
        ticker_and_investment[i] = investment

    globaldata = pulldata_tochart(ticker, buy_date)

#---------RUN FUNCTIONS TO COLLECT OUR DICTIONARIES
    adj_price = ticker_dictionary(globaldata, ticker_and_investment, investment)[0]
    num_of_shares = ticker_dictionary(globaldata, ticker_and_investment, investment)[1]


#---------OUTPUT THE DATA!!!
    print('---------------------------------------------\n')
    print(f'With an initial investment of ${investment:,} on {buy_date}..')
    
    for k,v in adj_price.items():
        print(f'Your {num_of_shares[k]} shares of {k} would now be worth ${v:,}')

    single_stock = [k if len(adj_price.keys())==0 else 'Searched Stock' for k in adj_price.keys()]
    print()
#----------DETERMINE IF USER WANTS A MATPLOTLIB PLOT
    print(
        '---------------------------------------------\n'
        '-----------Show Chart?  [Y]es to Show--------\n'
        '---------------------------------------------')
    chart = str(input()).upper()
    if chart == 'Y':
        showchart(globaldata,single_stock)
    elif chart == 'N':
        break
    print()
#----------DETERMINE IF USER RUNS AGAIN OR KILLS
    again = str(input('Look Up More Tickers?\n[Y]es/[N]o: ')).upper()
    if again == 'Y':
        pass
    elif again == 'N':
        break
    else:
        print('Invalid Command, Breaking.')
        break