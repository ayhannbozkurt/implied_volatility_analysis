# Implied Volatility Analysis

A sophisticated tool for analyzing market sentiment through options implied volatility and related metrics.

## Overview

This application provides comprehensive market sentiment analysis by examining options data through multiple dimensions:

- Volatility smile for call and put options
- Open interest patterns
- Trading volume analysis
- 3D volatility surfaces
- Historical implied volatility trends
- Put/Call ratio analysis
- Options Greeks (Delta, Gamma, Theta, Vega)
- Overall sentiment scoring
- Machine learning-based future implied volatility predictions

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To launch the Streamlit interface:

```bash
streamlit run app.py
```

Enter the ticker symbol you wish to analyze (e.g., AAPL, TSLA) in the interface and click "Start Analysis" to run the analysis.

## Project Structure

- `app.py` - Streamlit interface and main application
- `data_fetcher.py` - Functions for retrieving options and historical data
- `analysis.py` - Data analysis and calculations (Put/Call ratio, sentiment score, Greeks)
- `visualization.py` - Data visualization functions (Plotly charts)
- `interpretation.py` - Functions for interpreting analysis results
- `utils.py` - Helper functions and data formatting utilities
- `ml_models.py` - Machine learning models and future IV predictions

## Features

### Volatility Smile Analysis
Visualizes and interprets implied volatility patterns across different strike prices.

### Open Interest and Volume Analysis
Analyzes the distribution of open interest and trading volume in options contracts.

### 3D Volatility Surface
Provides three-dimensional visualization of implied volatility distribution by strike price and expiration date.

### Historical IV Analysis
Displays and interprets historical implied volatility trends.

### Put/Call Ratio
Calculates the volume ratio between put and call options to evaluate market sentiment.

### Greeks Analysis
Calculates and visualizes Delta, Gamma, Theta, and Vega values.

### Sentiment Score
Generates an overall market sentiment score based on various metrics.

### Machine Learning Predictions
Uses LightGBM model to predict future implied volatility values.

## Requirements

- Python 3.6 or higher
- Streamlit
- Pandas
- NumPy
- Plotly
- yfinance
- py_vollib
- LightGBM
- scikit-learn
