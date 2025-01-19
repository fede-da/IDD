import csv

import pandas as pd
import recordlinkage
from recordlinkage.preprocessing import clean
from itertools import combinations

# 1) Caricamento dei dati
# ------------------------

# Ground truth (informazioni su coppie di record duplicati o meno)
#df_ground_truth = pd.read_csv('../../../data/processed/prove/ground_truth_base.csv')

# Carica il dataset delle aziende
df_companies = pd.read_csv('../../../data/processed/prove/tabella_risultante_raffinata.csv')
# Imposta l'indice del DataFrame come ID dei record.
# Assumiamo che l'indice attuale corrisponda a record_id. Se necessario, converti in stringa.
df_companies.index = df_companies.index.map(str)

sim_cap = 0.1

# Carica i blocchi dal file CSV
blocks_df = pd.read_csv('../../../data/processed/prove/trigram_blocs.csv')
blocks = {}
for _, row in blocks_df.iterrows():
    block_id = row['block_id']
    record_ids = row['record_ids'].split(';')
    # Rimuovi eventuali stringhe vuote che possono derivare da separatori finali
    record_ids = [rid for rid in record_ids if rid]
    blocks[block_id] = record_ids

# Definisci il comparatore con i campi di interesse
compare = recordlinkage.Compare()

# Esempio di configurazione della comparazione:
# Confronta il nome dell'azienda con Jaro-Winkler
compare.string('CompanyName', 'CompanyName', method='levenshtein', label='CompanyName')
# Confronta MarketCap in maniera numerica (se appropriato)
compare.numeric('MarketCap', 'MarketCap', method='gauss', scale=1, label='MarketCap')
# Confronta esattamente il numero di dipendenti
compare.exact('EmployeesTotalAmount', 'EmployeesTotalAmount', label='EmployeesTotalAmount')

# Lista per raccogliere tutti i match trovati
all_matches = []

# Itera su ciascun blocco
for block_id, record_ids in blocks.items():
    if len(record_ids) < 2:
        continue  # Se il blocco ha meno di due record, non serve confrontare

    # Seleziona i record del blocco
    subset = df_companies.loc[df_companies.index.intersection(record_ids)]

    # Genera tutte le possibili coppie di record all'interno del blocco
    candidate_pairs = list(combinations(subset.index, 2))
    if not candidate_pairs:
        continue

    # Crea un MultiIndex per le coppie candidate
    candidate_index = pd.MultiIndex.from_tuples(candidate_pairs, names=['_left', '_right'])

    # Calcola le caratteristiche per le coppie candidate
    features = compare.compute(candidate_index, subset, subset)

    # Calcola la media delle similarità per ciascuna coppia
    mean_scores = features.mean(axis=1)

    # Seleziona le coppie che superano la soglia di 0.8
    matches = mean_scores[mean_scores >= sim_cap].index.tolist()

    # Aggiungi i match trovati alla lista complessiva
    all_matches.extend(matches)

# Stampa i match trovati
print("Coppie di record che superano la soglia di similarità " + str(sim_cap) + ":")

output_file = '../../../data/processed/prove/trigram_record_linkage.csv'
with open(output_file, mode='w', newline='', encoding='utf-8') as file_csv:
    writer = csv.writer(file_csv)

    # Scrivo ogni tupla come riga nel CSV
    for tupla in all_matches:
        writer.writerow(tupla)

print(f"Salvate come {output_file}")
