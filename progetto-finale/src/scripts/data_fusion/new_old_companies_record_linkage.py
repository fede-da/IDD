import csv
import pandas as pd
import recordlinkage
from itertools import combinations

# ==============================================================
# 1) Caricamento dei dataset (vecchio e nuovo)
# ==============================================================

old_file = '../../../data/processed/prove/tabella_risultante_raffinata.csv'  # file CSV con gli attributi originali
new_file = 'nuove_aziende.csv'  # file CSV con stessi record ma attributi aggiuntivi
blocks_file_old = 'bigram_blocks_old.csv'  # blocchi (bigram) per il vecchio file
blocks_file_new = 'bigram_blocks_new.csv'  # blocchi (bigram) per il nuovo file
output_matches = 'matches_old_new.csv'  # risultati di matching

df_old = pd.read_csv(old_file)
df_new = pd.read_csv(new_file)

# Assegniamo un indice univoco a ciascun record
df_old.index = df_old.index.map(str)
df_new.index = df_new.index.map(lambda x: "NEW_" + str(x))


# (Così evitiamo conflitti di ID tra i due dataset, distinguendo record “nuovi” da “vecchi”.)

# ==============================================================
# 2) Caricamento e unione blocchi bigrammi
#    (Qui semplifichiamo: usiamo stessi script di generazione bigrammi
#     e creiamo un meccanismo per incrociare i blocchi fra i due file)
# ==============================================================

def load_blocks(blocks_csv):
    """
    Carica un file CSV del tipo:
    block_id, record_ids
    0,1;2;100
    ...
    Restituisce un dizionario { block_id -> [lista di record_id] }
    """
    blocks_dict = {}
    df_blocks = pd.read_csv(blocks_csv)
    for _, row in df_blocks.iterrows():
        bid = row['block_id']
        rids = row['record_ids'].split(';')
        rids = [r for r in rids if r]  # rimuovi stringhe vuote
        blocks_dict[bid] = rids
    return blocks_dict


blocks_old = load_blocks(blocks_file_old)
blocks_new = load_blocks(blocks_file_new)

# ==============================================================
# 3) Creazione dei blocchi “incrociati”
#    Idea: se un bigramma compare nel file vecchio e in quello nuovo,
#    allora potenzialmente quei record corrispondono e verranno confrontati.
# ==============================================================

# Esempio semplificato: usiamo come “chiave del blocco” l’indice numerico
# e verifichiamo le intersezioni

# Creiamo un dizionario bigramma -> (lista old, lista new)
# (Se i file di block_id e bigram differiscono, andranno adattati.)
from collections import defaultdict

bigram_to_old = defaultdict(list)
bigram_to_new = defaultdict(list)

# Immaginiamo che "block_id" corrisponda in realtà al testo del bigram.
# Se invece è un ID numerico, andrebbe ricollegato al bigram originale.
# Qui assumiamo una corrispondenza diretta, altrimenti servirebbe
# un passaggio aggiuntivo.

for b_id, recs in blocks_old.items():
    # b_id potrebbe essere un intero o la stringa del bigram.
    # Se b_id è effettivamente il bigram, va bene.
    # Se no, va modificato per recuperare il bigram.
    bigram_to_old[b_id].extend(recs)

for b_id, recs in blocks_new.items():
    bigram_to_new[b_id].extend(recs)

# Adesso costruiamo “blocchi incrociati”
cross_blocks = []
for bigram, old_records in bigram_to_old.items():
    if bigram in bigram_to_new:
        new_records = bigram_to_new[bigram]
        # Se old_records e new_records non sono vuoti, generiamo un “blocco incrociato”
        if old_records and new_records:
            cross_blocks.append((bigram, old_records, new_records))

# ==============================================================
# 4) Definisci il comparatore (Record Linkage)
#    Confrontiamo i campi in comune (es. CompanyName, MarketCap).
# ==============================================================

compare = recordlinkage.Compare()
compare.string('CompanyName', 'CompanyName', method='levenshtein', label='CompanyName')
compare.numeric('MarketCap', 'MarketCap', method='gauss', scale=1, label='MarketCap')
# ecc... altri campi in comune
sim_threshold = 0.2  # soglia di matching (regolabile)

# ==============================================================
# 5) Esegui il pairwise matching tra old_records e new_records
#    di ciascun blocco
# ==============================================================

all_matches = []

for bigram, old_rids, new_rids in cross_blocks:
    # Estrae i subset dal df_old e df_new
    subset_old = df_old.loc[df_old.index.intersection(old_rids)]
    subset_new = df_new.loc[df_new.index.intersection(new_rids)]

    if subset_old.empty or subset_new.empty:
        continue

    # Creiamo l’indice candidato tra i record old e new
    # (ogni coppia (r_old, r_new))
    indexer = recordlinkage.Index()
    indexer.full()  # crea la lista di tutte le possibili coppie
    candidate_links = indexer.index(subset_old, subset_new)

    # Calcola le features
    features = compare.compute(candidate_links, subset_old, subset_new)

    # Calcola la media di tutte le similarità
    mean_scores = features.mean(axis=1)

    # Trova le coppie con media >= soglia
    matched_pairs = mean_scores[mean_scores >= sim_threshold].index.tolist()

    # Salva i match (left_index, right_index)
    for (left_id, right_id) in matched_pairs:
        # left_id appartiene a subset_old, right_id a subset_new
        all_matches.append((left_id, right_id))

# ==============================================================
# 6) Salvataggio dei match trovati
# ==============================================================

with open(output_matches, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['old_record_id', 'new_record_id'])
    for pair in all_matches:
        writer.writerow(pair)

print(f"Salvati {len(all_matches)} match in {output_matches}")