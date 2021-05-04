# stock_app.py
from logging import debug
from flask import Flask, render_template, redirect, request, escape
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import os
import Stock_Funcs

app = Flask(__name__)

def plot(data, single_stock):
        data_to_plot = data.reset_index()
        x_vals = data_to_plot['Date']

        multi = False
        try:
            [float(x) for x in data_to_plot['High']]
        except:
            multi=True


        plt.figure(figsize=(11,7))
        if multi==True:
            for i in data_to_plot['High']:
                y_val = data_to_plot['High'][i]
                plt.plot(x_vals, y_val, linewidth=2.5)
                plt.legend([i for i in data_to_plot['High']], loc='upper left')
        else:
            plt.plot(x_vals, data_to_plot['High'], linewidth=2.5)
            plt.legend(single_stock, loc='upper left')

        plt.xticks(rotation=50)
        plt.xlim(min([j for i,j in enumerate(x_vals)]),max([j for i,j in enumerate(x_vals)]))
        plt.ylabel('Price ($USD)')
        plt.grid(zorder=3)
        buf = BytesIO()
        plt.savefig(buf, format='png')
        data = base64.b64encode(buf.getbuffer()).decode('ascii')
        return f"'data:image/png;base64,{data}'/"



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
    single_stock = [k if len(tickers)==1 else 'Searched Stock' for k in tickers]
    chart = plot(data_to_chart, single_stock)

    return render_template('query_form.html', output_string=output_string, amount=print_amount, chart=chart)

if __name__=="__main__":
    app.run(debug=True)

