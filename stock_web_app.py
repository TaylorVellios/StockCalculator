# stock_app.py
from ast import Bytes
from flask import Flask, render_template, redirect, request
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import base64
from io import BytesIO

from time import sleep
import Stock_Funcs

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'null'

def plot(data):
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
    image = base64.b64encode(buf.getbuffer()).decode('ascii')
    buf.close()
    return f"'data:image/png;base64,{image}'/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calc', methods=['POST'])
def stock_calc():


    form = request.form
    ticker1 = form['ticker1']
    ticker2 = form['ticker2']
    ticker3 = form['ticker3']
    ticker4 = form['ticker4']

    start = form['start']
    amount = form['amount']
    intamount = int(amount)
    print_amount = f'{intamount:,d}'
    tickers = [ticker1, ticker2, ticker3, ticker4]

    output_string, data_to_chart = Stock_Funcs.calculate(tickers, start, amount)
    chart = plot(data_to_chart)

    return render_template('query_form.html', output_string=output_string, amount=print_amount, chart=chart)

if __name__=="__main__":
    app.run(debug=True)

