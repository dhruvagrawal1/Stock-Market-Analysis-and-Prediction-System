import streamlit as st
import pandas as pd
import datetime
import time
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.title("Stock Price Screener and Analysis")
pd.set_option('max_colwidth', 400)
if datetime.time(15, 30) < datetime.datetime.now().time():
    st.write("Market is closed")
nifty, sensex = st.columns(2)
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
if yesterday.weekday() == 5:
    yesterday = yesterday - datetime.timedelta(days=1)
elif yesterday.weekday() == 6:
    yesterday = yesterday - datetime.timedelta(days=2)
with nifty:
    st.header("Nifty 50")
    nifty_df_today = pd.DataFrame()
    nifty_df_today = yf.download("^NSEI", start=today, interval="2m")
    st.write(nifty_df_today['Close'].iloc[-1])
    nifty_df_yesterday = pd.DataFrame()
    nifty_df_yesterday = yf.download(
        "^NSEI", start=yesterday, end=today, interval="2m")
    percent_change_nifty = (
        nifty_df_today['Close'].iloc[-1] - nifty_df_yesterday['Close'].iloc[-1]) / (nifty_df_today['Close'].iloc[-1]) * 100
    percent_change_nifty = round(percent_change_nifty, 2)

    if datetime.time(15, 30) > datetime.datetime.now().time():
        if percent_change_nifty > 0:
            st.write("Nifty 50 Index is up by {}%".format(percent_change_nifty))
        else:
            st.write("Nifty 50 Index is down by {}%".format(
                percent_change_nifty))
    else:
        if percent_change_nifty > 0:
            st.write("Nifty 50 Index was up by {}%".format(
                percent_change_nifty))
        else:
            st.write("Nifty 50 Index was down by {}%".format(
                percent_change_nifty))
with sensex:
    st.header("Sensex")
    sensex_df = pd.DataFrame()
    sensex_df = yf.download("^BSESN", start=today, interval="2m")
    st.write(sensex_df['Close'].iloc[-1])
    sensex_df_yesterday = pd.DataFrame()
    sensex_df_yesterday = yf.download(
        "^BSESN", start=yesterday, end=today, interval="2m")
    percent_change_sensex = (
        sensex_df['Close'].iloc[-1] - sensex_df_yesterday['Close'].iloc[-1]) / (sensex_df['Close'].iloc[-1]) * 100
    percent_change_sensex = round(percent_change_sensex, 2)
    if datetime.time(15, 30) > datetime.datetime.now().time():
        if percent_change_sensex > 0:
            st.write("Sensex Index is up by {}%".format(percent_change_sensex))
        else:
            st.write("Sensex Index is down by {}%".format(
                percent_change_sensex))
    else:
        if percent_change_sensex > 0:
            st.write("Sensex Index was up by {}%".format(
                percent_change_sensex))
        else:
            st.write("Sensex Index was down by {}%".format(
                percent_change_sensex))
todays_stock, stocks, indicators, int_stocks = st.tabs(
    ["Stock price for Today ", "Historical Price of Stock", "Indicators", "International Stocks"])

with todays_stock:
    st.title("Today's Price of Stock")
    today = datetime.date.today()
    if today.weekday() == 5:
        today = today - datetime.timedelta(days=1)
        st.write("Market is closed on Saturday.")
    elif today.weekday() == 6:
        today = today - datetime.timedelta(days=2)
        st.write("Market is closed on Sunday.")
    stock = st.text_input("Enter a stock ticker symbol", "LT")
    Today_stock = st.button("Get Today's Price")

    if Today_stock:
        start_date = today
        df_today = pd.DataFrame()
        df_today = yf.download(f"{stock}.NS", start=start_date, interval="2m")
        df_today['% Change'] = df_today['Close'].pct_change()*100
        df_today['% Change'] = df_today['% Change'].round(2)
        st.write(df_today)
        df_yesterday = pd.DataFrame()
        df_yesterday = yf.download(
            f"{stock}.NS", start=yesterday, end=today, interval="2m")
        df_yesterday['% Change'] = df_yesterday['Close'].pct_change()*100
        df_yesterday['% Change'] = df_yesterday['% Change'].round(2)
        percent_change = (
            df_today['Close'].iloc[-1] - df_yesterday['Close'].iloc[-1]) / (df_today['Close'].iloc[-1]) * 100
        percent_change = round(percent_change, 2)
        if percent_change > 0:
            st.write("The stock is up by {}%".format(percent_change))
        else:
            st.write("The stock is down by {}%".format(percent_change))

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[
                            0.7, 0.3], specs=[[{"type": "candlestick"}], [{"type": "bar"}]])
        fig.update_xaxes(rangeslider_visible=False)
        fig.add_trace(go.Candlestick(x=df_today.index, open=df_today['Open'], high=df_today['High'],
                      low=df_today['Low'], close=df_today['Close'], name='market data'), row=1, col=1)
        fig.add_trace(
            go.Bar(x=df_today.index, y=df_today['Volume'], name='Volume'), row=2, col=1)

        st.plotly_chart(fig, use_container_width=True)


with stocks:
    st.title("Stocks")
    df_today = pd.DataFrame()
    today_date = datetime.date.today() + datetime.timedelta(days=1)
    if today_date.weekday() == 5:
        today_date = today_date - datetime.timedelta(days=1)
        st.write("Market is closed ")
    elif today_date.weekday() == 6:
        today_date = today_date - datetime.timedelta(days=2)
        st.write("Market is closed ")
    stock_name = st.text_input("Enter a stock ticker symbol")
    start_date = st.date_input("Start date")
    goto_today = st.button("Get Price from start date till today")
    end_date = st.date_input("End date")
    get_stock = st.button("Get Stock Price")
    if end_date < start_date:
        st.error("Error: End date must fall after start date.")
    elif goto_today:
        end_date = today_date
        diff = end_date - start_date
        if 180 > diff.days < 365 and diff.days > 90:
            interval = "1d"
        elif 90 >= diff.days >= 30:
            interval = "60m"
        elif diff.days > 365:
            interval = "1wk"

        df_stock = pd.DataFrame()
        df_stock = yf.download(f"{stock}.NS", start=start_date,
                               end=end_date, interval=interval)
        df_stock.style.set_properties(**{'text-align': 'left'})
        st.write(df_stock)
        # if df_today['% Change'].iloc[-1] > 0:
        #     st.write("The stock is up by {}%".format(
        #         df_today['% Change'].iloc[-1]))
        # else:
        #     st.write("The stock is down by {}%".format(
        #         df_today['% Change'].iloc[-1]))
        st.write("The time interval for plotting of chart is :", interval)
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[
                            0.7, 0.3], specs=[[{"type": "candlestick"}], [{"type": "bar"}]])
        fig.update_xaxes(rangeslider_visible=False)
        if interval == "1wk" or interval == "1d":
            fig.update_xaxes(
                rangebreaks=[
                    dict(bounds=["sat", "mon"]),
                ]
            )
        else:
            fig.update_xaxes(
                rangebreaks=[
                    dict(bounds=["sat", "mon"]),
                    dict(pattern='hour', bounds=[16, 9])
                ]
            )

        fig.add_trace(go.Candlestick(x=df_stock.index, open=df_stock['Open'], high=df_stock['High'],
                                     low=df_stock['Low'], close=df_stock['Close'], name='market data'), row=1, col=1)
        # bar chart
        fig.add_trace(
            go.Bar(x=df_stock.index, y=df_stock['Volume'], name='Volume'), row=2, col=1)

        st.plotly_chart(fig, use_container_width=True)
    elif get_stock:
        # get the difference between the two dates
        diff = end_date - start_date
        if 180 > diff.days < 365 and diff.days > 90:
            interval = "1d"
        # bteween 30 days and 90 days interval is 90 minutes
        elif 90 >= diff.days >= 30:
            interval = "60m"
        elif diff.days > 365:
            interval = "1wk"

        df_get_stock = pd.DataFrame()
        df_get_stock = yf.download(f"{stock}.NS", start=start_date,
                                   end=end_date+datetime.timedelta(days=1), interval=interval)
        df_get_stock.style.set_properties(**{'text-align': 'left'})
        st.write(df_get_stock)
        if df_today['% Change'].iloc[-1] > 0:
            st.write("The stock is up by {}%".format(
                df_today['% Change'].iloc[-1]))
        else:
            st.write("The stock is down by {}%".format(
                df_today['% Change'].iloc[-1]))
        st.write("The time interval for plotting of chart is :", interval)
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[
                            0.7, 0.3], specs=[[{"type": "candlestick"}], [{"type": "bar"}]])
        fig.update_xaxes(rangeslider_visible=False)
        if interval == "1wk" or interval == "1d":
            fig.update_xaxes(
                rangebreaks=[
                    dict(bounds=["sat", "mon"]),]
            )
        else:
            fig.update_xaxes(
                rangebreaks=[
                    dict(bounds=["sat", "mon"]),
                    dict(pattern='hour', bounds=[16, 9])
                ]
            )

        fig.add_trace(go.Candlestick(x=df_get_stock.index, open=df_get_stock['Open'], high=df_get_stock['High'],
                      low=df_get_stock['Low'], close=df_get_stock['Close'], name='market data'), row=1, col=1)
        # bar chart
        fig.add_trace(
            go.Bar(x=df_get_stock.index, y=df_get_stock['Volume'], name='Volume'), row=2, col=1)

        st.plotly_chart(fig, use_container_width=True)


with indicators:
    # select = st.sidebar.selectbox("Select a indicator",["aberration", "above", "above_value", "accbands", "ad", "adosc", "adx", "alma", "amat", "ao", "aobv", "apo", "aroon", "atr", "bbands","below", "below_value", "bias", "bop", "brar", "cci," "cdl_pattern", "cdl_z", "cfo", "cg", "chop","cksp", "cmf", "cmo", "coppock", "cross", "cross_value", "cti," "decay", "decreasing", "dema", "dm", "donchian", "dpo", "ebsw", "efi", "ema", "entropy", "eom", "er ","eri", "fisher", "fwma", "ha", "hilo", "hl2," "hlc3", "hma," "hwc," "hwma", "ichimoku", "increasing", "inertia", "jma", "kama", "kc", "kdj," "kst," "kurtosis", "kvo," "linreg", "log_return", "long_run," "macd"," mad", "massi", "mcgd", "median", "mfi," "midpoint", "midprice", "mom," "natr", "nvi," "obv," "ohlc4", "pdist", "percent_return", "pgo," "ppo," "psar", "psl," "pvi," "pvo," "pvol", "pvr," "pvt," "pwma", "qqe," "qstick", "quantile", "rma," "roc," "rsi," "rsx," "rvgi", "rvi," "short_run", "sinwma", "skew", "slope", "sma", "smi", "squeeze", "squeeze_pro", "ssf," "stc," "stdev", "stoch", "stochrsi", "supertrend", "swma", "t3, ""td_seq", "tema", "thermo", "tos_stdevall", "trima", "trix", "true_range", "tsi," "tsignals", "ttm_trend", "ui, ""uo, ""variance", "vhf," "vidya", "vortex", "vp, ""vwap", "vwma", "wcp," "willr", "wma," "xsignals", "zlma", "zscore"])
    candles = "2crows", "3blackcrows", "3inside", "3linestrike", "3outside", "3starsinsouth", "3whitesoldiers", "abandonedbaby", "advanceblock", "belthold", "breakaway", "closingmarubozu", "concealbabyswall", "counterattack", "darkcloudcover", "doji", "dojistar", "dragonflydoji", "engulfing", "eveningdojistar", "eveningstar", "gapsidesidewhite", "gravestonedoji", "hammer", "hangingman", "harami", "haramicross", "highwave", "hikkake", "hikkakemod", "homingpigeon", "identical3crows", "inneck", "inside", "invertedhammer", "kicking", "kickingbylength", "ladderbottom", "longleggeddoji", "longline", "marubozu", "matchinglow", "mathold", "morningdojistar", "morningstar", "onneck", "piercing", "rickshawman", "risefall3methods", "separatinglines", "shootingstar", "shortline", "spinningtop", "stalledpattern", "sticksandwich", "takuri", "tasukigap", "thrusting", "tristar", "unique3river", "upsidegap2crows", "xsidegap3methods", "Heikin-Ashi: ha", "Z Score: cdl_z"

    cycles = "Even Better Sinewave: ebsw"

    momentum = "Awesome Oscillator: ao", "Absolute Price Oscillator: apo", "Bias: bias", "Balance of Power: bop", "BRAR: brar", "Commodity Channel Index: cci", "Chande Forecast Oscillator: cfo", "Center of Gravity: cg", "Chande Momentum Oscillator: cmo", "Coppock Curve: coppock", "Correlation Trend Indicator: cti", "Directional Movement: dm", "Efficiency Ratio: er", "Elder Ray Index: eri", "Fisher Transform: fisher", "Inertia: inertia", "KDJ: kdj", "KST Oscillator: kst", "Moving Average Convergence Divergence: macd", "Momentum: mom", "Pretty Good Oscillator: pgo", "Percentage Price Oscillator: ppo", "Psychological Line: psl", "Percentage Volume Oscillator: pvo", "Quantitative Qualitative Estimation: qqe", "Rate of Change: roc", "Relative Strength Index: rsi", "Relative Strength Xtra: rsx", "Relative Vigor Index: rvgi", "Schaff Trend Cycle: stc", "Slope: slope", "SMI Ergodic smi", "Squeeze: squeeze", "Squeeze Pro: squeeze_pro", "Stochastic Oscillator: stoch", "Stochastic RSI: stochrsi", "TD Sequential: td_seq", "Trix: trix", "True strength index: tsi", "Ultimate Oscillator: uo", "Williams %R: willr"

    overlap = "Arnaud Legoux Moving Average: alma", "Double Exponential Moving Average: dema", "Exponential Moving Average: ema", "Fibonacci's Weighted Moving Average: fwma", "Gann High-Low Activator: hilo", "High-Low Average: hl2", "High-Low-Close Average: hlc3", "Commonly known as 'Typical Price' in Technical Analysis literature", "Hull Exponential Moving Average: hma", "Holt-Winter Moving Average: hwma", "Ichimoku Kinkō Hyō: ichimoku", "Jurik Moving Average: jma", "Kaufman's Adaptive Moving Average: kama", "Linear Regression: linreg", "McGinley Dynamic: mcgd", "Midpoint: midpoint", "Midprice: midprice", "Open-High-Low-Close Average: ohlc4", "Pascal's Weighted Moving Average: pwma", "WildeR's Moving Average: rma", "Sine Weighted Moving Average: sinwma", "Simple Moving Average: sma", "Ehler's Super Smoother Filter: ssf", "Supertrend: supertrend", "Symmetric Weighted Moving Average: swma", "T3 Moving Average: t3", "Triple Exponential Moving Average: tema", "Triangular Moving Average: trima", "Variable Index Dynamic Average: vidya", "Volume Weighted Average Price: vwap", "Requires the DataFrame index to be a DatetimeIndex", "Volume Weighted Moving Average: vwma", "Weighted Closing Price: wcp", "Weighted Moving Average: wma", "Zero Lag Moving Average: zlma"

    performance = "Draw Down: drawdown", "Log Return: log_return", "Percent Return: percent_return"

    statistics = "Entropy: entropy", "Kurtosis: kurtosis", "Mean Absolute Deviation: mad", "Median: median", "Quantile: quantile", "Skew: skew", "Standard Deviation: stdev", "Think or Swim Standard Deviation All: tos_stdevall", "Variance: variance", "Z Score: zscore"

    trend = "Average Directional Movement Index: adx", "Archer Moving Averages Trends: amat", "Aroon & Aroon Oscillator: aroon", "Choppiness Index: chop", "Chande Kroll Stop: cksp", "Decay: decay", "Decreasing: decreasing", "Detrended Price Oscillator: dpo", "Increasing: increasing", "Long Run: long_run", "Parabolic Stop and Reverse: psar", "Q Stick: qstick", "Short Run: short_run", "Trend Signals: tsignals", "TTM Trend: ttm_trend", "Vertical Horizontal Filter: vhf", "Vortex: vortex", "Cross Signals: xsignals"

    utility = "Above: above", "Above Value: above_value", "Below: below", "Below Value: below_value", "Cross: cross"

    volatility = "Aberration: aberration", "Acceleration Bands: accbands", "Average True Range: atr", "Bollinger Bands: bbands", "Donchian Channel: donchian", "Holt-Winter Channel: hwc", "Keltner Channel: kc", "Mass Index: massi", "Normalized Average True Range: natr", "Price Distance: pdist", "Relative Volatility Index: rvi", "Elder's Thermometer: thermo", "True Range: true_range", "Ulcer Index: ui"

    volume = "Accumulation/Distribution Index: ad", "Accumulation/Distribution Oscillator: adosc", "Archer On-Balance Volume: aobv", "Chaikin Money Flow: cmf", "Elder's Force Index: efi", "Ease of Movement: eom", "Klinger Volume Oscillator: kvo", "Money Flow Index: mfi", "Negative Volume Index: nvi", "On-Balance Volume: obv", "Positive Volume Index: pvi", "Price-Volume: pvol", "Price Volume Rank: pvr", "Price Volume Trend: pvt", "Volume Profile: vp"

    stock_name = st.text_input("Enter a stock ticker symbol", "RELIANCE")
    category = st.selectbox("Select a category", [
        'candles', 'cycles', 'momentum', 'overlap', 'performance', 'statistics', 'trend', 'volatility', 'volume'])
    button_clicked = st.button("Get Indicators")
    st.write(
        f"These are the following indicators available in {category} category")
    if category == "candles":
        st.write(candles)
    elif category == "cycles":
        st.write(cycles)
    elif category == "momentum":
        st.write(momentum)
    elif category == "overlap":
        st.write(overlap)
    elif category == "performance":
        st.write(performance)
    elif category == "statistics":
        st.write(statistics)
    elif category == "trend":
        st.write(trend)
    elif category == "volatility":
        st.write(volatility)
    elif category == "volume":
        st.write(volume)

    if button_clicked:
        df1 = pd.DataFrame()
        df1 = df1.ta.ticker(f"{stock_name}.NS", period="1y", asobject=True)
        df1.ta.strategy(category)
        df1 = df1.drop(columns=['Stock Splits', 'Dividends'])
        st.write(df1)
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[
                            0.7, 0.3], specs=[[{"type": "candlestick"}], [{"type": "bar"}]])
        fig.update_xaxes(rangeslider_visible=False)
        fig.add_trace(go.Candlestick(x=df1.index, open=df1['Open'], high=df1['High'],
                      low=df1['Low'], close=df1['Close'], name='market data'), row=1, col=1)
        # bar chart
        fig.add_trace(
            go.Bar(x=df1.index, y=df1['Volume'], name='Volume'), row=2, col=1)

        st.plotly_chart(fig, use_container_width=True)

with int_stocks:
    international = pd.DataFrame()
    today_date = datetime.date.today() + datetime.timedelta(days=1)
    if today_date.weekday() == 5:
        today_date = today_date - datetime.timedelta(days=1)
        st.write("Market is closed ")
    elif today_date.weekday() == 6:
        today_date = today_date - datetime.timedelta(days=2)
        st.write("Market is closed ")
    stock_name = st.text_input("Enter a stock ticker symbol", "AAPL")
    start_date = st.date_input("Starting date")
    end_date = st.date_input("Ending date")
    get_stock = st.button("Get the Stock Price")
    if end_date < start_date:
        st.error("Error: End date must fall after start date.")

    end_date = today_date
    diff = end_date - start_date
    interval = "1d"
    if 180 > diff.days < 365 and diff.days > 90:
        interval = "1d"
    # bteween 30 days and 90 days interval is 90 minutes
    elif 90 >= diff.days >= 30:
        interval = "60m"
    elif diff.days > 365:
        interval = "1wk"
    if get_stock:
        international = pd.DataFrame()
        international = international.ta.ticker(
            stock_name, start=start_date, end=end_date+datetime.timedelta(days=1), interval=interval)
        international = international.drop(
            columns=['Stock Splits', 'Dividends'])
        st.write(international)
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[
            0.7, 0.3], specs=[[{"type": "candlestick"}], [{"type": "bar"}]])
        fig.update_xaxes(rangeslider_visible=False)
        fig.add_trace(go.Candlestick(x=international.index, open=international['Open'], high=international['High'],
                                     low=international['Low'], close=international['Close'], name='market data'), row=1, col=1)
        # bar chart
        fig.add_trace(
            go.Bar(x=international.index, y=international['Volume'], name='Volume'), row=2, col=1)

        st.plotly_chart(fig, use_container_width=True)

