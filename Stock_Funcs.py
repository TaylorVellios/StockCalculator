from datetime import datetime
import matplotlib
import yfinance
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import base64
from io import BytesIO

def calculate(tickers, start, amount):
    tickers = [str(i.upper()) for i in tickers if len(i)>0]

    amount = int(amount)

#----------USE DATETIME AND SPLIT TO PULL JUST TODAY'S DATE IN FORMAT "YYYY-MM-DD"
    this_day = datetime.strftime(datetime.today(),'%Y-%m-%d')


#----------FUNCTION TO USE YFINANCE TO DOWNLOAD RELEVANT DATA
    def pulldata_tochart(ticker,start,enddate=this_day):
        data = yfinance.download(ticker, start, enddate, progress=False)
        return data.reset_index()


    def stock_change(yfinance_data, investment):
        shares = round(investment / yfinance_data['Open'][0], 3)
        value = round(shares * [i for i in yfinance_data['Close']][-1], 2)
        return (f"{value:,}", shares)

    charting_data = {}
    for i in tickers:
        charting_data[i] = pulldata_tochart(i,start)

    value_and_shares = []
    for i in tickers:
        calc = stock_change(charting_data[i], amount)
        value_and_shares.append(f"Your {calc[1]} shares of {i} would now be worth: ${calc[0]}")

    return value_and_shares, charting_data

def plot(data):
    BytesIO.truncate(0)
    data_to_plot = data

    x_max = 0
    x_min = 0
    title_loop = []
    for h,i in enumerate(data_to_plot.keys()):
        plt.plot(data_to_plot[i]['Date'], data_to_plot[i]['High'], label=i, linewidth=3)
        title_loop.append(i)
        if h==0:
            x_max = max(data_to_plot[i]['Date'])
            x_min = min(data_to_plot[i]['Date'])

    plt.legend(fontsize=10, loc='best')
    plt.title(f"Price Movement for Equities: {'--'.join(title_loop)}")
    plt.xticks(rotation=35, fontsize=8)
    plt.xlim(x_min,x_max)
    plt.ylabel('Price ($USD)')
    plt.grid(zorder=3)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    data = base64.b64encode(buf.getbuffer()).decode('ascii')
    title_loop.clear()
    return f"'data:image/png;base64,{data}'/"