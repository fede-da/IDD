import pandas as pd
import numpy as np
import os
import re

def pulisci_nome_azienda(nome):
    """
    Pulisce e normalizza il nome dell'azienda:
    - Converte in maiuscolo.
    - Rimuove suffissi come 'Inc', 'LLC', 'Ltd', ecc.
    - Rimuove eventuali caratteri speciali extra.
    """
    if pd.isna(nome):
        return np.nan

    # Converti in maiuscolo
    nome_pulito = nome.upper()

    # Lista di suffissi da rimuovere
    suffissi = [' INC', ' LLC', ' LTD', ' CORPORATION', ' CORP', ' LIMITED', ' CO', ' PLC', ' S.A.', ' S.A']

    # Rimuovi i suffissi
    for suffisso in suffissi:
        if nome_pulito.endswith(suffisso):
            nome_pulito = nome_pulito.replace(suffisso, '')
            break  # Rimuovi solo uno suffisso alla volta

    # Rimuovi eventuali spazi in eccesso
    nome_pulito = nome_pulito.strip()

    return nome_pulito

def normalizza_marketcap(marketcap):
    """
    Normalizza il valore di MarketCap:
    - Rimuove eventuali simboli di valuta.
    - Gestisce diverse rappresentazioni numeriche (es. "8.192" -> 8192).
    - Converte in formato float.
    """
    if pd.isna(marketcap):
        return np.nan

    # Rimuovi simboli di valuta e spazi
    marketcap_pulito = re.sub(r'[^\d.,]', '', str(marketcap)).strip()

    # Controlla se usa la virgola come decimale o come separatore delle migliaia
    # Supponiamo che se c'è solo un punto o una virgola, sia il decimale
    # Se ci sono entrambi, la virgola è il separatore delle migliaia e il punto il decimale
    if marketcap_pulito.count('.') > 1 and marketcap_pulito.count(',') == 0:
        # Molto probabile che siano separatori delle migliaia
        marketcap_pulito = marketcap_pulito.replace('.', '')
    elif marketcap_pulito.count(',') > 1 and marketcap_pulito.count('.') == 0:
        # Molto probabile che siano separatori delle migliaia
        marketcap_pulito = marketcap_pulito.replace(',', '')
    elif '.' in marketcap_pulito and ',' in marketcap_pulito:
        # Supponiamo che la virgola sia il separatore delle migliaia e il punto il decimale
        marketcap_pulito = marketcap_pulito.replace(',', '')
    else:
        # Sostituisci la virgola con il punto per standardizzare
        marketcap_pulito = marketcap_pulito.replace(',', '.')

    try:
        valore = float(marketcap_pulito)
    except ValueError:
        valore = np.nan

    return valore

def gestisci_valori_mancanti(df):
    """
    Gestisce i valori mancanti nel DataFrame.
    - Per 'EmployeesTotalAmount', si potrebbe decidere di imputare con la mediana o lasciare NaN.
    - Qui, semplicemente segnaliamo la presenza di NaN.
    """
    # Puoi personalizzare questa funzione per imputare valori se necessario
    # Ad esempio, per imputare con la mediana:
    # df['EmployeesTotalAmount'].fillna(df['EmployeesTotalAmount'].median(), inplace=True)
    return df

def pulisci_e_raffinata_dati(percorso_input, percorso_output):
    """
    Esegue la pulitura e il raffinamento dei dati dal file CSV di input e salva il risultato.

    :param percorso_input: Percorso del file CSV di input (tabella_risultante.csv).
    :param percorso_output: Percorso del file CSV di output (tabella_risultante_raffinata.csv).
    """
    try:
        # Leggi il file CSV
        df = pd.read_csv(percorso_input)
        print(f"File '{percorso_input}' caricato con successo.")
    except Exception as e:
        print(f"Errore nel caricamento del file '{percorso_input}': {e}")
        return

    # Pulisci la colonna 'CompanyName'
    if 'CompanyName' in df.columns:
        df['CompanyName'] = df['CompanyName'].apply(pulisci_nome_azienda)
        print("Colonna 'CompanyName' pulita e normalizzata.")
    else:
        print("La colonna 'CompanyName' non è presente nel DataFrame.")

    # Normalizza la colonna 'MarketCap'
    if 'MarketCap' in df.columns:
        df['MarketCap'] = df['MarketCap'].apply(normalizza_marketcap)
        print("Colonna 'MarketCap' normalizzata.")
    else:
        print("La colonna 'MarketCap' non è presente nel DataFrame.")

    # Gestisci i valori mancanti
    df = gestisci_valori_mancanti(df)
    print("Valori mancanti gestiti.")

    # Opzionale: Rimuovi eventuali duplicati
    initial_count = len(df)
    df.drop_duplicates(inplace=True)
    final_count = len(df)
    print(f"Rimosso {initial_count - final_count} duplicati.")

    # Salva il DataFrame pulito in un nuovo file CSV
    try:
        df.to_csv(percorso_output, index=False)
        print(f"File pulito e raffinato salvato come '{percorso_output}'.")
    except Exception as e:
        print(f"Errore nel salvataggio del file '{percorso_output}': {e}")

if __name__ == "__main__":
    # Specifica il percorso del file CSV di input
    percorso_input = '../../../data/processed/tabella_risultante.csv'

    # Specifica il percorso del file CSV di output
    percorso_output = '../../../data/processed/tabella_risultante_raffinata.csv'

    # Esegui la pulizia e il raffinamento dei dati
    pulisci_e_raffinata_dati(percorso_input, percorso_output)