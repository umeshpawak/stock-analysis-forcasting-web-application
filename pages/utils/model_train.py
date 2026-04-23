"""
Prophet based forecasting (REAL model)
Hinglish comments added for clear understanding
"""

import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.metrics import mean_squared_error
from prophet import Prophet


# ==============================
# DATA FETCH FUNCTION
# ==============================
def get_data(ticker: str, start: str = "2020-01-01") -> pd.Series:
    """
    Yeh function stock ka historical close price laata hai
    """

    df = yf.download(ticker, start=start, progress=False)

    if df.empty:
        return pd.Series(dtype=float)

    if 'Close' in df.columns:
        s = df['Close']
    else:
        s = df.iloc[:, 0]

    s.index = pd.to_datetime(s.index)
    return s.dropna()


# ==============================
# FORECAST PIPELINE
# ==============================
def forecast_pipeline(series: pd.Series, periods: int = 30) -> dict:
    """
    Yeh function stock ka future forecast karega using Prophet model
    """

    # 1. Data cleaning
    if isinstance(series, pd.DataFrame):
        series = series.squeeze()

    series = pd.to_numeric(series, errors='coerce').dropna()
    series.index = pd.to_datetime(series.index)

    # 2. Prophet format
    df = pd.DataFrame({
        "ds": series.index,
        "y": series.values
    })

    # 3. Train/Test split
    split_idx = int(len(df) * 0.8)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]

    # 4. Model train
    model = Prophet(
        daily_seasonality=True,
        yearly_seasonality=True
    )
    model.fit(train_df)

    # 5. Test prediction
    future_test = model.make_future_dataframe(periods=len(test_df))
    forecast_test = model.predict(future_test)

    forecast_test_trimmed = forecast_test.tail(len(test_df))

    y_true = test_df["y"].values
    y_pred = forecast_test_trimmed["yhat"].values

    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    nrmse = rmse / (np.max(y_true) - np.min(y_true))

    # 6. Retrain on full data
    model_full = Prophet(
        daily_seasonality=True,
        yearly_seasonality=True
    )
    model_full.fit(df)

    # 7. Future forecast
    future = model_full.make_future_dataframe(periods=periods)
    forecast = model_full.predict(future)

    forecast_future = forecast.iloc[-periods:]

    # 8. Output
    forecast_df = pd.DataFrame({
        "Close": forecast_future["yhat"].values
    }, index=forecast_future["ds"])

    return {
        "forecast_df": forecast_df,
        "rmse": rmse,
        "nrmse": nrmse
    }