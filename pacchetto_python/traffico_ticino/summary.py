import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from pathlib import Path
from IPython.display import display


def summary(station="all", show="ols", pollutants="all", comparison=True):
    # Percorsi base
    base_path = Path(__file__).parent / "data"
    noO3_path = base_path / "stazioni singole" / "noO3"
    meteo_path = base_path / "meteo_mensile"

    # Stazioni disponibili
    stazioni_disponibili = [
        "Chiasso", "Bioggio", "Giubiasco", "Locarno", "Mendrisio", "Minusio", "Airolo"
    ]

    # Inquinanti disponibili
    tutti_pollutanti = ["no", "no2", "nox", "pm10"]

    # Interpreta argomenti
    if station == "all":
        stazioni_target = stazioni_disponibili
    elif isinstance(station, str):
        stazioni_target = [station]
    else:
        stazioni_target = station

    if pollutants == "all":
        pollutants = tutti_pollutanti

    risultati_regressione = []
    dati_per_confronto = {pol: [] for pol in pollutants}

    for st in stazioni_target:
        try:
            df_poll = pd.read_csv(noO3_path / f"{st}_noO3.csv")
            df_poll['date'] = pd.to_datetime(df_poll['date'])
            df_poll['month'] = df_poll['date'].dt.to_period("M")

            df_meteo = pd.read_csv(meteo_path / f"{st.lower()}_meteo_mensile.csv")
            df_meteo['date'] = pd.to_datetime(df_meteo['date'], format="%Y-%m")
            df_meteo['month'] = df_meteo['date'].dt.to_period("M")

            df_full = pd.merge(
                df_poll,
                df_meteo[['month', 'temperatura', 'precipitazioni', 'vento']],
                on='month',
                how='left'
            )
        except FileNotFoundError:
            print(f"⚠ Dati non trovati per {st}, saltata.")
            continue

        for pol in pollutants:
            if pol not in df_full.columns:
                print(f"⚠ Nessun dato valido per {pol.upper()} – {st}")
                continue

            predictors = ['traffic', 'temperatura', 'precipitazioni', 'vento']
            data = df_full[[pol] + predictors].dropna()

            if data.empty:
                continue

            X = sm.add_constant(data[predictors])
            y = data[pol]
            model = sm.OLS(y, X).fit()

            if show in ["ols", "all"]:
                print(f"\n📌 Regressione per: {pol.upper()} – {st}")
                print(model.summary())

            if show in ["graphic", "all"]:
                data['predicted'] = model.predict(X)
                data['station'] = st
                dati_per_confronto[pol].append(data)

                plt.figure(figsize=(8, 5))
                sns.scatterplot(x=data['traffic'], y=data[pol], label="Osservato", alpha=0.6)
                sns.lineplot(x=data['traffic'], y=data['predicted'], color="red", label="Predetto")
                plt.title(f"{pol.upper()} ~ Traffic (con meteo) – {st}")
                plt.xlabel("Traffic")
                plt.ylabel(pol.upper())
                plt.legend()
                plt.grid(True)
                plt.tight_layout()
                plt.show()

            risultati_regressione.append({
                "Stazione": st,
                "Inquinante": pol.upper(),
                "R2": round(model.rsquared, 3),
                "p_traffic": round(model.pvalues.get('traffic', None), 4),
                "coeff_traffic": round(model.params.get('traffic', None), 5)
            })

    if comparison and risultati_regressione:
        df_riepilogo = pd.DataFrame(risultati_regressione)

        if show in ["ols", "all"]:
            print("\n\n📊 Tabella comparativa delle regressioni OLS")
            for pol in pollutants:
                df_pol = df_riepilogo[df_riepilogo["Inquinante"] == pol.upper()][
                    ["Stazione", "coeff_traffic", "p_traffic", "R2"]
                ].set_index("Stazione")
                df_pol.columns = ["coeff_traffic", "p_value", "R_squared"]
                print(f"\n🔎 {pol.upper()}")
                display(df_pol)

        if show in ["graphic", "all"]:
            for pol in pollutants:
                combined_df = pd.concat(dati_per_confronto[pol], ignore_index=True)
                if combined_df.empty:
                    continue

                plt.figure(figsize=(10, 6))
                sns.scatterplot(
                    data=combined_df, x="traffic", y=pol, hue="station", alpha=0.6, style="station"
                )
                sns.lineplot(
                    data=combined_df, x="traffic", y="predicted", hue="station", legend=False, lw=2
                )
                plt.title(f"Confronto stazioni – {pol.upper()} vs Traffic")
                plt.xlabel("Traffic")
                plt.ylabel(pol.upper())
                plt.grid(True)
                plt.tight_layout()
                plt.show()

    return

