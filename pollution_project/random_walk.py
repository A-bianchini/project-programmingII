import numpy as np
import matplotlib.pyplot as plt

def simulate_random_walk(start_value, mu=0, sigma=1, n_steps=30, n_sim=10000):
    """
    Simula una Random Walk Monte Carlo a partire da un valore iniziale.

    Parametri:
    - start_value: valore iniziale (es. concentrazione attuale di NO2)
    - mu: drift medio per passo (default 0)
    - sigma: deviazione standard del rumore (default 1)
    - n_steps: numero di giorni/passi da simulare
    - n_sim: numero di simulazioni da generare

    Ritorna:
    - array (n_sim, n_steps) con le simulazioni
    """
    simulations = np.zeros((n_sim, n_steps))
    for i in range(n_sim):
        noise = np.random.normal(loc=mu, scale=sigma, size=n_steps)
        simulations[i] = np.cumsum(noise) + start_value
    return simulations


def plot_random_walk(simulations, title="Random Walk Monte Carlo", ylabel="Valore simulato"):
    """
    Plotta i risultati della simulazione random walk.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(simulations[:100].T, color="lightgray", alpha=0.3, label="Simulazioni")
    plt.plot(simulations.mean(axis=0), color="red", linewidth=2, label="Media")
    plt.title(title)
    plt.xlabel("Giorni futuri")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
