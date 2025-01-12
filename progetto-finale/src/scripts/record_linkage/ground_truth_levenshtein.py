import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import numpy as np

from src.utils.timer import Timer


# Funzione per calcolare la distanza di Levenshtein
def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


# Carica i dati
df = pd.read_csv('../../../data/processed/tabella_risultante_raffinata.csv')


# Funzione per estrarre bigrammi
def bigrams(name):
    vec = CountVectorizer(analyzer='char', ngram_range=(2, 2))
    bg_matrix = vec.fit_transform([name])
    bigrams = vec.get_feature_names_out()
    return set(bigrams)


# Applica bigram blocking
df['bigrams'] = df['CompanyName'].apply(bigrams)
blocks = {}
print("Start applying bigram blocks")
for idx, bigs in enumerate(df['bigrams']):
    for bg in bigs:
        if bg in blocks:
            blocks[bg].append(idx)
        else:
            blocks[bg] = [idx]
print("Bigram blocks application completed")
timer = Timer()
timer.start()
# Confronta i record all'interno di ogni blocco
total_pairs = sum(len(b) * (len(b) - 1) / 2 for b in blocks.values())
current_pair = 0
duplicates = []
for block in blocks.values():
    if len(block) > 1:
        for i in range(len(block)):
            for j in range(i + 1, len(block)):
                # Calcola la distanza di Levenshtein tra i nomi delle aziende
                lev_distance = levenshtein(df['CompanyName'].iloc[block[i]], df['CompanyName'].iloc[block[j]])
                # Considera duplicati se la distanza è minore o uguale a 2
                is_duplicate = 'TRUE' if lev_distance <= 2 else 'FALSE'
                duplicates.append((block[i], block[j], is_duplicate))
                current_pair += 1
                print(f"Processed block {current_pair} of {total_pairs} ({current_pair / total_pairs * 100:.2f}%)")
timer.stop()
print(f"Blocks pairwise completed in {timer.get_elapsed_time()}")

# Crea un DataFrame per il risultato
result_df = pd.DataFrame(duplicates, columns=['record_id_1', 'record_id_2', 'is_duplicate'])

# Salva il risultato in un nuovo CSV
result_df.to_csv('../../../data/processed/ground_truth_lev.csv', index=False)
