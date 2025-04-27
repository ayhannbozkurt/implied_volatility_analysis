import pandas as pd

def interpret_volatility_smile(ticker, overall_avg_iv_calls, overall_avg_iv_puts, avg_iv_by_strike_calls, avg_iv_by_strike_puts):
    """Volatilite smile verilerini yorumlar."""
    if overall_avg_iv_calls is None or overall_avg_iv_puts is None:
        return None
        
    interpretation = f"**{ticker} Volatilite Smile Yorumu:**\n"

    interpretation += f"- Call opsiyonları için ortalama implied volatilite %{overall_avg_iv_calls:.2f}.\n"
    interpretation += f"- Put opsiyonları için ortalama implied volatilite %{overall_avg_iv_puts:.2f}.\n"

    if avg_iv_by_strike_calls.var() > 0.1:
        interpretation += "- Call opsiyonları belirgin bir 'volatilite smile' gösteriyor, bu da farklı kullanım fiyatlarında değişen implied volatilite olduğunu gösterir.\n"
    else:
        interpretation += "- Call opsiyonları belirgin bir 'volatilite smile' göstermiyor, bu da kullanım fiyatları arasında daha istikrarlı bir implied volatilite olduğunu gösterir.\n"

    if avg_iv_by_strike_puts.var() > 0.1:
        interpretation += "- Put opsiyonları belirgin bir 'volatilite smile' gösteriyor, bu da farklı kullanım fiyatlarında değişen implied volatilite olduğunu gösterir.\n"
    else:
        interpretation += "- Put opsiyonları belirgin bir 'volatilite smile' göstermiyor, bu da kullanım fiyatları arasında daha istikrarlı bir implied volatilite olduğunu gösterir.\n"

    market_sentiment = "yükseliş eğilimli" if overall_avg_iv_calls > overall_avg_iv_puts else "düşüş eğilimli"
    interpretation += f"- Genel piyasa hissiyatı {market_sentiment}, bu call ve put opsiyonlarının ortalama implied volatilitesinden çıkarılmıştır.\n"

    if overall_avg_iv_calls > overall_avg_iv_puts:
        interpretation += "- Call opsiyonlarındaki daha yüksek implied volatilite, yatırımcıların yukarı yönlü fiyat hareketleri veya hisse senedi fiyatında daha yüksek belirsizlik beklediğini gösterir.\n"
    else:
        interpretation += "- Put opsiyonlarındaki daha yüksek implied volatilite, yatırımcıların aşağı yönlü fiyat hareketleri veya hisse senedi fiyatında daha yüksek belirsizlik beklediğini gösterir.\n"

    return interpretation


def interpret_open_interest(ticker, overall_avg_oi_calls, overall_avg_oi_puts, calls_data, puts_data):
    """Açık pozisyon verilerini yorumlar."""
    if overall_avg_oi_calls is None or overall_avg_oi_puts is None:
        return None
        
    interpretation = f"**{ticker} Açık Pozisyon Yorumu:**\n"

    interpretation += f"- Call opsiyonları için ortalama açık pozisyon {overall_avg_oi_calls:.2f} kontrat.\n"
    interpretation += f"- Put opsiyonları için ortalama açık pozisyon {overall_avg_oi_puts:.2f} kontrat.\n"

    if overall_avg_oi_calls > overall_avg_oi_puts:
        interpretation += "- Call opsiyonlarında daha yüksek ortalama açık pozisyon var, bu da call'larda daha yüksek işlem aktivitesi ve ilgi olduğunu gösterir.\n"
    else:
        interpretation += "- Put opsiyonlarında daha yüksek ortalama açık pozisyon var, bu da put'larda daha yüksek işlem aktivitesi ve ilgi olduğunu gösterir.\n"

    highest_oi_call = calls_data.loc[calls_data['openInterest'].idxmax()]
    highest_oi_put = puts_data.loc[puts_data['openInterest'].idxmax()]

    interpretation += f"- Call'lar için en yüksek açık pozisyona sahip kullanım fiyatı {highest_oi_call['strike']} ile {highest_oi_call['openInterest']} kontrat.\n"
    interpretation += f"- Put'lar için en yüksek açık pozisyona sahip kullanım fiyatı {highest_oi_put['strike']} ile {highest_oi_put['openInterest']} kontrat.\n"

    if overall_avg_oi_calls > overall_avg_oi_puts:
        interpretation += "- Call opsiyonlarındaki daha yüksek açık pozisyon, yatırımcıların yukarı yönlü fiyat hareketleri beklediğini gösterebilir.\n"
    else:
        interpretation += "- Put opsiyonlarındaki daha yüksek açık pozisyon, yatırımcıların aşağı yönlü fiyat hareketleri beklediğini gösterebilir.\n"

    return interpretation


def interpret_volume(ticker, overall_avg_vol_calls, overall_avg_vol_puts, calls_data, puts_data):
    """İşlem hacmi verilerini yorumlar."""
    if overall_avg_vol_calls is None or overall_avg_vol_puts is None:
        return None
        
    interpretation = f"**{ticker} İşlem Hacmi Analizi Yorumu:**\n"

    interpretation += f"- Call opsiyonları için ortalama işlem hacmi {overall_avg_vol_calls:.2f} kontrat.\n"
    interpretation += f"- Put opsiyonları için ortalama işlem hacmi {overall_avg_vol_puts:.2f} kontrat.\n"

    if overall_avg_vol_calls > overall_avg_vol_puts:
        interpretation += "- Call opsiyonlarında daha yüksek ortalama işlem hacmi var, bu da call'larda daha yüksek işlem aktivitesi ve ilgi olduğunu gösterir.\n"
    else:
        interpretation += "- Put opsiyonlarında daha yüksek ortalama işlem hacmi var, bu da put'larda daha yüksek işlem aktivitesi ve ilgi olduğunu gösterir.\n"

    highest_vol_call = calls_data.loc[calls_data['volume'].idxmax()]
    highest_vol_put = puts_data.loc[puts_data['volume'].idxmax()]

    interpretation += f"- Call'lar için en yüksek işlem hacmine sahip kullanım fiyatı {highest_vol_call['strike']} ile {highest_vol_call['volume']} kontrat.\n"
    interpretation += f"- Put'lar için en yüksek işlem hacmine sahip kullanım fiyatı {highest_vol_put['strike']} ile {highest_vol_put['volume']} kontrat.\n"

    if overall_avg_vol_calls > overall_avg_vol_puts:
        interpretation += "- Call opsiyonlarındaki daha yüksek işlem hacmi, yatırımcıların call'ları daha aktif olarak işlem yaptığını ve muhtemelen yukarı yönlü fiyat hareketleri beklediğini gösterir.\n"
    else:
        interpretation += "- Put opsiyonlarındaki daha yüksek işlem hacmi, yatırımcıların put'ları daha aktif olarak işlem yaptığını ve muhtemelen aşağı yönlü fiyat hareketleri beklediğini gösterir.\n"

    return interpretation


def interpret_3d_puts_implied_volatility(ticker, puts_data):
    """3D put opsiyonları implied volatilite verilerini yorumlar."""
    if puts_data is None:
        return None
        
    interpretation = f"**{ticker} Put Opsiyonları İmplied Volatilite (3D Grafik) Yorumu:**\n"

    overall_avg_iv_puts = puts_data["implied_volatility"].mean()
    interpretation += f"- Put opsiyonları için ortalama implied volatilite %{overall_avg_iv_puts:.2f}.\n"

    highest_iv_put_idx = puts_data['implied_volatility'].idxmax()
    highest_iv_put = puts_data.loc[highest_iv_put_idx]
    if isinstance(highest_iv_put, pd.Series):
        strike_price = highest_iv_put['strike']
        implied_volatility = highest_iv_put['implied_volatility']
        expiration_date = highest_iv_put['expiration']
    else:
        strike_price = highest_iv_put.iloc[0]['strike']
        implied_volatility = highest_iv_put.iloc[0]['implied_volatility']
        expiration_date = highest_iv_put.iloc[0]['expiration']

    interpretation += f"- Put'lar için en yüksek implied volatiliteye sahip kullanım fiyatı {strike_price} ile %{implied_volatility:.2f} implied volatilite, vade tarihi {expiration_date}.\n"

    interpretation += "\n**Vade Tarihlerine Göre İmplied Volatilite:**\n"
    for exp in puts_data['expiration'].unique():
        exp_data = puts_data[puts_data['expiration'] == exp]
        avg_iv_exp = exp_data['implied_volatility'].mean()
        interpretation += f"- {exp} tarihinde sona eren put'lar için ortalama IV: %{avg_iv_exp:.2f}.\n"

    interpretation += "\n**Kullanım Fiyatlarına Göre İmplied Volatilite:**\n"
    strike_price_bins = pd.cut(puts_data['strike'], bins=5)
    grouped_strike_data = puts_data.groupby(strike_price_bins)['implied_volatility'].mean()
    for interval, avg_iv_strike in grouped_strike_data.items():
        interpretation += f"- {interval} aralığındaki kullanım fiyatlarına sahip put'lar için ortalama IV: %{avg_iv_strike:.2f}.\n"

    iv_variability = puts_data['implied_volatility'].std()
    if iv_variability > 10:
        interpretation += "\n**Genel Piyasa Yorumu:**\n"
        interpretation += f"- Farklı kullanım fiyatları ve vade tarihleri arasında implied volatilitede önemli bir değişkenlik var (standart sapma: %{iv_variability:.2f}).\n"
        interpretation += "- Bu değişkenlik, piyasa katılımcıları arasında farklı beklentiler olduğunu ve yüksek bir belirsizlik ortamını gösteriyor.\n"
        interpretation += "- Yüksek volatilite değişkenliği genellikle önemli bir haber, ekonomik veri açıklaması veya şirket olayı beklentisini yansıtabilir.\n"
        interpretation += "- Yatırımcılar için: Bu durumda, opsiyon pozisyonlarınızı çeşitlendirmek ve volatilite değişimlerinden faydalanabilecek stratejiler (örn. strangle, straddle) düşünmek faydalı olabilir.\n"
        interpretation += f"- {ticker} için put opsiyonlarındaki bu yüksek volatilite değişkenliği, hisse senedi fiyatında aşağı yönlü hareket beklentisini gösterebilir.\n"
    else:
        interpretation += "\n**Genel Piyasa Yorumu:**\n"
        interpretation += f"- İmplied volatilite, farklı kullanım fiyatları ve vade tarihleri arasında nispeten istikrarlı (standart sapma: %{iv_variability:.2f}).\n"
        interpretation += "- Bu istikrar, piyasa katılımcıları arasında tutarlı beklentiler olduğunu ve düşük bir belirsizlik ortamını gösteriyor.\n"
        interpretation += "- Düşük volatilite değişkenliği genellikle piyasanın mevcut fiyatlamaya güvendiğini ve yakın vadede büyük fiyat hareketleri beklenmediğini gösterir.\n"
        interpretation += "- Yatırımcılar için: Bu durumda, volatilite satışı stratejileri (örn. covered call, cash-secured put) daha uygun olabilir.\n"
        interpretation += f"- {ticker} için put opsiyonlarındaki bu istikrarlı volatilite, hisse senedi fiyatında büyük bir düşüş beklentisi olmadığını gösterebilir.\n"

    return interpretation


def interpret_3d_calls_implied_volatility(ticker, calls_data):
    """3D call opsiyonları implied volatilite verilerini yorumlar."""
    if calls_data is None:
        return None
        
    interpretation = f"**{ticker} Call Opsiyonları İmplied Volatilite (3D Grafik) Yorumu:**\n"

    overall_avg_iv_calls = calls_data["implied_volatility"].mean()
    interpretation += f"- Call opsiyonları için ortalama implied volatilite %{overall_avg_iv_calls:.2f}.\n"

    highest_iv_call_idx = calls_data['implied_volatility'].idxmax()
    highest_iv_call = calls_data.loc[highest_iv_call_idx]
    if isinstance(highest_iv_call, pd.Series):
        strike_price = highest_iv_call['strike']
        implied_volatility = highest_iv_call['implied_volatility']
        expiration_date = highest_iv_call['expiration']
    else:
        strike_price = highest_iv_call.iloc[0]['strike']
        implied_volatility = highest_iv_call.iloc[0]['implied_volatility']
        expiration_date = highest_iv_call.iloc[0]['expiration']

    interpretation += f"- Call'lar için en yüksek implied volatiliteye sahip kullanım fiyatı {strike_price} ile %{implied_volatility:.2f} implied volatilite, vade tarihi {expiration_date}.\n"

    interpretation += "\n**Vade Tarihlerine Göre İmplied Volatilite:**\n"
    for exp in calls_data['expiration'].unique():
        exp_data = calls_data[calls_data['expiration'] == exp]
        avg_iv_exp = exp_data['implied_volatility'].mean()
        interpretation += f"- {exp} tarihinde sona eren call'lar için ortalama IV: %{avg_iv_exp:.2f}.\n"

    interpretation += "\n**Kullanım Fiyatlarına Göre İmplied Volatilite:**\n"
    strike_price_bins = pd.cut(calls_data['strike'], bins=5)
    grouped_strike_data = calls_data.groupby(strike_price_bins)['implied_volatility'].mean()
    for interval, avg_iv_strike in grouped_strike_data.items():
        interpretation += f"- {interval} aralığındaki kullanım fiyatlarına sahip call'lar için ortalama IV: %{avg_iv_strike:.2f}.\n"

    iv_variability = calls_data['implied_volatility'].std()
    if iv_variability > 10:
        interpretation += "\n**Genel Piyasa Yorumu:**\n"
        interpretation += f"- Farklı kullanım fiyatları ve vade tarihleri arasında implied volatilitede önemli bir değişkenlik var (standart sapma: %{iv_variability:.2f}).\n"
        interpretation += "- Bu değişkenlik, piyasa katılımcıları arasında farklı beklentiler olduğunu ve yüksek bir belirsizlik ortamını gösteriyor.\n"
        interpretation += "- Yüksek volatilite değişkenliği genellikle önemli bir haber, ekonomik veri açıklaması veya şirket olayı beklentisini yansıtabilir.\n"
        interpretation += "- Yatırımcılar için: Bu durumda, opsiyon pozisyonlarınızı çeşitlendirmek ve volatilite değişimlerinden faydalanabilecek stratejiler (örn. strangle, straddle) düşünmek faydalı olabilir.\n"
        interpretation += f"- {ticker} için call opsiyonlarındaki bu yüksek volatilite değişkenliği, hisse senedi fiyatında yukarı yönlü hareket beklentisini gösterebilir.\n"
    else:
        interpretation += "\n**Genel Piyasa Yorumu:**\n"
        interpretation += f"- İmplied volatilite, farklı kullanım fiyatları ve vade tarihleri arasında nispeten istikrarlı (standart sapma: %{iv_variability:.2f}).\n"
        interpretation += "- Bu istikrar, piyasa katılımcıları arasında tutarlı beklentiler olduğunu ve düşük bir belirsizlik ortamını gösteriyor.\n"
        interpretation += "- Düşük volatilite değişkenliği genellikle piyasanın mevcut fiyatlamaya güvendiğini ve yakın vadede büyük fiyat hareketleri beklenmediğini gösterir.\n"
        interpretation += "- Yatırımcılar için: Bu durumda, volatilite satışı stratejileri (örn. covered call, cash-secured put) daha uygun olabilir.\n"
        interpretation += f"- {ticker} için call opsiyonlarındaki bu istikrarlı volatilite, hisse senedi fiyatında büyük bir yükseliş beklentisi olmadığını gösterebilir.\n"

    return interpretation


def interpret_historical_iv(ticker, historical_iv, current_iv):
    """Tarihsel implied volatilite verilerini yorumlar."""
    if historical_iv is None or current_iv is None:
        return None
        
    interpretation = f"**{ticker} Tarihsel İmplied Volatilite Yorumu:**\n"

    avg_iv = historical_iv["IV"].mean()
    max_iv = historical_iv["IV"].max()
    min_iv = historical_iv["IV"].min()

    interpretation += f"- Dönem boyunca ortalama implied volatilite %{avg_iv:.2f}.\n"
    interpretation += f"- Kaydedilen en yüksek implied volatilite %{max_iv:.2f}.\n"
    interpretation += f"- Kaydedilen en düşük implied volatilite %{min_iv:.2f}.\n"
    interpretation += f"- Mevcut implied volatilite %{current_iv:.2f}.\n"
    if len(historical_iv) > 30:
        recent_trend = "artmış" if historical_iv['IV'].iloc[-1] > historical_iv['IV'].iloc[-30] else "azalmış"
        interpretation += f"- Son 30 günde, implied volatilite önceki döneme göre {recent_trend}.\n"

    historical_iv['Year'] = historical_iv.index.year
    avg_iv_by_year = historical_iv.groupby('Year')['IV'].mean()
    interpretation += "\n**Yıllara Göre Ortalama İmplied Volatilite:**\n"
    for year, avg_iv in avg_iv_by_year.items():
        interpretation += f"- {year}: %{avg_iv:.2f}.\n"

    iv_variability = historical_iv['IV'].std()
    interpretation += f"\n- Dönem boyunca implied volatilitenin standart sapması %{iv_variability:.2f}, bu da implied volatilitede {'yüksek' if iv_variability > 10 else 'düşük'} değişkenlik olduğunu gösteriyor.\n"

    if len(historical_iv) > 30:
        recent_trend = "artmış" if historical_iv['IV'].iloc[-1] > historical_iv['IV'].iloc[-30] else "azalmış"
        interpretation += f"\n- Son 30 günde, implied volatilite önceki döneme göre {recent_trend}.\n"

    return interpretation


def interpret_put_call_ratio(ticker, total_puts, total_calls, put_call_ratio):
    """Put/call oranı verilerini yorumlar."""
    if total_puts is None or total_calls is None or put_call_ratio is None:
        return None
        
    interpretation = f"**{ticker} Put/Call Oranı Yorumu:**\n"

    interpretation += f"- Put/Call Oranı {put_call_ratio:.2f}.\n"

    interpretation += f"- Put'ların toplam hacmi: {total_puts}\n"
    interpretation += f"- Call'ların toplam hacmi: {total_calls}\n"

    if put_call_ratio > 1:
        interpretation += "- 1'den büyük bir Put/Call Oranı, piyasada düşüş eğilimli bir hissiyatı gösterir, çünkü call'lara göre daha fazla put işlem görüyor.\n"
    elif put_call_ratio < 1:
        interpretation += "- 1'den küçük bir Put/Call Oranı, piyasada yükseliş eğilimli bir hissiyatı gösterir, çünkü put'lara göre daha fazla call işlem görüyor.\n"
    else:
        interpretation += "- 1'e eşit bir Put/Call Oranı, piyasada nötr bir hissiyatı gösterir, put ve call'ların eşit hacimlerde işlem gördüğünü belirtir.\n"

    return interpretation


def interpret_greeks(ticker, calls_data, puts_data):
    """Greeks verilerini yorumlar."""
    if calls_data is None or puts_data is None:
        return None
        
    interpretation = f"**{ticker} Greeks Analizi Yorumu:**\n"

    avg_delta_calls = calls_data["delta"].mean()
    avg_delta_puts = puts_data["delta"].mean()
    avg_gamma_calls = calls_data["gamma"].mean()
    avg_gamma_puts = puts_data["gamma"].mean()
    avg_theta_calls = calls_data["theta"].mean()
    avg_theta_puts = puts_data["theta"].mean()
    avg_vega_calls = calls_data["vega"].mean()
    avg_vega_puts = puts_data["vega"].mean()

    interpretation += f"- Call opsiyonları için ortalama delta: {avg_delta_calls:.4f}.\n"
    interpretation += f"- Put opsiyonları için ortalama delta: {avg_delta_puts:.4f}.\n"
    interpretation += f"- Call opsiyonları için ortalama gamma: {avg_gamma_calls:.4f}.\n"
    interpretation += f"- Put opsiyonları için ortalama gamma: {avg_gamma_puts:.4f}.\n"
    interpretation += f"- Call opsiyonları için ortalama theta: {avg_theta_calls:.4f}.\n"
    interpretation += f"- Put opsiyonları için ortalama theta: {avg_theta_puts:.4f}.\n"
    interpretation += f"- Call opsiyonları için ortalama vega: {avg_vega_calls:.4f}.\n"
    interpretation += f"- Put opsiyonları için ortalama vega: {avg_vega_puts:.4f}.\n"

    interpretation += "\n**Delta Yorumu:**\n"
    interpretation += "- Delta, hisse senedi fiyatındaki değişime göre opsiyon fiyatının değişim oranını ölçer.\n"
    interpretation += f"- Call opsiyonları için pozitif delta ({avg_delta_calls:.4f}), hisse senedi fiyatı yükseldiğinde opsiyon değerinin artacağını gösterir.\n"
    interpretation += f"- Put opsiyonları için negatif delta ({avg_delta_puts:.4f}), hisse senedi fiyatı yükseldiğinde opsiyon değerinin azalacağını gösterir.\n"

    interpretation += "\n**Gamma Yorumu:**\n"
    interpretation += "- Gamma, hisse senedi fiyatındaki değişime göre deltanın değişim oranını ölçer.\n"
    interpretation += f"- Yüksek gamma ({max(avg_gamma_calls, avg_gamma_puts):.4f}), hisse senedi fiyatındaki değişimlere karşı opsiyon değerinin daha duyarlı olduğunu gösterir.\n"

    interpretation += "\n**Theta Yorumu:**\n"
    interpretation += "- Theta, zaman geçtikçe opsiyon değerindeki azalmayı ölçer (zaman değeri kaybı).\n"
    interpretation += f"- Negatif theta değerleri (call: {avg_theta_calls:.4f}, put: {avg_theta_puts:.4f}), zaman geçtikçe opsiyonların değer kaybettiğini gösterir.\n"

    interpretation += "\n**Vega Yorumu:**\n"
    interpretation += "- Vega, implied volatilitedeki değişime göre opsiyon değerindeki değişimi ölçer.\n"
    interpretation += f"- Yüksek vega değerleri (call: {avg_vega_calls:.4f}, put: {avg_vega_puts:.4f}), opsiyonların implied volatilitedeki değişimlere duyarlı olduğunu gösterir.\n"

    if abs(avg_delta_calls) > abs(avg_delta_puts):
        interpretation += "\n- Call'lar için put'lara göre daha yüksek ortalama delta, yükseliş eğilimli bir hissiyatı gösterir, çünkü call opsiyonları hisse senedi fiyatındaki yukarı yönlü hareketlere daha duyarlıdır.\n"
    else:
        interpretation += "\n- Put'lar için call'lara göre daha yüksek ortalama delta, düşüş eğilimli bir hissiyatı gösterir, çünkü put opsiyonları hisse senedi fiyatındaki aşağı yönlü hareketlere daha duyarlıdır.\n"

    return interpretation, avg_delta_calls, avg_delta_puts, avg_gamma_calls, avg_gamma_puts, avg_theta_calls, avg_theta_puts, avg_vega_calls, avg_vega_puts


def interpret_sentiment_score(ticker, sentiment_score, sentiment_description, high_iv_calls, low_iv_puts, total_calls, total_puts):
    """Hissiyat skoru verilerini yorumlar."""
    if sentiment_score is None or sentiment_description is None:
        return None
        
    interpretation = f"**{ticker} Piyasa Hissiyatı Skoru Yorumu:**\n"

    interpretation += f"- Piyasa Hissiyatı Skoru: {sentiment_score:.2f} ({sentiment_description}).\n"
    interpretation += f"- En yüksek IV'li call opsiyonları: %{high_iv_calls:.2f}.\n"
    interpretation += f"- En düşük IV'li put opsiyonları: %{low_iv_puts:.2f}.\n"
    interpretation += f"- Call/Put Hacim Oranı: {total_calls/total_puts:.2f}.\n"

    if sentiment_score > 0.6:
        interpretation += "- Yüksek bir hissiyat skoru, piyasanın güçlü bir yükseliş eğiliminde olduğunu gösterir. Yatırımcılar, hisse senedi fiyatında yukarı yönlü hareketler bekliyor olabilir.\n"
    elif sentiment_score < 0.4:
        interpretation += "- Düşük bir hissiyat skoru, piyasanın güçlü bir düşüş eğiliminde olduğunu gösterir. Yatırımcılar, hisse senedi fiyatında aşağı yönlü hareketler bekliyor olabilir.\n"
    else:
        interpretation += "- Orta düzeyde bir hissiyat skoru, piyasanın nötr veya kararsız olduğunu gösterir. Yatırımcılar, hisse senedi fiyatında belirgin bir yön beklemiyor olabilir.\n"

    if sentiment_score > 0.5:
        interpretation += "- Yükseliş eğilimli hissiyat, call'lardaki put'lara göre daha yüksek implied volatilite ve daha yüksek call hacmi ile destekleniyor.\n"
    else:
        interpretation += "- Düşüş eğilimli hissiyat, put'lardaki call'lara göre daha yüksek implied volatilite ve daha yüksek put hacmi ile destekleniyor.\n"

    return interpretation


def overall_interpretation(ticker, iv_data, vol_data, oi_data, hist_data, ratio_data, greeks_data, sentiment_data):
    """Tüm analiz sonuçlarının genel bir yorumunu oluşturur."""
    if None in [iv_data, vol_data, oi_data, hist_data, ratio_data, greeks_data, sentiment_data]:
        return "Eksik veriler nedeniyle genel yorum oluşturulamıyor."
        
    overall_avg_iv_calls, overall_avg_iv_puts, avg_iv_by_strike_calls, avg_iv_by_strike_puts = iv_data
    overall_avg_vol_calls, overall_avg_vol_puts, calls_data, puts_data = vol_data
    overall_avg_oi_calls, overall_avg_oi_puts = oi_data
    historical_iv, current_iv = hist_data
    total_puts, total_calls, put_call_ratio = ratio_data
    (_, avg_delta_calls, avg_delta_puts, avg_gamma_calls, avg_gamma_puts, 
     avg_theta_calls, avg_theta_puts, avg_vega_calls, avg_vega_puts) = greeks_data
    sentiment_score, sentiment_description, high_iv_calls, low_iv_puts = sentiment_data
    
    interpretation = f"**{ticker} Piyasa Analizi ve Yorumu:**\n\n"

    interpretation += f"**Volatilite Smile Analizi:**\n"
    interpretation += f"- Call opsiyonları için ortalama implied volatilite %{overall_avg_iv_calls:.2f}.\n"
    interpretation += f"- Put opsiyonları için ortalama implied volatilite %{overall_avg_iv_puts:.2f}.\n"
    interpretation += f"- Call opsiyonları {'belirgin bir volatilite smile gösteriyor' if avg_iv_by_strike_calls.var() > 0.1 else 'belirgin bir volatilite smile göstermiyor'}.\n"
    interpretation += f"- Put opsiyonları {'belirgin bir volatilite smile gösteriyor' if avg_iv_by_strike_puts.var() > 0.1 else 'belirgin bir volatilite smile göstermiyor'}.\n"
    interpretation += f"- Genel piyasa hissiyatı {'yükseliş eğilimli' if overall_avg_iv_calls > overall_avg_iv_puts else 'düşüş eğilimli'}, call ve put opsiyonlarının ortalama implied volatilitesinden elde edilmiştir.\n\n"

    interpretation += f"**İşlem Hacmi Analizi:**\n"
    interpretation += f"- Call opsiyonları için ortalama işlem hacmi {overall_avg_vol_calls:.2f} kontrat.\n"
    interpretation += f"- Put opsiyonları için ortalama işlem hacmi {overall_avg_vol_puts:.2f} kontrat.\n"
    interpretation += f"- {'Call' if overall_avg_vol_calls > overall_avg_vol_puts else 'Put'} opsiyonlarında daha yüksek ortalama işlem hacmi var, bu da {'call' if overall_avg_vol_calls > overall_avg_vol_puts else 'put'}larda daha yüksek işlem aktivitesi ve ilgi olduğunu gösterir.\n"
    highest_vol_call = calls_data.loc[calls_data['volume'].idxmax()]
    highest_vol_put = puts_data.loc[puts_data['volume'].idxmax()]
    interpretation += f"- Call'lar için en yüksek işlem hacmine sahip kullanım fiyatı {highest_vol_call['strike']} ile {highest_vol_call['volume']} kontrat.\n"
    interpretation += f"- Put'lar için en yüksek işlem hacmine sahip kullanım fiyatı {highest_vol_put['strike']} ile {highest_vol_put['volume']} kontrat.\n\n"

    interpretation += f"**Tarihsel İmplied Volatilite Analizi:**\n"
    avg_iv = historical_iv["IV"].mean()
    max_iv = historical_iv["IV"].max()
    min_iv = historical_iv["IV"].min()
    interpretation += f"- Dönem boyunca ortalama implied volatilite %{avg_iv:.2f}.\n"
    interpretation += f"- Kaydedilen en yüksek implied volatilite %{max_iv:.2f}.\n"
    interpretation += f"- Kaydedilen en düşük implied volatilite %{min_iv:.2f}.\n"
    interpretation += f"- Mevcut implied volatilite %{current_iv:.2f}.\n"
    if len(historical_iv) > 30:
        recent_trend = "artmış" if historical_iv['IV'].iloc[-1] > historical_iv['IV'].iloc[-30] else "azalmış"
        interpretation += f"- Son 30 günde, implied volatilite önceki döneme göre {recent_trend}.\n\n"

    interpretation += f"**Put/Call Oranı Analizi:**\n"
    interpretation += f"- Put/Call Oranı {put_call_ratio:.2f}.\n"
    interpretation += f"- Put'ların toplam hacmi: {total_puts}\n"
    interpretation += f"- Call'ların toplam hacmi: {total_calls}\n"
    if put_call_ratio > 1:
        interpretation += "- 1'den büyük bir Put/Call Oranı, piyasada düşüş eğilimli bir hissiyatı gösterir, çünkü call'lara göre daha fazla put işlem görüyor.\n\n"
    elif put_call_ratio < 1:
        interpretation += "- 1'den küçük bir Put/Call Oranı, piyasada yükseliş eğilimli bir hissiyatı gösterir, çünkü put'lara göre daha fazla call işlem görüyor.\n\n"
    else:
        interpretation += "- 1'e eşit bir Put/Call Oranı, piyasada nötr bir hissiyatı gösterir, put ve call'ların eşit hacimlerde işlem gördüğünü belirtir.\n\n"

    interpretation += f"**Greeks Analizi:**\n"
    interpretation += f"- **Delta:**\n"
    interpretation += f"  - Call opsiyonları için ortalama delta: {avg_delta_calls:.4f}.\n"
    interpretation += f"  - Put opsiyonları için ortalama delta: {avg_delta_puts:.4f}.\n"
    interpretation += f"- **Gamma:**\n"
    interpretation += f"  - Call opsiyonları için ortalama gamma: {avg_gamma_calls:.4f}.\n"
    interpretation += f"  - Put opsiyonları için ortalama gamma: {avg_gamma_puts:.4f}.\n"
    interpretation += f"- **Theta:**\n"
    interpretation += f"  - Call opsiyonları için ortalama theta: {avg_theta_calls:.4f}.\n"
    interpretation += f"  - Put opsiyonları için ortalama theta: {avg_theta_puts:.4f}.\n"
    interpretation += f"- **Vega:**\n"
    interpretation += f"  - Call opsiyonları için ortalama vega: {avg_vega_calls:.4f}.\n"
    interpretation += f"  - Put opsiyonları için ortalama vega: {avg_vega_puts:.4f}.\n\n"

    interpretation += f"**Hissiyat Skoru Analizi:**\n"
    interpretation += f"- Piyasa Hissiyatı Skoru: {sentiment_score:.2f} ({sentiment_description}).\n"
    interpretation += f"- En yüksek IV'li call opsiyonları: %{high_iv_calls:.2f}.\n"
    interpretation += f"- En düşük IV'li put opsiyonları: %{low_iv_puts:.2f}.\n"
    interpretation += f"- Call/Put Hacim Oranı: {total_calls/total_puts:.2f}.\n"
    if sentiment_score > 0.6:
        interpretation += "- Yüksek bir hissiyat skoru, piyasanın güçlü bir yükseliş eğiliminde olduğunu gösterir. Yatırımcılar, hisse senedi fiyatında yukarı yönlü hareketler bekliyor olabilir.\n"
    elif sentiment_score < 0.4:
        interpretation += "- Düşük bir hissiyat skoru, piyasanın güçlü bir düşüş eğiliminde olduğunu gösterir. Yatırımcılar, hisse senedi fiyatında aşağı yönlü hareketler bekliyor olabilir.\n"
    else:
        interpretation += "- Orta düzeyde bir hissiyat skoru, piyasanın nötr veya kararsız olduğunu gösterir. Yatırımcılar, hisse senedi fiyatında belirgin bir yön beklemiyor olabilir.\n"

    interpretation += "\n**Genel Piyasa Değerlendirmesi ve Yatırım Stratejisi Önerileri:**\n"
    
    market_trend = "yükseliş" if sentiment_score > 0.5 else "düşüş"
    volatility_state = "yüksek" if overall_avg_iv_calls > 30 or overall_avg_iv_puts > 30 else "düşük"
    
    interpretation += f"- **Piyasa Eğilimi:** {ticker} için genel piyasa eğilimi {market_trend} yönünde görünmektedir. "
    interpretation += f"Bu durum, {'call' if market_trend == 'yükseliş' else 'put'} opsiyonlarındaki yüksek implied volatilite, "
    interpretation += f"{'düşük' if market_trend == 'yükseliş' else 'yüksek'} put/call oranı ve genel hissiyat skorundan anlaşılmaktadır.\n"
    
    interpretation += f"- **Volatilite Durumu:** Mevcut implied volatilite seviyeleri {volatility_state} olarak değerlendirilebilir. "
    
    if volatility_state == "yüksek":
        interpretation += "Yüksek volatilite, piyasada belirsizlik ve risk algısının arttığını gösterir. "
        interpretation += "Bu durum, yaklaşan önemli bir haber, şirket açıklaması veya ekonomik veri beklentisinden kaynaklanıyor olabilir.\n"
    else:
        interpretation += "Düşük volatilite, piyasada istikrar ve düşük risk algısını gösterir. "
        interpretation += "Bu durum, piyasanın mevcut fiyatlamaya güvendiğini ve yakın vadede büyük fiyat hareketleri beklenmediğini gösterir.\n"
    
    interpretation += "- **Opsiyon Stratejisi Önerileri:**\n"
    
    if market_trend == "yükseliş" and volatility_state == "yüksek":
        interpretation += "  * Yükseliş eğilimli yüksek volatilite ortamında, call opsiyonları satın almak veya bull call spread stratejileri düşünülebilir.\n"
        interpretation += "  * Yüksek volatiliteden faydalanmak için, covered call stratejisi de etkili olabilir.\n"
        interpretation += "  * Riskten korunmak için, portföyünüzde koruyucu put opsiyonları bulundurmak faydalı olabilir.\n"
    elif market_trend == "yükseliş" and volatility_state == "düşük":
        interpretation += "  * Yükseliş eğilimli düşük volatilite ortamında, LEAPS call opsiyonları (uzun vadeli) veya call alım stratejileri düşünülebilir.\n"
        interpretation += "  * Düşük volatiliteden faydalanmak için, bull call spread veya risk reversal stratejileri uygun olabilir.\n"
        interpretation += "  * Volatilitenin artması bekleniyorsa, long straddle veya strangle stratejileri değerlendirilebilir.\n"
    elif market_trend == "düşüş" and volatility_state == "yüksek":
        interpretation += "  * Düşüş eğilimli yüksek volatilite ortamında, put opsiyonları satın almak veya bear put spread stratejileri düşünülebilir.\n"
        interpretation += "  * Yüksek volatiliteden faydalanmak için, covered put stratejisi etkili olabilir.\n"
        interpretation += "  * Riskten korunmak için, portföyünüzdeki uzun pozisyonları azaltmak veya hedge etmek önemlidir.\n"
    else:  # market_trend == "düşüş" and volatility_state == "düşük"
        interpretation += "  * Düşüş eğilimli düşük volatilite ortamında, put opsiyonları veya bear put spread stratejileri düşünülebilir.\n"
        interpretation += "  * Düşük volatiliteden faydalanmak için, put yazma stratejileri uygun olabilir.\n"
        interpretation += "  * Volatilitenin artması bekleniyorsa, long straddle veya strangle stratejileri değerlendirilebilir.\n"
    
    interpretation += "- **Greeks Bazlı Değerlendirme:**\n"
    
    if abs(avg_delta_calls) > 0.5:
        interpretation += f"  * Call opsiyonları için yüksek delta ({avg_delta_calls:.4f}), bu opsiyonların dayanak varlık fiyat değişimlerine daha duyarlı olduğunu gösterir.\n"
    if abs(avg_delta_puts) > 0.5:
        interpretation += f"  * Put opsiyonları için yüksek delta ({avg_delta_puts:.4f}), bu opsiyonların dayanak varlık fiyat değişimlerine daha duyarlı olduğunu gösterir.\n"
    
    if avg_gamma_calls > 0.05 or avg_gamma_puts > 0.05:
        interpretation += f"  * Yüksek gamma değerleri, delta değerinin hızla değişebileceğini gösterir. Bu durum, fiyat hareketlerinin hızlanması durumunda opsiyon değerlerinde büyük değişimler yaşanabileceğini işaret eder.\n"
    
    if abs(avg_theta_calls) > 0.05 or abs(avg_theta_puts) > 0.05:
        interpretation += f"  * Yüksek theta değerleri, zaman değeri kaybının hızlı olduğunu gösterir. Kısa vadeli opsiyonlarda bu kayıp daha belirgindir. Uzun opsiyon pozisyonlarında bu zaman değeri kaybını dikkate almak önemlidir.\n"
    
    if avg_vega_calls > 0.1 or avg_vega_puts > 0.1:
        interpretation += f"  * Yüksek vega değerleri, opsiyon fiyatlarının volatilite değişimlerine duyarlı olduğunu gösterir. Volatilite artışı bekleniyorsa, yüksek vega'lı opsiyonlar avantajlı olabilir.\n"
    
    interpretation += "\n**Önemli Uyarı:**\n"
    interpretation += "- Bu analiz, mevcut piyasa verilerine dayanmaktadır ve gelecekteki piyasa hareketlerini garanti etmez.\n"
    interpretation += "- Opsiyon işlemleri yüksek risk içerir ve sermayenizin tamamını kaybetme olasılığı vardır.\n"
    interpretation += "- Yatırım kararları vermeden önce, kendi araştırmınızı yapmanız ve profesyonel finansal danışmanlık almanız önerilir.\n"
    interpretation += "- Piyasa koşulları hızla değişebilir, bu nedenle düzenli olarak pozisyonlarınızı ve stratejilerinizi gözden geçirin.\n"
    interpretation += f"- {ticker} için bu analiz, {current_iv:.2f}% implied volatilite ve {sentiment_score:.2f} hissiyat skoru temelinde yapılmıştır.\n"

    return interpretation


def interpret_future_iv_predictions(ticker, historical_iv, predictions_df):
    """Gelecekteki IV tahminlerini yorumlar."""
    if historical_iv is None or predictions_df is None or predictions_df.empty:
        return None
        
    interpretation = f"**{ticker} İmplied Volatilite Tahmin Yorumu:**\n"
    
    current_iv = historical_iv['IV'].iloc[-1]
    last_predicted_iv = predictions_df['Predicted_IV'].iloc[-1]
    
    interpretation += f"- Mevcut implied volatilite: %{current_iv:.2f}.\n"
    interpretation += f"- Tahmin edilen son implied volatilite: %{last_predicted_iv:.2f}.\n"
    
    if last_predicted_iv > current_iv:
        change_pct = ((last_predicted_iv - current_iv) / current_iv) * 100
        interpretation += f"- Tahmin döneminde implied volatilite %{change_pct:.2f} artış gösteriyor, bu da piyasada artan belirsizlik beklentisi olduğunu gösterebilir.\n"
    elif last_predicted_iv < current_iv:
        change_pct = ((current_iv - last_predicted_iv) / current_iv) * 100
        interpretation += f"- Tahmin döneminde implied volatilite %{change_pct:.2f} düşüş gösteriyor, bu da piyasada azalan belirsizlik beklentisi olduğunu gösterebilir.\n"
    else:
        interpretation += "- Tahmin döneminde implied volatilite nispeten sabit kalıyor, bu da piyasada istikrarlı bir belirsizlik beklentisi olduğunu gösterebilir.\n"
    
    min_predicted = predictions_df['Predicted_IV'].min()
    max_predicted = predictions_df['Predicted_IV'].max()
    range_predicted = max_predicted - min_predicted
    
    interpretation += f"- Tahmin edilen implied volatilite aralığı: %{min_predicted:.2f} - %{max_predicted:.2f} (aralık: %{range_predicted:.2f}).\n"
    
    if range_predicted > 5:
        interpretation += "- Tahmin edilen implied volatilite aralığı geniş, bu da tahmin döneminde yüksek oynaklık beklentisi olduğunu gösterebilir.\n"
    else:
        interpretation += "- Tahmin edilen implied volatilite aralığı dar, bu da tahmin döneminde istikrarlı bir oynaklık beklentisi olduğunu gösterebilir.\n"
    
    historical_avg = historical_iv["IV"].mean()
    historical_std = historical_iv["IV"].std()
    
    if last_predicted_iv > (historical_avg + historical_std):
        interpretation += f"- Son tahmin edilen implied volatilite (%{last_predicted_iv:.2f}), tarihsel ortalamadan (%{historical_avg:.2f}) bir standart sapma (%{historical_std:.2f}) daha yüksek, bu da olağandışı yüksek bir oynaklık beklentisi olduğunu gösterebilir.\n"
    elif last_predicted_iv < (historical_avg - historical_std):
        interpretation += f"- Son tahmin edilen implied volatilite (%{last_predicted_iv:.2f}), tarihsel ortalamadan (%{historical_avg:.2f}) bir standart sapma (%{historical_std:.2f}) daha düşük, bu da olağandışı düşük bir oynaklık beklentisi olduğunu gösterebilir.\n"
    else:
        interpretation += f"- Son tahmin edilen implied volatilite (%{last_predicted_iv:.2f}), tarihsel ortalama (%{historical_avg:.2f}) etrafında normal bir aralıkta, bu da piyasada normal bir oynaklık beklentisi olduğunu gösterebilir.\n"
    
    interpretation += "\n**Tahmin Güvenilirliği Uyarısı:**\n"
    interpretation += "- Bu tahminler geçmiş verilere dayalı olarak yapılmıştır ve gelecekteki piyasa koşullarını tam olarak yansıtmayabilir.\n"
    interpretation += "- Özellikle beklenmedik haberler, ekonomik olaylar veya şirket duyuruları gibi faktörler implied volatiliteyi önemli ölçüde etkileyebilir.\n"
    interpretation += "- Bu tahminleri yatırım kararları için tek başına bir gösterge olarak kullanmak yerine, diğer analiz araçlarıyla birlikte değerlendirmek önemlidir.\n"
    
    return interpretation