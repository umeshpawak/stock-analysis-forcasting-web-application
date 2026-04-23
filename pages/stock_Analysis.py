import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
from pages.utils.plotly_figure import plotly_table
from plotly.subplots import make_subplots
try:
    import ta
    from ta.momentum import RSIIndicator
    from ta.trend import MACD
except ImportError:
    ta = None
    RSIIndicator = None
    MACD = None

def app():
    # A simple anchor link pointing back to the root acts as a Home button.
    st.markdown('<a href="/" target="_self" style="text-decoration: none; padding: 0.5rem 1rem; background-color: #f0f2f6; border-radius: 5px; color: black; font-weight: bold;">⬅️ Home</a><br><br>', unsafe_allow_html=True)

    st.title("Stock Analysis")

    # 3 columns banaye hain - ticker, start date, end date input ke liye
    col1, col2, col3 = st.columns(3)
    today = datetime.date.today()

    # Column 1: Stock ka ticker symbol input le rahe hain (e.g., TSLA, AAPL)
    with col1:
        ticker = st.text_input("Stock Ticker", value="TSLA").upper().strip()

    # Column 2: Start date select karne ke liye - default 1 year pehle se
    with col2:
        start_date = st.date_input("Choose Start Date", datetime.date(today.year - 1, today.month, today.day))

    # Column 3: End date select karne ke liye - default aaj ka date
    with col3:
        end_date = st.date_input("Chose End Date", datetime.date(today.year, today.month, today.day))

    st.subheader(ticker)

    stock = yf.Ticker(ticker)

    summary = stock.info.get('longBusinessSummary', "No data available")
    if len(summary) > 500:
        st.write(summary[:500] + "...")
        with st.expander("Read More"):
            st.write(summary[500:])
    else:
        st.write(summary)
        
    st.markdown("---")

    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.write("**Sector:**", stock.info.get('sector', "No data available"))
    with col_info2:
        st.write("**Full Time Employes:**", stock.info.get('fullTimeEmployees', "No data available"))
        st.write("**Website:**", stock.info.get('website', "No data available"))

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        df1 = pd.DataFrame({
            "Metric": ['Market Cap', 'Beta', 'EPS', 'PE Ratio'],
            "Value": [
                stock.info.get("marketCap", "N/A"),
                stock.info.get("beta", "N/A"),
                stock.info.get("trailingEps", "N/A"),
                stock.info.get("trailingPE", "N/A")
            ]
        })
        fig1 = plotly_table(df1, height=180)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        df2 = pd.DataFrame({
            "Metric": ['Quick Ratio', 'Revenue Per Share', 'Profit Margin', 'Debt to Equity', 'Return on Equity'],
            "Value": [
                stock.info.get("quickRatio", "N/A"),
                stock.info.get("revenuePerShare", "N/A"),
                stock.info.get("profitMargins", "N/A"),
                stock.info.get("debtToEquity", "N/A"),
                stock.info.get("returnOnEquity", "N/A")
            ]
        })
        fig2 = plotly_table(df2, height=180)
        st.plotly_chart(fig2, use_container_width=True)

    data = yf.download(ticker, start=start_date, end=end_date)
    data.columns = data.columns.get_level_values(0)

    if data.shape[0] < 2:
        st.warning("Not enough historical data for the selected range.")
        return

    daily_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
    previous_close = data['Close'].iloc[-2]
    percentage_change = (daily_change / previous_close) * 100

    st.subheader("Daily Change")
    st.metric(
        label=f"{ticker}",
        value=round(data['Close'].iloc[-1], 2),
        delta=f"{round(daily_change, 2)} ({round(percentage_change, 2)}%)"
    )

    last_10_df = data.tail(10).sort_index(ascending=False).round(3)
    fig_df = plotly_table(last_10_df, height=500)

    st.markdown("---")
    st.write('#### Historical Data (last 10 days)')
    st.plotly_chart(fig_df, width='stretch')

    # Chart controls
    st.markdown("---")
    pcol = st.columns([1, 1, 1, 1, 1, 1, 1])
    start_override = None
    if pcol[0].button("5D"):
        start_override = datetime.date.today() - datetime.timedelta(days=5)
    if pcol[1].button("1M"):
        start_override = datetime.date.today() - datetime.timedelta(days=30)
    if pcol[2].button("6M"):
        start_override = datetime.date.today() - datetime.timedelta(days=182)
    if pcol[3].button("YTD"):
        start_override = datetime.date(datetime.date.today().year, 1, 1)
    if pcol[4].button("1Y"):
        start_override = datetime.date.today() - datetime.timedelta(days=365)
    if pcol[5].button("5Y"):
        start_override = datetime.date.today() - datetime.timedelta(days=365 * 5)
    if pcol[6].button("MAX"):
        start_override = datetime.date.today() - datetime.timedelta(days=365 * 20)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        chart_type = st.selectbox("Chart Type", ["Candle", "Line"], index=0)
    with col_b:
        indicator = st.selectbox("Indicator", ["None", "RSI", "MACD", "Moving Average"], index=0)

    if start_override is not None:
        start_date = start_override
        # Download chart specifically to accommodate expanded ranges like 'MAX' or '5Y'
        chart_data = yf.download(ticker, start=start_date, end=end_date)
        if not chart_data.empty:
            chart_data.columns = chart_data.columns.get_level_values(0)
    else:
        chart_data = data.copy()


    def make_chart(df, chart_type='Candle', indicator='None'):
        add_rsi = indicator == 'RSI'
        add_macd = indicator == 'MACD'
        rows = 1 + (1 if add_rsi or add_macd else 0)
        specs = [[{"secondary_y": False}]] * rows
        fig = make_subplots(rows=rows, cols=1, shared_xaxes=True,
                            vertical_spacing=0.06, specs=specs)

        if chart_type == 'Candle':
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Price'), row=1, col=1)
        else:
            fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name='Close'), row=1, col=1)

        if indicator == 'Moving Average':
            df['SMA_50'] = df['Close'].rolling(50).mean()
            df['SMA_200'] = df['Close'].rolling(200).mean()
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], name='SMA 50', line=dict(color='orange')), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_200'], name='SMA 200', line=dict(color='purple')), row=1, col=1)

        if add_rsi:
            if RSIIndicator is not None:
                rsi = RSIIndicator(close=df['Close'], window=14).rsi()
                fig.add_trace(go.Scatter(x=df.index, y=rsi, name='RSI', line=dict(color='orange')), row=2, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=[70] * len(df), name='Overbought', line=dict(color='red', dash='dash')), row=2, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=[30] * len(df), name='Oversold', line=dict(color='green', dash='dash')), row=2, col=1)
            else:
                st.warning("The 'ta' library is missing. Install it with pip install ta.")

        if add_macd:
            if MACD is not None:
                macd_obj = MACD(close=df['Close'])
                macd = macd_obj.macd()
                macd_sig = macd_obj.macd_signal()
                macd_hist = macd - macd_sig
                fig.add_trace(go.Bar(x=df.index, y=macd_hist, name='MACD Hist', marker_color='lightblue'), row=2, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=macd, name='MACD', line=dict(color='black')), row=2, col=1)
                fig.add_trace(go.Scatter(x=df.index, y=macd_sig, name='Signal', line=dict(color='red')), row=2, col=1)
            else:
                st.warning("The 'ta' library is missing. Install it with pip install ta.")

        fig.update_layout(height=700 if rows > 1 else 500, showlegend=True)
        return fig


    if not chart_data.empty:
        fig = make_chart(chart_data, chart_type=chart_type, indicator=indicator)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No chart data available for the selected range.")


# When Streamlit imports this module as a page, call app() so the page renders
if __name__ == "__main__":
    app()

