import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import RandomizedSearchCV
import warnings
warnings.filterwarnings('ignore')
import lightgbm as lgb

# =====================
# TEKNİK ÖZELLİKLER
# =====================
def add_technical_features(df):
    df_copy = df.copy()
    df_copy['MA5'] = df_copy['IV'].rolling(window=5).mean()
    df_copy['MA10'] = df_copy['IV'].rolling(window=10).mean()
    df_copy['MA20'] = df_copy['IV'].rolling(window=20).mean()
    df_copy['Volatility'] = df_copy['IV'].rolling(window=10).std()
    df_copy['ROC5'] = df_copy['IV'].pct_change(periods=5) * 100
    df_copy['ROC10'] = df_copy['IV'].pct_change(periods=10) * 100
    df_copy['EMA5'] = df_copy['IV'].ewm(span=5, adjust=False).mean()
    df_copy['EMA10'] = df_copy['IV'].ewm(span=10, adjust=False).mean()
    df_copy['MACD'] = df_copy['EMA5'] - df_copy['EMA10']
    df_copy['DayOfWeek_sin'] = np.sin(2 * np.pi * df_copy.index.dayofweek / 7)
    df_copy['DayOfWeek_cos'] = np.cos(2 * np.pi * df_copy.index.dayofweek / 7)
    df_copy['DayOfMonth_sin'] = np.sin(2 * np.pi * df_copy.index.day / 31)
    df_copy['DayOfMonth_cos'] = np.cos(2 * np.pi * df_copy.index.day / 31)
    df_copy['IV_diff1'] = df_copy['IV'].diff(1)
    df_copy['IV_diff5'] = df_copy['IV'].diff(5)
    df_copy['IV_max5'] = df_copy['IV'].rolling(window=5).max()
    df_copy['IV_min5'] = df_copy['IV'].rolling(window=5).min()
    df_copy['Vol_change'] = df_copy['Volatility'].pct_change() * 100
    df_copy = df_copy.fillna(method='ffill').fillna(method='bfill')
    return df_copy

def get_feature_columns():
    return [
        'MA5', 'MA10', 'MA20', 'Volatility', 'ROC5', 'ROC10', 'EMA5', 'EMA10', 'MACD',
        'DayOfWeek_sin', 'DayOfWeek_cos', 'DayOfMonth_sin', 'DayOfMonth_cos',
        'IV_diff1', 'IV_diff5', 'IV_max5', 'IV_min5', 'Vol_change'
    ]

def prepare_time_series_data(df, window_size=20):
    df = df.sort_index()
    df = df.fillna(method='ffill').fillna(method='bfill')
    df = add_technical_features(df)
    features, targets, dates = [], [], []
    min_required_rows = max(window_size, 20) + 1
    if len(df) <= min_required_rows:
        print(f"Uyarı: Veri seti çok küçük! En az {min_required_rows} satır gerekli.")
        return None, None, None
    for i in range(len(df) - window_size):
        window_features = df['IV'].iloc[i:i+window_size].values
        extra_features = df.iloc[i+window_size-1][get_feature_columns()].values
        all_features = np.concatenate([window_features, extra_features])
        # Hedef değişken: log(IV) farkı
        prev_iv = df['IV'].iloc[i+window_size-1]
        curr_iv = df['IV'].iloc[i+window_size]
        # Negatif veya sıfır IV varsa log alınamaz, küçük bir sabit ekle
        prev_iv = max(prev_iv, 1e-6)
        curr_iv = max(curr_iv, 1e-6)
        target = np.log(curr_iv) - np.log(prev_iv)
        features.append(all_features)
        targets.append(target)
        dates.append(df.index[i+window_size])
    return np.array(features), np.array(targets), dates

def train_iv_prediction_model(historical_iv_data, window_size=20, test_size=0.2):
    X, y, dates = prepare_time_series_data(historical_iv_data, window_size)
    if X is None or len(X) < 10:
        print("Yeterli veri yok! Model eğitilemedi.")
        return None, None, None
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    param_grid = {
        'num_leaves': [15, 31, 63, 127],
        'learning_rate': [0.005, 0.01, 0.05, 0.1, 0.2],
        'n_estimators': [200, 500, 1000, 1500],
        'min_child_samples': [3, 5, 10, 20],
        'min_split_gain': [0.0, 0.01, 0.05],
        'reg_alpha': [0, 0.1, 1],
        'reg_lambda': [0, 0.1, 1]
    }
    lgbm = lgb.LGBMRegressor(random_state=42)
    tscv = TimeSeriesSplit(n_splits=3)
    search = RandomizedSearchCV(lgbm, param_grid, n_iter=20, scoring='neg_mean_squared_error', cv=tscv, n_jobs=-1, random_state=42)
    search.fit(X_scaled, y)
    model = search.best_estimator_
    y_pred = model.predict(X_scaled)
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    print(f"LightGBM Model (log(IV) farkı) - MSE: {mse:.4f}, R²: {r2:.4f}")
    print_feature_importance(model, window_size)
    return model, scaler, get_feature_columns()

def print_feature_importance(model, window_size):
    feature_importance = model.feature_importances_
    print("\nÖzellik Önemleri:")
    feature_columns = get_feature_columns()
    for i, importance in enumerate(feature_importance):
        if i < window_size:
            print(f"IV_{i+1}: {importance:.4f}")
        else:
            idx = i - window_size
            if idx < len(feature_columns):
                print(f"{feature_columns[idx]}: {importance:.4f}")

def get_cyclic_date_features(date):
    day_of_week_sin = np.sin(2 * np.pi * date.dayofweek / 7)
    day_of_week_cos = np.cos(2 * np.pi * date.dayofweek / 7)
    day_of_month_sin = np.sin(2 * np.pi * date.day / 31)
    day_of_month_cos = np.cos(2 * np.pi * date.day / 31)
    return day_of_week_sin, day_of_week_cos, day_of_month_sin, day_of_month_cos

def create_empty_prediction_df(last_date, days_to_predict, default_value=None):
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=days_to_predict, freq='B')
    df = pd.DataFrame(index=future_dates)
    if default_value is not None:
        df['Predicted_IV'] = [default_value] * days_to_predict
    else:
        df['IV'] = np.nan
    return df, future_dates

def predict_future_iv(model, scaler, historical_iv_data, days_to_predict=15, window_size=20):
    if model is None:
        print("Model eğitilemedi! Tahmin yapılamıyor.")
        last_date = historical_iv_data.index[-1]
        predictions_df, _ = create_empty_prediction_df(
            last_date, 
            days_to_predict, 
            default_value=historical_iv_data['IV'].mean()
        )
        return predictions_df
    df = add_technical_features(historical_iv_data.copy().sort_index())
    latest_iv_values = df['IV'].values[-window_size:]
    last_date = df.index[-1]
    last_iv = df['IV'].iloc[-1]
    last_iv = max(last_iv, 1e-6)  # Log alınabilir olması için
    last_volatility = df['Volatility'].iloc[-1]
    predicted_df, future_dates = create_empty_prediction_df(last_date, days_to_predict)
    combined_df = df.copy()
    future_predictions = []
    current_features = latest_iv_values.copy()
    ema5 = df['EMA5'].iloc[-1]
    ema10 = df['EMA10'].iloc[-1]
    for i in range(days_to_predict):
        future_date = future_dates[i]
        day_of_week_sin, day_of_week_cos, day_of_month_sin, day_of_month_cos = get_cyclic_date_features(future_date)
        if i == 0:
            ma5 = df['MA5'].iloc[-1]
            ma10 = df['MA10'].iloc[-1]
            ma20 = df['MA20'].iloc[-1]
            volatility = df['Volatility'].iloc[-1]
            roc5 = df['ROC5'].iloc[-1]
            roc10 = df['ROC10'].iloc[-1]
            iv_diff1 = df['IV_diff1'].iloc[-1]
            iv_diff5 = df['IV_diff5'].iloc[-1]
            iv_max5 = df['IV_max5'].iloc[-1]
            iv_min5 = df['IV_min5'].iloc[-1]
            vol_change = df['Vol_change'].iloc[-1]
            macd = df['MACD'].iloc[-1]
        else:
            for prev_date in future_dates[:i]:
                if prev_date in predicted_df.index:
                    combined_df.loc[prev_date, 'IV'] = predicted_df.loc[prev_date, 'IV']
            ma5 = combined_df['IV'].iloc[-5:].mean()
            ma10 = combined_df['IV'].iloc[-10:].mean()
            ma20 = combined_df['IV'].iloc[-20:].mean()
            volatility = combined_df['IV'].iloc[-10:].std() if len(combined_df) >= 10 else last_volatility
            roc5 = (future_predictions[-1] - future_predictions[-5]) / future_predictions[-5] * 100 if len(future_predictions) >= 5 and future_predictions[-5] != 0 else 0
            roc10 = 0
            if len(future_predictions) > 0:
                ema5 = ema5 * 0.8 + future_predictions[-1] * 0.2
                ema10 = ema10 * 0.9 + future_predictions[-1] * 0.1
            macd = ema5 - ema10
            iv_diff1 = future_predictions[-1] - (future_predictions[-2] if len(future_predictions) > 1 else current_features[-1])
            iv_diff5 = 0
            iv_max5 = max(future_predictions[-5:]) if len(future_predictions) >= 5 else max(future_predictions + list(current_features))
            iv_min5 = min(future_predictions[-5:]) if len(future_predictions) >= 5 else min(future_predictions + list(current_features))
            vol_change = 0
        extra_features = np.array([
            ma5, ma10, ma20, volatility, roc5, roc10, ema5, ema10, macd,
            day_of_week_sin, day_of_week_cos, day_of_month_sin, day_of_month_cos,
            iv_diff1, iv_diff5, iv_max5, iv_min5, vol_change
        ])
        all_features = np.concatenate([current_features, extra_features])
        scaled_features = scaler.transform(all_features.reshape(1, -1))
        # Model log(IV) farkı tahmin ediyor
        next_log_iv_delta = model.predict(scaled_features)[0]
        next_log_iv = np.log(last_iv) + next_log_iv_delta
        next_iv = np.exp(next_log_iv)
        next_iv = max(next_iv, 0)  # Negatif IV engellenir
        last_iv = next_iv
        future_predictions.append(next_iv)
        predicted_df.loc[future_date, 'IV'] = next_iv
        combined_df.loc[future_date] = np.nan
        combined_df.loc[future_date, 'IV'] = next_iv
        current_features = np.roll(current_features, -1)
        current_features[-1] = next_iv
    predictions_df = pd.DataFrame({
        'Predicted_IV': future_predictions
    }, index=future_dates)
    return predictions_df
