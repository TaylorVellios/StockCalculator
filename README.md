# StockCalculator
## Remember that equity you didn't purchase? Now you can find out how much money you missed out on! (Or saved..)

![Capture](https://user-images.githubusercontent.com/14188580/111310046-9b77cc00-862a-11eb-831a-3796f740de84.PNG)

Using the yfinance and matplotlib libraries, this script takes user inputs (highlighted above) and returns the increase or decrease of an initial investment in any number of equities.

# Prerequisites
Install yfinance and matplotlib with pip<br>
```
$ pip install yahoo-finance
```

```
$ python -m pip install -U matplotlib
```

# How to Use
Download the Stock_Calc.py file, navigate to its directory in bash or open it in your IDE of choice.<br>
As long as you have the required libraries installed, follow the prompts from the script in your terminal to begin calculating.<br><br>

![Capture2](https://user-images.githubusercontent.com/14188580/111311726-8ef47300-862c-11eb-90e4-5078e36d562b.PNG)
<br>
## Inputs
The first thing you will be asked is to input the ticker symbols you would like to search for. These are case in-sensitive, but a typo or asking for data before a ticker hit IPO will result in "nan" outputs. You can input as many different tickers as you want (separate each one with a single space) or a single ticker.<br>

Next, you will need to input a date that will represent when you would have bought into the equities listed above. The terminal will output the YYYY-MM-DD format that you need to copy, hyphens included. Please ensure that your input vertically matches the example display printed in the terminal.<br>

Finally, enter the amount you wish you had invested. If you entered more than one ticker, the invested amount will be the same for each.
