import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

# Carica i dati
df = pd.read_csv('../../../data/processed/tabella_risultante_raffinata.csv')

# Se non esiste già una colonna 'record_id', la crei usando l'indice:
# (Se esiste già, ometti questa riga)
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

# Confronta i record all'interno di ogni blocco
duplicates = []
for block in blocks.values():
    if len(block) > 1:
        # Esempio: se in un blocco ci sono [10, 94, 141],
        # creiamo coppie (10,94), (10,141), (94,141) etc.
        for i in range(len(block)):
            for j in range(i + 1, len(block)):
                # Qui assumiamo che tutti i record nel medesimo blocco siano NON duplicati
                # (o "FALSE") a scopo di esempio. In un caso reale potresti mettere una
                # logica di confronto per stabilire se è "TRUE" o "FALSE".
                duplicates.append((block[i], block[j], 'FALSE'))

# Crea un DataFrame per il risultato
result_df = pd.DataFrame(duplicates, columns=['record_id_1', 'record_id_2', 'is_duplicate'])

# Salva il risultato in un nuovo CSV
result_df.to_csv('../../../data/processed/ground_truth_base.csv', index=False)
result_df.to_csv('../../../data/processed/prove/ground_truth_base.csv', index=False)
