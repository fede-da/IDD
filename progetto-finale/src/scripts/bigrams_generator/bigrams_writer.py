import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

def extract_bigrams(text):
    """
    Restituisce l'insieme dei bigrammi in una stringa.
    """
    if not isinstance(text, str):
        return set()
    vec = CountVectorizer(analyzer='char', ngram_range=(2, 2))
    X = vec.fit_transform([text])
    return set(vec.get_feature_names_out())

def create_bigrams_csv(companies_csv, output_csv, chunksize=10000):
    """
    Legge 'companies_csv' in chunk, produce un CSV 'output_csv' con due colonne: [bigram, record_id].
    """
    # Apriamo un file CSV in append mode, scrivendo di volta in volta
    with open(output_csv, 'w', encoding='utf-8') as f_out:
        f_out.write("bigram,record_id\n")  # intestazione

    # Leggiamo a chunk
    chunk_iter = pd.read_csv(companies_csv, chunksize=chunksize)
    for df_chunk in chunk_iter:
        # Assicurati che la colonna 'record_id' esista, altrimenti la crei
        if 'record_id' not in df_chunk.columns:
            df_chunk['record_id'] = df_chunk.index  # oppure df_chunk.index + offset, se serve

        # Calcola i bigrammi per ognuna delle righe del chunk
        rows_to_append = []
        for _, row in df_chunk[['record_id', 'CompanyName']].iterrows():
            rec_id = row['record_id']
            bigrams_set = extract_bigrams(row['CompanyName'])
            for bg in bigrams_set:
                rows_to_append.append((bg, rec_id))

        # Scriviamo il tutto su file
        df_temp = pd.DataFrame(rows_to_append, columns=['bigram', 'record_id'])
        df_temp.to_csv(output_csv, mode='a', header=False, index=False)
        df_temp.to_csv('./bigrams_temp.csv', mode='a', header=False, index=False)

    print(f"Creato il file {output_csv} con coppie (bigram, record_id).")


create_bigrams_csv('../../../data/processed/tabella_risultante.csv', '../../../data/processed/bigrams_temp.csv')
