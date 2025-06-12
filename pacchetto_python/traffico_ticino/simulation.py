import pandas as pd
import numpy as np
import json
import os
import warnings

def monte_verita_simulation(
    df,
    variable,
    traffic_col=None,
    trend_type="historical",
    custom_trend=None,
    period_freq="M",
    meteo_csv_path=None,
    coef_json_path=None,
    traffic_in_units=1,
    n_simulations=1000,
    seed=42,
    temp_col=None,
    wind_col=None,
    rain_col=None,
    modification_factor=1.1,
    growth_rate=0.02,
    linear_slope=5.0,
    n_periods=48
):
    df = df.copy()

    # Gestione intelligente delle date: estensione assoluta a n_periods
    if period_freq is not None:
        if 'date' not in df.columns:
            raise ValueError("La colonna 'date' è obbligatoria quando si usa 'period_freq'.")
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date').reset_index(drop=True)

        first_date = df['date'].min()
        full_dates = pd.date_range(start=first_date, periods=n_periods, freq=period_freq)
        df = df.reindex(range(n_periods)).copy()
        df['date'] = full_dates
    else:
        df = df.reindex(range(n_periods)).copy()
        df['date'] = list(range(n_periods))

    if traffic_col is None:
        excluded = {"date", "variable"}
        candidates = [col for col in df.columns if col not in excluded]
        if not candidates:
            raise ValueError("Non ci sono colonne valide nel DataFrame per essere usate come traffico.")
        traffic_col = candidates[0]
        warnings.warn(f"Nessuna colonna 'traffic_col' specificata: uso '{traffic_col}'.")

    if traffic_col not in df.columns:
        df[traffic_col] = np.nan  # crea colonna vuota per i nuovi periodi

    if trend_type == "historical":
        traffic_series = df[traffic_col].interpolate(limit_direction='both').values
    elif trend_type == "manual":
        if custom_trend is None:
            raise ValueError("custom_trend deve essere specificato se trend_type='manual'")
        if len(custom_trend) != len(df):
            raise ValueError("custom_trend deve avere la stessa lunghezza del DataFrame")
        traffic_series = np.array(custom_trend)
    elif trend_type == "linear":
        first_value = df[traffic_col].dropna().iloc[0]
        traffic_series = first_value + linear_slope * np.arange(len(df))
    elif trend_type == "exponential":
        base_value = df[traffic_col].dropna().iloc[0]
        traffic_series = base_value * (1 + growth_rate) ** np.arange(len(df))
    elif trend_type == "historical_modified":
        traffic_series = df[traffic_col].interpolate(limit_direction='both').values * modification_factor
    else:
        raise ValueError(f"Trend type '{trend_type}' non supportato.")

    traffic_series = traffic_series / traffic_in_units

    if coef_json_path is None:
        coef_json_path = os.path.join(
            os.path.dirname(__file__), "data", "coefficients", "pooled.json"
        )

    with open(coef_json_path, "r") as f:
        coef = json.load(f)

    intercept = coef[variable]["const"]
    beta_traffic = coef[variable]["traffico"]
    beta_temp = coef[variable].get("temperatura", 0)
    beta_wind = coef[variable].get("vento", 0)
    beta_prec = coef[variable].get("precipitazioni", 0)

    meteo_needed = any([beta_temp != 0, beta_wind != 0, beta_prec != 0])
    meteo_cols = {
        'temperatura': temp_col or 'temperatura',
        'vento': wind_col or 'vento',
        'precipitazioni': rain_col or 'precipitazioni'
    }

    if meteo_needed:
        if meteo_csv_path is None:
            for key, col in meteo_cols.items():
                if col in df.columns:
                    df[key] = df[col]
                else:
                    warnings.warn(f"Colonna meteo '{col}' non trovata. '{key}' impostata a 0.")
                    df[key] = 0
        else:
            meteo_df = pd.read_csv(meteo_csv_path)
            if 'month' not in meteo_df.columns:
                raise ValueError("Il file meteo deve contenere una colonna 'month' con valori da 1 a 12.")
            df['mese'] = df['date'].dt.month
            df = df.merge(meteo_df, left_on='mese', right_on='month', how='left')
            for key, col in meteo_cols.items():
                df[key] = df.get(col, 0)
    else:
        df['temperatura'] = 0
        df['vento'] = 0
        df['precipitazioni'] = 0

    df['base_prediction'] = (
        intercept
        + beta_traffic * traffic_series
        + beta_temp * df['temperatura']
        + beta_wind * df['vento']
        + beta_prec * df['precipitazioni']
    )

    np.random.seed(seed)
    std_val = df['base_prediction'].dropna().std()
    if pd.isna(std_val) or std_val == 0:
        warnings.warn("DEBUG: Deviazione standard nulla o NaN. Imposto std_val = 1.0")
        std_val = 1.0

    simulations = [df['base_prediction'] + np.random.normal(0, std_val, size=len(df))
                   for _ in range(n_simulations)]

    sim_df = pd.DataFrame(simulations).T
    sim_df.columns = [f"sim_{i+1}" for i in range(n_simulations)]
    sim_df['date'] = df['date'].astype(str)
    sim_df['base_prediction'] = df['base_prediction']

    return sim_df
