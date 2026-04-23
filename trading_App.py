import streamlit as st

st.set_page_config(page_title="Precision Ledger", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded")

def main():
    st.markdown("""
<style>
[data-testid="stHeader"] { visibility: hidden; height: 0px; }
footer { visibility: hidden; }
.block-container {
    padding: 0rem !important;
    max-width: 100% !important;
}

[data-testid="stAppViewContainer"] {
    background-color: #080d17;
    background-image: 
        radial-gradient(ellipse at 50% 0%, rgba(38, 166, 154, 0.15) 0%, transparent 60%),
        linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
    background-size: 100% 100%, 40px 40px, 40px 40px;
    background-position: center 0, center, center;
}

.hero-container {
    text-align: center;
    padding-top: 6rem;
    padding-bottom: 2rem;
}
.hero-title {
    font-size: 4rem;
    font-weight: 800;
    line-height: 1.1;
    color: #ffffff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    margin-bottom: 1rem;
    text-shadow: 0px 4px 20px rgba(0,0,0,0.5);
}
.hero-subtitle {
    font-size: 1.25rem;
    color: #a0aab8;
    font-weight: 500;
    margin-bottom: 2.5rem;
}

.btn-container {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 1rem;
}
.primary-btn {
    background-color: #26a69a;
    color: white !important;
    border-radius: 8px;
    padding: 1rem 2.5rem;
    font-weight: 600;
    font-size: 1.05rem;
    text-decoration: none;
    box-shadow: 0 4px 12px rgba(38, 166, 154, 0.3);
    transition: all 0.2s ease-in-out;
}
.primary-btn:hover {
    background-color: #1e877c;
    transform: translateY(-2px);
    color: white;
    box-shadow: 0 6px 16px rgba(38, 166, 154, 0.4);
}
.secondary-btn {
    background-color: transparent;
    border: 1px solid rgba(255,255,255,0.2);
    color: #ffffff !important;
    border-radius: 8px;
    padding: 1rem 2.5rem;
    font-weight: 600;
    font-size: 1.05rem;
    text-decoration: none;
    backdrop-filter: blur(10px);
    transition: all 0.2s ease-in-out;
}
.secondary-btn:hover {
    background-color: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
    color: white;
    border-color: rgba(255,255,255,0.4);
}

.tickers {
    margin-top: 3.5rem;
    text-align: center;
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: 2px;
    color: #26a69a;
}
.tickers span.down {
    color: #ef5350;
    margin-left: 1.5rem;
}

.services-wrapper {
    background-color: #0f172a;
    padding: 5rem 15% 6rem 15%;
    width: 100%;
    margin-top: 4rem;
    border-radius: 40px 40px 0 0; 
    border-top: 1px solid #1e293b;
    box-shadow: 0 -10px 40px rgba(0,0,0,0.2);
}
.services-label {
    color: #26a69a;
    font-weight: 800;
    font-size: 0.85rem;
    letter-spacing: 2px;
    margin-bottom: 1rem;
    text-transform: uppercase;
}
.services-title {
    color: #f8fafc;
    font-size: 2.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
    line-height: 1.3;
}
.services-desc {
    color: #94a3b8;
    font-size: 1.1rem;
    margin-bottom: 4rem;
}

.cards-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2.5rem;
}
.service-card {
    background-color: #1e293b;
    border-radius: 16px;
    padding: 3rem;
    box-shadow: 0px 10px 40px rgba(0,0,0,0.3); 
    border: 1px solid #334155;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.service-card:hover {
    transform: translateY(-8px);
    box-shadow: 0px 20px 50px rgba(0,0,0,0.4);
}
.card-green { border-top: 4px solid #26a69a; }
.card-dark { border-top: 4px solid #3b82f6; }

.service-card-icon {
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
}
.service-card-title {
    font-weight: 800;
    font-size: 1.5rem;
    color: #f8fafc;
    margin-bottom: 1rem;
}
.service-card-text {
    color: #cbd5e1;
    font-size: 1rem;
    line-height: 1.7;
}
</style>

<div class="hero-container">
<div class="hero-title">Decoding Market Data for<br>Smarter Decisions.</div>
<div class="hero-subtitle">Transforming Data Chaos into Harmony.</div>
</div>

<div class="btn-container">
<a href="/stock_prediction" target="_self" class="primary-btn">Stock Prediction</a>
<a href="/stock_Analysis" target="_self" class="secondary-btn">Stock Analysis</a>
</div>

<div class="tickers">
NASDAQ +1.24% <span class="down">S&P 500 -0.85%</span>
</div>

<div class="services-wrapper">
<div class="services-label">OUR SERVICES</div>
<div class="services-title">A small toolkit to explore stock data and<br>predictions.</div>
<div class="services-desc">We provide the following services:</div>

<div class="cards-grid">
<div class="service-card card-green">
<div class="service-card-icon">📊</div>
<div class="service-card-title">Stock Information</div>
<div class="service-card-text">Detailed fundamentals and charts providing a comprehensive view of historical performance and current standing.</div>
</div>
<div class="service-card card-dark">
<div class="service-card-icon">📡</div>
<div class="service-card-title">Stock Prediction</div>
<div class="service-card-text">Baseline and advanced model forecasts leveraging structural data to anticipate future market movements.</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()




