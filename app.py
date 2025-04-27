# -*- coding: utf-8 -*-
"""
Implied Volatility Analiz Aracı (Streamlit Arayüzü)

Bu uygulama, opsiyon verilerinin analizini yaparak piyasa hissiyatını ve implied volatility gibi metrikleri görsel ve açıklamalı şekilde sunar.
"""

import pandas as pd
import streamlit as st
from data_fetcher import get_options_data, get_historical_iv
from analysis import (
    calculate_put_call_ratio, 
    calculate_sentiment_score, 
    add_greeks_to_options_data
)
from visualization import (
    plot_volatility_smile,
    plot_open_interest,
    plot_volume,
    plot_3d_puts_implied_volatility,
    plot_3d_calls_implied_volatility,
    plot_historical_iv,
    plot_greeks,
    plot_future_iv_predictions
)
from interpretation import (
    interpret_volatility_smile,
    interpret_open_interest,
    interpret_volume,
    interpret_3d_puts_implied_volatility,
    interpret_3d_calls_implied_volatility,
    interpret_historical_iv,
    interpret_put_call_ratio,
    interpret_greeks,
    interpret_sentiment_score,
    overall_interpretation,
    interpret_future_iv_predictions
)
from utils import calculate_highest_iv_calls, calculate_lowest_iv_puts
from ml_models import train_iv_prediction_model, predict_future_iv
from datetime import datetime

st.set_page_config(page_title="Implied Volatility Analizi", layout="wide", page_icon="📈")
st.title("📈 Implied Volatility Analiz Aracı")
st.markdown("""
Bu uygulama, seçtiğiniz hisse senedinin opsiyon verilerini analiz ederek implied volatility, open interest, işlem hacmi, put/call oranı, grekler ve piyasa hissiyatı gibi önemli metrikleri **görsel ve açıklamalı** olarak sunar.
""")

with st.sidebar:
    st.header("Ayarlar")
    ticker = st.text_input("Sembol (ör. AAPL, TSLA)", value="AAPL")
    analyze_btn = st.button("Analizi Başlat")

if analyze_btn:

    options_data, recent_price = get_options_data(ticker)
    if options_data is None:
        st.error(f"{ticker} için geçerli opsiyon verisi bulunamadı.")
    else:
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs([
            "Volatilite Smile",
            "Açık Pozisyon",
            "İşlem Hacmi",
            "IV Yüzeyi",
            "Tarihsel IV",
            "Put/Call Oranı",
            "Grekler",
            "Hissiyat Skoru",
            "En Yüksek/En Düşük IV",
            "IV Tahmini (ML)",
            "Genel Yorum"
        ])

        with tab1:
            st.subheader("Volatilite Smile")
            iv_results = plot_volatility_smile(options_data, recent_price, ticker)
            st.plotly_chart(iv_results[0], use_container_width=True)
            yorum = interpret_volatility_smile(ticker, iv_results[1], iv_results[2], iv_results[3], iv_results[4])
            st.markdown(f"**Yorum:** {yorum}")

        with tab2:
            st.subheader("Açık Pozisyon (Open Interest)")
            oi_results = plot_open_interest(options_data, recent_price, ticker)
            st.plotly_chart(oi_results[0], use_container_width=True)
            yorum = interpret_open_interest(ticker, oi_results[1], oi_results[2], oi_results[3], oi_results[4])
            st.markdown(f"**Yorum:** {yorum}")

        with tab3:
            st.subheader("İşlem Hacmi (Volume)")
            vol_results = plot_volume(options_data, recent_price, ticker)
            st.plotly_chart(vol_results[0], use_container_width=True)
            yorum = interpret_volume(ticker, vol_results[1], vol_results[2], vol_results[3], vol_results[4])
            st.markdown(f"**Yorum:** {yorum}")

        with tab4:
            st.subheader("IV Yüzeyi (3D Volatilite)")
            puts_data = plot_3d_puts_implied_volatility(options_data, ticker)
            calls_data = plot_3d_calls_implied_volatility(options_data, ticker)
            st.plotly_chart(puts_data[0], use_container_width=True)
            st.plotly_chart(calls_data[0], use_container_width=True)
            yorum_put = interpret_3d_puts_implied_volatility(ticker, puts_data[1])
            yorum_call = interpret_3d_calls_implied_volatility(ticker, calls_data[1])
            st.markdown(f"**Put Yorum:** {yorum_put}")
            st.markdown(f"**Call Yorum:** {yorum_call}")

        with tab5:
            st.subheader("Tarihsel Implied Volatility")
            start_date = "2020-01-01"
            end_date = datetime.now().strftime("%Y-%m-%d")
            historical_iv = get_historical_iv(ticker, start_date, end_date)
            hist_results = plot_historical_iv(ticker, historical_iv)
            st.plotly_chart(hist_results[0], use_container_width=True)
            yorum = interpret_historical_iv(ticker, hist_results[1], hist_results[2])
            st.markdown(f"**Yorum:** {yorum}")

        with tab6:
            st.subheader("Put/Call Oranı")
            ratio_results = calculate_put_call_ratio(options_data)
            st.metric("Put/Call Oranı", f"{ratio_results[2]:.2f}")
            yorum = interpret_put_call_ratio(ticker, *ratio_results)
            st.markdown(f"**Yorum:** {yorum}")

        with tab7:
            st.subheader("Grekler Analizi")
            calls_with_greeks, puts_with_greeks = add_greeks_to_options_data(options_data, recent_price)
            st.plotly_chart(plot_greeks(calls_with_greeks, puts_with_greeks, recent_price, ticker), use_container_width=True)
            greeks_results = interpret_greeks(ticker, calls_with_greeks, puts_with_greeks)
            st.markdown(f"**Yorum:** {greeks_results[0]}")

        with tab8:
            st.subheader("Piyasa Hissiyatı (Sentiment Skoru)")
            high_iv_calls = calculate_highest_iv_calls(calls_data[1])
            low_iv_puts = calculate_lowest_iv_puts(puts_data[1])
            total_puts, total_calls, _ = ratio_results
            sentiment_results = calculate_sentiment_score(options_data, high_iv_calls, low_iv_puts, total_calls, total_puts)
            yorum = interpret_sentiment_score(ticker, *sentiment_results, high_iv_calls, low_iv_puts, total_calls, total_puts)
            st.metric("Hissiyat Skoru", f"{sentiment_results[0]:.2f}")
            st.markdown(f"**Yorum:** {yorum}")

        with tab9:
            st.subheader("En Yüksek IV'li Call'lar ve En Düşük IV'li Put'lar")
            st.write("**En Yüksek IV'li Call Opsiyonları:**")
            st.metric("En Yüksek Call IV Değeri", f"{high_iv_calls:.2f}%")
            
            if isinstance(calls_data[1], pd.DataFrame) and not calls_data[1].empty:
                top_calls = calls_data[1].sort_values(by='implied_volatility', ascending=False).head(5)
                st.dataframe(top_calls)
            
            st.write("**En Düşük IV'li Put Opsiyonları:**")
            st.metric("En Düşük Put IV Değeri", f"{low_iv_puts:.2f}%")
            
            if isinstance(puts_data[1], pd.DataFrame) and not puts_data[1].empty:
                bottom_puts = puts_data[1].sort_values(by='implied_volatility', ascending=True).head(5)
                st.dataframe(bottom_puts)
            
        with tab10:
            st.subheader("Implied Volatility Tahmini (ML)")
            
            historical_iv = hist_results[1]
            
            window_size = 10
            days_to_predict = 5
            
            with st.spinner("ML modeli eğitiliyor..."):
                model, scaler, feature_columns = train_iv_prediction_model(historical_iv, window_size=window_size)
            
            if model is not None:
                with st.spinner("Gelecek IV değerleri tahmin ediliyor..."):
                    predictions_df = predict_future_iv(model, scaler, historical_iv, days_to_predict=days_to_predict, window_size=window_size)
                
                st.plotly_chart(plot_future_iv_predictions(ticker, historical_iv, predictions_df), use_container_width=True)
                
                yorum = interpret_future_iv_predictions(ticker, historical_iv, predictions_df)
                st.markdown(f"**Yorum:** {yorum}")
                
                st.write("**Tahmin Edilen IV Değerleri:**")
                st.dataframe(predictions_df)
            else:
                st.error("ML modeli eğitilemedi. Yeterli tarihsel veri yok.")

        
        with tab11:
            st.subheader("Genel Yorum ve Özet")
            iv_data = (iv_results[1], iv_results[2], iv_results[3], iv_results[4])
            oi_data = (oi_results[1], oi_results[2])
            vol_data = (vol_results[1], vol_results[2], vol_results[3], vol_results[4])  
            hist_data = (hist_results[1], hist_results[2])
            sentiment_data = (*sentiment_results, high_iv_calls, low_iv_puts)
            genel_yorum = overall_interpretation(
                ticker, 
                iv_data, 
                vol_data, 
                oi_data, 
                hist_data, 
                ratio_results, 
                greeks_results,  
                sentiment_data
            )
            st.markdown(f"**Genel Yorum:** {genel_yorum}")
