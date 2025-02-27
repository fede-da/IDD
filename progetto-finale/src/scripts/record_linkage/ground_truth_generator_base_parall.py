import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from concurrent.futures import ProcessPoolExecutor
from itertools import combinations

# Carica i dati
df = pd.read_csv('../../../data/processed/tabella_risultante_raffinata.csv')

# Se non esiste già una colonna 'record_id', la crei usando l'indice:
if 'record_id' not in df.columns:
    df['record_id'] = df.index

# Funzione per estrarre bigrammi
def bigrams(name):
    vec = CountVectorizer(analyzer='char', ngram_range=(2, 2))
    bg_matrix = vec.fit_transform([name])  # generiamo i bigrammi
    bg_list = vec.get_feature_names_out()  # vettore di bigrammi
    return set(bg_list)

# Applica bigram blocking
df['bigrams'] = df['CompanyName'].apply(bigrams)

# Dizionario { bigramma : [ lista di record_id che contengono questo bigramma ] }
blocks = {}
for i, row in df[['record_id', 'bigrams']].iterrows():
    rec_id = row['record_id']
    bigs = row['bigrams']
    for bg in bigs:
        blocks.setdefault(bg, []).append(rec_id)

# Funzione per calcolare le coppie di duplicati per un blocco
def compute_duplicates_for_block(block):
    """Data una lista di record_id in un blocco, genera tutte le coppie possibili."""
    return [(i, j, 'FALSE') for i, j in combinations(block, 2)]

# Filtra i blocchi con più di un elemento
blocks_to_process = [block for block in blocks.values() if len(block) > 1]

# Utilizza un ProcessPoolExecutor per processare i blocchi in parallelo
duplicates = []
with ProcessPoolExecutor() as executor:
    # Mappa la funzione sui blocchi da processare
    results = executor.map(compute_duplicates_for_block, blocks_to_process)
    # Estrai i risultati
    for sublist in results:
        duplicates.extend(sublist)

# Crea un DataFrame per il risultato
result_df = pd.DataFrame(duplicates, columns=['record_id_1', 'record_id_2', 'is_duplicate'])

# Salva il risultato in un nuovo CSV
result_df.to_csv('../../../data/processed/ground_truth_base.csv', index=False)
result_df.to_csv('../../../data/processed/prove/ground_truth_base.csv', index=False)