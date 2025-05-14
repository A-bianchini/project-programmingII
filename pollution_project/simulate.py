import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def simulate_pollution(df, pollutant_col, traffic_col, reduction_pct=0.3, n_sim=1000000, ci=0.95, plot=True):
    """
    Simula l'inquinante in funzione del traffico con Monte Carlo.

    Parametri:
    - df: DataFrame con i dati
    - pollutant_col: nome della colonna dell'inquinante (es. 'NO2_media_2024')
    - traffic_col: nome della colonna del traffico (es. 'traffico_media_2024')
    - reduction_pct: percentuale di riduzione del traffico (es. 0.3 per 30%)
    - n_sim: numero di simulazioni
    - ci: livello di confidenza (es. 0.95)
    - plot: se True, disegna l'istogramma

    Ritorna:
    - dizionario con media, intervallo di confidenza, Env-VaR, simulazioni e riduzione
    """
    # Pulisci dati
    df = df[[pollutant_col, traffic_col]].dropna()

    # Modello lineare
    model = LinearRegression().fit(df[[traffic_col]], df[pollutant_col])
    residuals = df[pollutant_col] - model.predict(df[[traffic_col]])

    # Traffico ridotto
    traffic_reduced = df[traffic_col].mean() * (1 - reduction_pct)

    # Simulazione Monte Carlo
    simulated_vals = []
    for _ in range(n_sim):
        error = np.random.choice(residuals)
        sim_val = model.intercept_ + model.coef_[0] * traffic_reduced + error
        simulated_vals.append(sim_val)

    simulated_vals = np.array(simulated_vals)
    mean_val = simulated_vals.mean()
    ci_lower = np.percentile(simulated_vals, (1 - ci)/2 * 100)
    ci_upper = np.percentile(simulated_vals, (1 + ci)/2 * 100)
    env_var_95 = np.percentile(simulated_vals, 95)

    # Grafico opzionale
    if plot:
        plt.hist(simulated_vals, bins=30, alpha=0.7, color="lightblue")
        plt.axvline(mean_val, color="red", linestyle="--", label="Mean")
        plt.axvline(ci_lower, color="green", linestyle=":", label=f"{int(ci*100)}% CI lower")
        plt.axvline(ci_upper, color="green", linestyle=":", label=f"{int(ci*100)}% CI upper")
        plt.axvline(env_var_95, color="purple", linestyle="-.", label="Env-VaR 95%")
        plt.title(f"{pollutant_col} – {int(reduction_pct*100)}% traffico in meno")
        plt.xlabel(f"{pollutant_col} (µg/m³)")
        plt.ylabel("Frequency")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    return {
        "mean": mean_val,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "env_var_95": env_var_95,
        "simulated_array": simulated_vals,
        "reduction_pct": reduction_pct
    }
