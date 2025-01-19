import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

from src.utils.timer import Timer


def extract_trigrams(text):
    """
    Restituisce l'insieme dei trigrammi in una stringa.
    Se la stringa è vuota o non valida, restituisce un insieme vuoto.
    """
    # Verifica che text sia una stringa non vuota
    if not isinstance(text, str) or not text.strip():
        return set()
    vec = CountVectorizer(analyzer='char', ngram_range=(3, 3))
    # Prova a generare i trigrammi. Se fallisce, restituisce un insieme vuoto.
    try:
        vec.fit([text])
        return set(vec.get_feature_names_out())
    except ValueError:
        # Gestisce casi in cui CountVectorizer non trovi trigrammi
        return set()

def create_trigrams_csv(companies_csv, output_csv, chunksize=10000):
    """
    Legge 'companies_csv' a chunk, produce un CSV 'output_csv' con due colonne: [trigram, record_id].
    """
    # Apriamo un file CSV in modalità scrittura, scrivendo l'intestazione una volta sola
    with open(output_csv, 'w', encoding='utf-8') as f_out:
        f_out.write("trigram,record_id\n")  # intestazione

    # Leggiamo il CSV di input a chunk
    chunk_iter = pd.read_csv(companies_csv, chunksize=chunksize)
    for df_chunk in chunk_iter:
        # Se 'record_id' non esiste nella colonna, la creiamo con l'indice
        if 'record_id' not in df_chunk.columns:
            df_chunk['record_id'] = df_chunk.index

        # Assicuriamoci che 'CompanyName' sia trattato correttamente anche in caso di NaN
        if 'CompanyName' not in df_chunk.columns:
            print("Colonna 'CompanyName' non trovata nel chunk corrente.")
            continue

        # Rimpiazza eventuali NaN in 'CompanyName' con stringhe vuote
        df_chunk['CompanyName'] = df_chunk['CompanyName'].replace({np.nan: ''})

        # Calcoliamo i trigrammi per ciascuna riga del chunk
        rows_to_append = []
        for _, row in df_chunk[['record_id', 'CompanyName']].iterrows():
            rec_id = row['record_id']
            trigrams_set = extract_trigrams(row['CompanyName'])
            for tg in trigrams_set:
                rows_to_append.append((tg, rec_id))

        # Scriviamo i dati estratti nel file di output, aggiungendo nuove righe
        if rows_to_append:  # scrivi solo se ci sono dati
            df_temp = pd.DataFrame(rows_to_append, columns=['trigram', 'record_id'])
            df_temp.to_csv(output_csv, mode='a', header=False, index=False)
            # Se necessario, crea anche un file temporaneo
            df_temp.to_csv('./trigrams_temp.csv', mode='a', header=False, index=False)

    print(f"Creato il file {output_csv} con coppie (trigram, record_id).")


t = Timer()
t.start()
create_trigrams_csv('../../../data/processed/tabella_risultante.csv', '../../../data/processed/trigrams_temp.csv')
t.stop()
