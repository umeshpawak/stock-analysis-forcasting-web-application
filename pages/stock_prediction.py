import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf
import ta
from pages.utils.model_train import forecast_pipeline, get_data
from pages.utils.plotly_figure import plotly_table


def app():
    """Stock Prediction Page (Clean + Final Version)"""

    # Streamlit earlier versions don't natively support programmatic page switching easily.
    # A simple anchor link pointing back to the root acts as a Home button.
    st.markdown('<a href="/" target="_self" style="text-decoration: none; padding: 0.5rem 1rem; background-color: #f0f2f6; border-radius: 5px; color: black; font-weight: bold;">⬅️ Home</a><br><br>', unsafe_allow_html=True)

    st.title("Stock Prediction")

    # INPUT 
    ticker = st.text_input("Stock Ticker", value="AAPL").upper().strip()

    if not ticker:
        st.info("Enter a stock ticker")
        return

    # DATA FETCH 
    # yaha hum stock ka last 1 year data fetch kar rahe hai
    df = yf.download(ticker, period="1y", progress=False)

    if df.empty:
        st.error("No data found")
        return

    series = df["Close"]
    periods = 30   

    # MODEL RUN 
    # squeeze multi-level columns if needed
    if isinstance(series, pd.DataFrame):
        series = series.squeeze()
    result = forecast_pipeline(series, periods)
    forecast_df = result["forecast_df"]
    rmse = result["rmse"]

    if forecast_df is None or forecast_df.empty:
        st.error("Forecast failed")
        return

    # SECTION 1: TEXT 
    st.write(f"Predicting Next {periods} days Close Price for: {ticker}")

    # SECTION 2: RMSE (shown once, number in green) 
    if "nrmse" in result:
        nrmse = result["nrmse"]
        st.markdown(
            f"Normalized RMSE: <span style='color:#2ecc71; font-weight:bold;'>{nrmse:.4f}</span>",
            unsafe_allow_html=True,
        )

    # SECTION 3: TABLE 
    st.write("Forecast Data (Next 30 days)")

    table_df = forecast_df.copy()
    table_df = table_df.reset_index()
    table_df.columns = ["Date", "Close"]

    table_df["Date"] = pd.to_datetime(table_df["Date"]).dt.strftime('%Y-%m-%d')
    table_df["Close"] = table_df["Close"].astype(float).round(2)

    fig_val = plotly_table(table_df, height=350)
    st.plotly_chart(fig_val, use_container_width=True)

    st.markdown("---")

    # SECTION 4: CHART 
    history = series.tail(100)

    fig = go.Figure()

    # 📉 Historical
    fig.add_trace(go.Scatter(
        x=history.index,
        y=history.values,
        mode='lines',
        name='Historical',
        line=dict(color='black')
    ))

    # 🔴 Forecast (connected)
    last_date = history.index[-1]
    last_price = history.values[-1]

    future_dates = pd.to_datetime(forecast_df.index)
    future_prices = forecast_df["Close"].values

    x_vals = [last_date] + list(future_dates)
    y_vals = [last_price] + list(future_prices)

    fig.add_trace(go.Scatter(
        x=x_vals,
        y=y_vals,
        mode='lines',
        name='Forecast',
        line=dict(color='red')
    ))

    fig.update_layout(
        title=f"30-Day Forecast: {ticker}",
        xaxis_title="Date",
        yaxis_title="Price",
        template="plotly_white",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    app()