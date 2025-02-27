import csv
from collections import defaultdict
from typing import Dict, Any

# Sostituisci con il percorso del tuo file CSV
input_file = '../../../data/processed/bigrams_temp.csv'

row: Dict[str, Any]
inverted_index = defaultdict(set)  # Uso set per evitare duplicati

# Leggi il file CSV e popola l'indice inverso
with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        bigram = row['bigram']
        record_id = row['record_id']
        inverted_index[bigram].add(record_id)

with open('../../../data/processed/bigram_inverted_index.csv', mode='w', newline='', encoding='utf-8') as outfile:
    # Definisci i campi per il writer
    fieldnames = ['bigram', 'record_ids']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for bigram, record_ids in inverted_index.items():
        # Uniamo gli id in una singola stringa separata da punti e virgola
        writer.writerow({
            'bigram': bigram,
            'record_ids': ';'.join(sorted(record_ids))
        })

print(f"Indice inverso salvato in {'../../../data/processed/bigram_inverted_index.csv'}")