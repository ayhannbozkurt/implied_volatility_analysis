import pandas as pd
import numpy as np
from py_vollib.black_scholes.greeks import analytical

def calculate_put_call_ratio(options_data):
    """Calculate the Put/Call ratio from options data."""
    if options_data is None:
        return None, None, None
        
    calls_data = options_data[options_data["type"] == "call"]
    puts_data = options_data[options_data["type"] == "put"]

    total_puts = puts_data['volume'].sum()
    total_calls = calls_data['volume'].sum()
    
    if total_calls == 0:
        print("Warning: Total calls volume is zero. Cannot calculate put/call ratio.")
        return total_puts, total_calls, float('inf')
        
    put_call_ratio = total_puts / total_calls

    return total_puts, total_calls, put_call_ratio


def calculate_sentiment_score(options_data, high_iv_calls, low_iv_puts, total_calls, total_puts):
    """Calculate a sentiment score based on IV and volume data."""
    if options_data is None or total_calls + total_puts == 0:
        return None, None
        
    # Calculate sentiment score
    sentiment_score = (high_iv_calls - low_iv_puts) + (total_calls - total_puts) / (total_calls + total_puts)
    sentiment_description = "Bullish" if sentiment_score > 0 else "Bearish"

    return sentiment_score, sentiment_description


def calculate_greeks(option_type, S, K, T, r, sigma):
    """Calculate option Greeks using the Black-Scholes model."""
    greeks = {}
    try:
        # Set flag based on option type
        flag = "c" if option_type == "call" else "p"

        # Calculate the Greeks using the analytical methods
        greeks['delta'] = analytical.delta(flag, S, K, T, r, sigma)
        greeks['gamma'] = analytical.gamma(flag, S, K, T, r, sigma)
        greeks['theta'] = analytical.theta(flag, S, K, T, r, sigma)
        greeks['vega'] = analytical.vega(flag, S, K, T, r, sigma)

    except Exception as e:
        # Assign NaN if any error occurs
        greeks = {'delta': np.nan, 'gamma': np.nan, 'theta': np.nan, 'vega': np.nan}

    return greeks


def add_greeks_to_options_data(options_data, recent_price, risk_free_rate=0.01):
    """Add Greeks calculations to options data."""
    if options_data is None:
        return None, None
        
    calls_data = options_data[options_data["type"] == "call"].copy()
    puts_data = options_data[options_data["type"] == "put"].copy()

    for index, row in calls_data.iterrows():
        T = (pd.to_datetime(row['expiration']) - pd.Timestamp.now()).days / 365.25
        if T > 0 and row['impliedVolatility'] > 0:
            greeks = calculate_greeks("call", recent_price, row['strike'], T, risk_free_rate, row['impliedVolatility'])
        else:
            greeks = {'delta': np.nan, 'gamma': np.nan, 'theta': np.nan, 'vega': np.nan}
        for greek, value in greeks.items():
            calls_data.at[index, greek] = value

    for index, row in puts_data.iterrows():
        T = (pd.to_datetime(row['expiration']) - pd.Timestamp.now()).days / 365.25
        if T > 0 and row['impliedVolatility'] > 0:
            greeks = calculate_greeks("put", recent_price, row['strike'], T, risk_free_rate, row['impliedVolatility'])
        else:
            greeks = {'delta': np.nan, 'gamma': np.nan, 'theta': np.nan, 'vega': np.nan}
        for greek, value in greeks.items():
            puts_data.at[index, greek] = value

    return calls_data, puts_data 