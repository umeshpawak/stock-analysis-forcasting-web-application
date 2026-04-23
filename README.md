# 📈 Stock Analysis & Forecasting Dashboard

A professional, interactive **Stock Analysis & Forecasting Web App** built using Streamlit.
It enables users to analyze historical stock data, explore financial metrics, apply technical indicators, and predict future prices using machine learning.

---

## 🌐 Live Demo

👉 https://stock-analysis-forcasting-web-application-nj6orshzsnfwekcxqkie.streamlit.app

---

##  Key Highlights

* Built an **end-to-end ML-powered stock forecasting system**
* Deployed a **live cloud-based application using Streamlit**
* Integrated **real-time financial data** using yFinance API
* Implemented **technical indicators** (RSI, MACD, SMA)
* Designed **interactive dashboards** with Plotly
* Structured modular code with scalable architecture

---

##  Screenshots

###  Home Page
<img width="1440" height="900" alt="Screenshot 2026-04-24 at 2 45 19 AM" src="https://github.com/user-attachments/assets/bcd95dfa-e4f2-431d-8c2e-839a0f604875" />



### 📊 Stock Analysis
<img width="1440" height="900" alt="Screenshot 2026-04-24 at 2 46 31 AM" src="https://github.com/user-attachments/assets/ba564f93-73f9-4bad-85b0-f0ed39e85298" />
---

## ⚙️ Features

* **Comprehensive Stock Analysis**
  View key financial metrics like Market Cap, P/E Ratio, EPS, Profit Margins, and Debt-to-Equity.

* **Interactive Charts**
  Toggle between Candlestick & Line charts with dynamic timeframes (5D, 1M, YTD, 5Y, MAX).

* **Technical Indicators**

  * SMA (50, 200)
  * RSI
  * MACD

* **Stock Price Forecasting**
  Predict future prices using **Facebook Prophet time-series model**.

* **Modern UI**
  Clean, responsive interface with smooth navigation.

---

## 🛠️ Tech Stack

* **Frontend**: Streamlit
* **Data Source**: yFinance API
* **Visualization**: Plotly
* **ML & Forecasting**: Prophet, scikit-learn
* **Data Processing**: pandas, numpy
* **Technical Analysis**: ta

---

## 📦 Installation & Setup

```bash
# Clone repository
git clone https://github.com/umeshpawak/stock-analysis-forcasting-web-application.git

cd stock-analysis-forcasting-web-application

# Create virtual environment
python -m venv venv_new
source venv_new/bin/activate   # Windows: venv_new\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run trading_App.py
```

---

## 📂 Project Structure

```
.
├── trading_App.py              # Main entry point
├── pages/
│   ├── stock_Analysis.py       # Stock analysis module
│   ├── stock_prediction.py     # Forecasting module
│   └── utils/                  # Helper functions
├── requirements.txt            # Dependencies
├── app.png                     # App screenshots
└── README.md
```

---

## ⚡ Future Improvements

* Portfolio optimization module
* News sentiment analysis integration
* User authentication & watchlist

---
