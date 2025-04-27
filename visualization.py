import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime

def plot_volatility_smile(options_data, recent_price, ticker):
    """Volatilite gülümsemesini çağırır ve put opsiyonları için çizdirir."""
    if options_data is None:
        return None, None, None, None, None
        
    calls_data = options_data[options_data["type"] == "call"]
    puts_data = options_data[options_data["type"] == "put"]

    expirations = options_data['expiration'].unique()
    color_map_2d = px.colors.qualitative.Prism

    fig = make_subplots(rows=1, cols=2, subplot_titles=["Call Opsiyonları", "Put Opsiyonları"], shared_yaxes=True)

    for exp, color in zip(expirations, color_map_2d):
        exp_calls = calls_data[calls_data["expiration"] == exp]
        exp_puts = puts_data[puts_data["expiration"] == exp]

        fig.add_trace(go.Scatter(x=exp_calls["strike"], y=exp_calls["implied_volatility"], mode='markers',
                                 marker=dict(color=color), name=exp), row=1, col=1)
        fig.add_trace(go.Scatter(x=exp_puts["strike"], y=exp_puts["implied_volatility"], mode='markers',
                                 marker=dict(color=color), name=exp, showlegend=False), row=1, col=2)

    avg_iv_by_strike_calls = calls_data.groupby("strike")["implied_volatility"].mean()
    avg_iv_by_strike_puts = puts_data.groupby("strike")["implied_volatility"].mean()

    fig.add_trace(go.Scatter(x=avg_iv_by_strike_calls.index, y=avg_iv_by_strike_calls.values, mode='lines',
                             line=dict(color='black', dash='dash'), name='Ortalama IV (Call)'), row=1, col=1)
    fig.add_trace(go.Scatter(x=avg_iv_by_strike_puts.index, y=avg_iv_by_strike_puts.values, mode='lines',
                             line=dict(color='black', dash='dash'), name='Ortalama IV (Put)', showlegend=False), row=1, col=2)

    overall_avg_iv_calls = calls_data["implied_volatility"].mean()
    overall_avg_iv_puts = puts_data["implied_volatility"].mean()

    fig.add_hline(y=overall_avg_iv_calls, line=dict(color='gray', dash='dash'),
                  annotation_text=f"Genel Ort. IV (Call): {overall_avg_iv_calls:.2f}%",
                  row=1, col=1)
    fig.add_hline(y=overall_avg_iv_puts, line=dict(color='gray', dash='dash'),
                  annotation_text=f"Genel Ort. IV (Put): {overall_avg_iv_puts:.2f}%",
                  row=1, col=2)

    fig.update_layout(title=f"{ticker} Volatilite Smile - Güncel Fiyat: {recent_price:.2f}", 
                     showlegend=True, legend_title_text='Vade Tarihi')
    fig.update_xaxes(title_text="Kullanım Fiyatı")
    fig.update_yaxes(title_text="İmplied Volatilite (%)")

    return fig, overall_avg_iv_calls, overall_avg_iv_puts, avg_iv_by_strike_calls, avg_iv_by_strike_puts

def plot_open_interest(options_data, recent_price, ticker):
    """Açık pozisyonları çağırır ve put opsiyonları için çizdirir."""
    if options_data is None:
        return None, None, None, None
        
    calls_data = options_data[options_data["type"] == "call"]
    puts_data = options_data[options_data["type"] == "put"]

    expirations = options_data['expiration'].unique()
    color_map_2d = px.colors.qualitative.Prism

    fig = make_subplots(rows=1, cols=2, subplot_titles=["Call Açık Pozisyon", "Put Açık Pozisyon"], shared_yaxes=True)

    for exp, color in zip(expirations, color_map_2d):
        exp_calls = calls_data[calls_data["expiration"] == exp]
        exp_puts = puts_data[puts_data["expiration"] == exp]

        fig.add_trace(go.Scatter(x=exp_calls["strike"], y=exp_calls["openInterest"], mode='markers',
                                 marker=dict(color=color), name=exp), row=1, col=1)
        fig.add_trace(go.Scatter(x=exp_puts["strike"], y=exp_puts["openInterest"], mode='markers',
                                 marker=dict(color=color), name=exp, showlegend=False), row=1, col=2)

    overall_avg_oi_calls = calls_data["openInterest"].mean()
    overall_avg_oi_puts = puts_data["openInterest"].mean()

    fig.update_layout(title=f"{ticker} Kullanım Fiyatına Göre Açık Pozisyon - Güncel Fiyat: {recent_price:.2f}", 
                     showlegend=True, legend_title_text='Vade Tarihi')
    fig.update_xaxes(title_text="Kullanım Fiyatı")
    fig.update_yaxes(title_text="Açık Pozisyon")

    return fig, overall_avg_oi_calls, overall_avg_oi_puts, calls_data, puts_data

def plot_volume(options_data, recent_price, ticker):
    """Hacimleri çağırır ve put opsiyonları için çizdirir."""
    if options_data is None:
        return None, None, None, None
        
    calls_data = options_data[options_data["type"] == "call"]
    puts_data = options_data[options_data["type"] == "put"]

    expirations = options_data['expiration'].unique()
    color_map_2d = px.colors.qualitative.Prism

    fig = make_subplots(rows=1, cols=2, subplot_titles=["Call İşlem Hacmi", "Put İşlem Hacmi"], shared_yaxes=True)

    for exp, color in zip(expirations, color_map_2d):
        exp_calls = calls_data[calls_data["expiration"] == exp]
        exp_puts = puts_data[puts_data["expiration"] == exp]

        fig.add_trace(go.Scatter(x=exp_calls["strike"], y=exp_calls["volume"], mode='markers',
                                 marker=dict(color=color), name=exp), row=1, col=1)
        fig.add_trace(go.Scatter(x=exp_puts["strike"], y=exp_puts["volume"], mode='markers',
                                 marker=dict(color=color), name=exp, showlegend=False), row=1, col=2)

    overall_avg_vol_calls = calls_data["volume"].mean()
    overall_avg_vol_puts = puts_data["volume"].mean()

    fig.update_layout(title=f"{ticker} Kullanım Fiyatına Göre İşlem Hacmi - Güncel Fiyat: {recent_price:.2f}", 
                     showlegend=True, legend_title_text='Vade Tarihi')
    fig.update_xaxes(title_text="Kullanım Fiyatı")
    fig.update_yaxes(title_text="İşlem Hacmi")

    return fig, overall_avg_vol_calls, overall_avg_vol_puts, calls_data, puts_data

def plot_3d_puts_implied_volatility(options_data, ticker):
    """3D yüzeyi çağırır ve put opsiyonları için çizdirir."""
    if options_data is None:
        return None
        
    puts_data = options_data[options_data["type"] == "put"]
    expirations = options_data['expiration'].unique()
    color_map_3d = {exp: color for exp, color in zip(expirations, px.colors.qualitative.Prism)}

    fig = px.scatter_3d(puts_data, x='strike', y='expiration', z='implied_volatility',
                         color='expiration', color_discrete_map=color_map_3d,
                         title=f'{ticker} Put Opsiyonları İmplied Volatilite',
                         labels={'strike': 'Kullanım Fiyatı', 'expiration': 'Vade Tarihi', 
                                'implied_volatility': 'İmplied Volatilite (%)'},
                         hover_name='expiration')

    return fig, puts_data

def plot_3d_calls_implied_volatility(options_data, ticker):
    """3D yüzeyi çağırır ve call opsiyonları için çizdirir."""
    if options_data is None:
        return None
        
    calls_data = options_data[options_data["type"] == "call"]
    expirations = options_data['expiration'].unique()
    color_map_3d = {exp: color for exp, color in zip(expirations, px.colors.qualitative.Prism)}

    fig = px.scatter_3d(calls_data, x='strike', y='expiration', z='implied_volatility',
                         color='expiration', color_discrete_map=color_map_3d,
                         title=f'{ticker} Call Opsiyonları İmplied Volatilite',
                         labels={'strike': 'Kullanım Fiyatı', 'expiration': 'Vade Tarihi', 
                                'implied_volatility': 'İmplied Volatilite (%)'},
                         hover_name='expiration')

    return fig, calls_data

def plot_historical_iv(ticker, historical_iv):
    """Tarihsel implied volatility grafiğini çizdirir.
    
    Args:
        ticker (str): Hisse senedi sembolü
        historical_iv (pd.DataFrame): Tarihsel implied volatility verileri
        
    Returns:
        tuple: (fig, historical_iv, current_iv) - Grafik, tarihsel veri ve güncel IV değeri
    """
    if historical_iv is None or historical_iv.empty:
        return None, None, None
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=historical_iv.index, y=historical_iv['IV'], mode='lines', name='Tarihsel IV'))

    current_iv = historical_iv['IV'].iloc[-1]
    fig.add_trace(go.Scatter(x=[historical_iv.index[-1]], y=[current_iv], mode='markers', name='Güncel IV',
                             marker=dict(color='red', size=10)))

    fig.update_layout(
        title=f"{ticker} Tarihsel İmplied Volatilite",
        xaxis_title="Tarih",
        yaxis_title="İmplied Volatilite (%)",
        legend_title="Açıklama"
    )

    return fig, historical_iv, current_iv

def plot_greeks(calls_data, puts_data, recent_price, ticker):
    """Greeks grafiğini çağırır."""
    if calls_data is None or puts_data is None:
        return None
        
    fig = make_subplots(rows=2, cols=2, subplot_titles=["Delta", "Gamma", "Theta", "Vega"], shared_yaxes=True)

    fig.add_trace(go.Scatter(x=calls_data["strike"], y=calls_data["delta"], mode='markers', 
                            marker=dict(color='blue'), name="Delta (Call)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=puts_data["strike"], y=puts_data["delta"], mode='markers', 
                            marker=dict(color='red'), name="Delta (Put)"), row=1, col=1)

    fig.add_trace(go.Scatter(x=calls_data["strike"], y=calls_data["gamma"], mode='markers', 
                            marker=dict(color='blue'), name="Gamma (Call)"), row=1, col=2)
    fig.add_trace(go.Scatter(x=puts_data["strike"], y=puts_data["gamma"], mode='markers', 
                            marker=dict(color='red'), name="Gamma (Put)"), row=1, col=2)

    fig.add_trace(go.Scatter(x=calls_data["strike"], y=calls_data["theta"], mode='markers', 
                            marker=dict(color='blue'), name="Theta (Call)"), row=2, col=1)
    fig.add_trace(go.Scatter(x=puts_data["strike"], y=puts_data["theta"], mode='markers', 
                            marker=dict(color='red'), name="Theta (Put)"), row=2, col=1)
    fig.add_trace(go.Scatter(x=calls_data["strike"], y=calls_data["vega"], mode='markers', 
                            marker=dict(color='blue'), name="Vega (Call)"), row=2, col=2)
    fig.add_trace(go.Scatter(x=puts_data["strike"], y=puts_data["vega"], mode='markers', 
                            marker=dict(color='red'), name="Vega (Put)"), row=2, col=2)

    fig.update_layout(title=f"{ticker} Opsiyonları Greeks by Strike - Güncel Fiyat: {recent_price:.2f}", 
                     showlegend=True, legend_title_text='Opsiyon Türü')
    fig.update_xaxes(title_text="Kullanım Fiyatı")
    fig.update_yaxes(title_text="Greeks Değeri")

    return fig

def plot_future_iv_predictions(ticker, historical_iv, predictions_df):
    """İmplied volatility tahmini grafiğini çağırır."""
    if historical_iv is None or predictions_df is None:
        return None
        
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=historical_iv.index[-30:],  # Son 30 günlük veri
        y=historical_iv['IV'].iloc[-30:],
        mode='lines',
        name='Geçmiş IV',
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=predictions_df.index,
        y=predictions_df['Predicted_IV'],
        mode='lines+markers',
        name='Tahmin Edilen IV',
        line=dict(color='red', dash='dash'),
        marker=dict(size=8)
    ))

    current_iv = historical_iv['IV'].iloc[-1]
    fig.add_trace(go.Scatter(
        x=[historical_iv.index[-1]],
        y=[current_iv],
        mode='markers',
        name='Güncel IV',
        marker=dict(color='green', size=12, symbol='star')
    ))

    fig.update_layout(
        title=f"{ticker} İmplied Volatilite Tahmini",
        xaxis_title="Tarih",
        yaxis_title="İmplied Volatilite (%)",
        legend_title="Veri Türü",
        hovermode="x unified"
    )

    return fig