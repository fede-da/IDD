import itertools

import pandas as pd
import recordlinkage

# 1) Caricamento dei dati
# ------------------------

# Ground truth (informazioni su coppie di record duplicati o meno)
df_ground_truth = pd.read_csv('../../../data/processed/prove/ground_truth_base.csv')

bigrams_df = pd.read_csv('../../../data/processed/prove/bigrams.csv')

# Dataset sorgente (lista di aziende con informazioni)
df_companies = pd.read_csv('../../../data/processed/prove/tabella_risultante_raffinata.csv')

# Convertire colonne numeriche e gestire NaN
df_companies['MarketCap'] = pd.to_numeric(df_companies['MarketCap'], errors='coerce').fillna(0)
df_companies['EmployeesTotalAmount'] = pd.to_numeric(df_companies['EmployeesTotalAmount'], errors='coerce').fillna(0)

# Stampa per controllo
print("Ground Truth:\n", df_ground_truth.head())
print("Companies:\n", df_companies.head())

# Raggruppa i record per bigramma, ottenendo liste di record_id per ciascun bigramma
bigram_groups = bigrams_df.groupby('bigram')['record_id'].apply(list)

# Insieme per raccogliere tutte le coppie candidate uniche
candidate_pairs = set()

# Per ogni gruppo di record che condividono lo stesso bigramma, genera tutte le combinazioni possibili
for record_ids in bigram_groups:
    if len(record_ids) > 1:
        # Genera combinazioni di coppie per il gruppo
        for pair in itertools.combinations(record_ids, 2):
            # Ordina la coppia per evitare duplicati (come (1,2) e (2,1))
            candidate_pairs.add(tuple(sorted(pair)))

# Crea un MultiIndex da usare come candidate_links in RecordLinkage Toolkit
candidate_links = pd.MultiIndex.from_tuples(list(candidate_pairs))
print("Numero di coppie candidate generate:", len(candidate_links))

# Inizializza l'oggetto Compare
compare = recordlinkage.Compare()

# Calcola le caratteristiche di confronto utilizzando le coppie candidate generate
features = compare.compute(candidate_links, bigrams_df)

print("Feature calcolate per le coppie candidate:")
print(features.head())

# Esempio di soglia: somma delle similarità maggiore di un certo valore
soglia = 1.5
matches = features[features.sum(axis=1) > soglia]

print("Coppie identificate come possibili match:")
print(matches)
