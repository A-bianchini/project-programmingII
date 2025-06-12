import pandas as pd
import os

def load_dataset(nome_file, sottocartella, stazione_singola=False):
    """
    Carica un dataset CSV dalla cartella 'data'.

    - nome_file: nome base del file senza estensione (es. 'O3_media')
    - sottocartella: 'media', 'all', oppure una delle sottocartelle in 'stazioni_singole'
    - stazione_singola: se True, cerca dentro 'data/stazioni_singole/sottocartella/'

    Esempi:
        load_dataset("O3_media", "media")
        load_dataset("BIASCA_traffic_only", "traffic_only", stazione_singola=True)
    """
    base_dir = os.path.dirname(__file__)

    # Se è una stazione singola, il nome del file deve includere la stazione
    if stazione_singola:
        # Se il nome del file contiene già la stazione, non la ripetiamo
        filename = f"{nome_file}.csv"
        sub_path = os.path.join("data", "stazioni singole", sottocartella)
    else:
        filename = f"{nome_file}.csv"
        sub_path = os.path.join("data", sottocartella)

    # Costruisce il percorso completo al file CSV
    path = os.path.join(base_dir, sub_path, filename)

    # Aggiungi un print per vedere il percorso
    print(f"Percorso generato: {path}")

    # Controlla se il file esiste
    if not os.path.exists(path):
        raise FileNotFoundError(f"File non trovato: {path}")

    return pd.read_csv(path)

