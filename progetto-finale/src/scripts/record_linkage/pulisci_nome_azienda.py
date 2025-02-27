import pandas as pd
import numpy as np
import os
import re

def pulisci_nome_azienda(nome):
    if pd.isna(nome):
        return np.nan
    nome_pulito = nome.upper()

    suffissi = [' INC', ' LLC', ' LTD', ' CORPORATION', ' CORP', ' LIMITED', ' CO', ' PLC', ' S.A.', ' S.A']
    for suffisso in suffissi:
        if nome_pulito.endswith(suffisso):
            nome_pulito = nome_pulito.replace(suffisso, '')
            break

    return nome_pulito.strip()

def normalizza_marketcap(marketcap):
    if pd.isna(marketcap):
        return np.nan

    marketcap_pulito = re.sub(r'[^\d.,]', '', str(marketcap)).strip()
    if marketcap_pulito.count('.') > 1 and marketcap_pulito.count(',') == 0:
        marketcap_pulito = marketcap_pulito.replace('.', '')
    elif marketcap_pulito.count(',') > 1 and marketcap_pulito.count('.') == 0:
        marketcap_pulito = marketcap_pulito.replace(',', '')
    elif '.' in marketcap_pulito and ',' in marketcap_pulito:
        marketcap_pulito = marketcap_pulito.replace(',', '')
    else:
        marketcap_pulito = marketcap_pulito.replace(',', '.')

    try:
        return float(marketcap_pulito)
    except ValueError:
        return np.nan

def gestisci_valori_mancanti(df):
    # Qui potresti imputare o semplicemente lasciare i NaN
    return df

def pulisci_e_raffinata_dati(percorso_input, percorso_output):
    try:
        df = pd.read_csv(percorso_input)
        print(f"File '{percorso_input}' caricato con successo.")
    except Exception as e:
        print(f"Errore nel caricamento del file '{percorso_input}': {e}")
        return

    # Se non esiste alcuna colonna 'record_id', la creo in base all'indice
    if 'record_id' not in df.columns:
        df['record_id'] = df.index
        print("Colonna 'record_id' creata con l'indice di ogni riga (perché non esisteva).")
    else:
        print("Colonna 'record_id' trovata: non viene sovrascritta.")

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

    # Rimuovi eventuali duplicati
    initial_count = len(df)
    df.drop_duplicates(inplace=True)
    final_count = len(df)
    print(f"Rimosso {initial_count - final_count} duplicati.")

    # Salva in un nuovo CSV
    try:
        df.to_csv(percorso_output, index=False)
        df.to_csv(percorso_output2, index=False)
        print(f"File pulito e raffinato salvato come '{percorso_output}'.")
    except Exception as e:
        print(f"Errore nel salvataggio del file '{percorso_output}': {e}")

if __name__ == "__main__":
    percorso_input = '../../../data/processed/tabella_risultante.csv'
    percorso_output = '../../../data/processed/tabella_risultante_raffinata.csv'
    percorso_output2 = '../../../data/processed/prove/tabella_risultante_raffinata.csv'
    pulisci_e_raffinata_dati(percorso_input, percorso_output)