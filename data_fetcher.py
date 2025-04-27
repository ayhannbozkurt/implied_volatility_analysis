import yfinance as yf
import pandas as pd

def get_options_data(ticker):
    """Belirtilen sembol için opsiyon verilerini getirir."""
    asset = yf.Ticker(ticker)
    exp_dates = asset.options

    if not exp_dates:
        print(f"{ticker} sembolü için opsiyon verisi bulunamadı.")
        return None, None

    recent_price = asset.history(period="1d")["Close"].iloc[-1]

    options_data = []
    for date in exp_dates:
        calls = asset.option_chain(date).calls
        puts = asset.option_chain(date).puts
        calls["expiration"] = date
        puts["expiration"] = date
        calls["type"] = "call"
        puts["type"] = "put"
        data = pd.concat([calls, puts])
        options_data.append(data)

    if not options_data:
        print(f"{ticker} sembolü için geçerli opsiyon verisi bulunamadı.")
        return None, None

    options_data = pd.concat(options_data)
    options_data = options_data[options_data["strike"].between(recent_price * 0.9, recent_price * 1.1)]
    options_data["implied_volatility"] = options_data["impliedVolatility"] * 100

    return options_data, recent_price


def get_historical_iv(ticker, start_date, end_date):
    """Tarihsel hisse senedi verilerini indirir ve yaklaşık IV hesaplar."""
    hist_data = yf.download(ticker, start=start_date, end=end_date)
    
    # Yüksek ve düşük fiyatlar arasındaki yüzde fark olarak tarihsel implied volatility hesapla
    hist_data['IV'] = (hist_data['High'] - hist_data['Low']) / hist_data['Low'] * 100
    
    return hist_data