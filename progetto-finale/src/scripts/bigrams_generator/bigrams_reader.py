import csv

def generate_pairs_from_sorted(input_sorted_csv, output_ground_truth_csv):
    """
    Legge in streaming 'input_sorted_csv' (ordinato per bigram) e produce
    un CSV 'output_ground_truth_csv' con colonne [record_id_1, record_id_2, is_duplicate].
    Segna 'FALSE' di default.
    """
    with open(input_sorted_csv, 'r', encoding='utf-8') as fin, \
         open(output_ground_truth_csv, 'w', encoding='utf-8') as fout:

        reader = csv.reader(fin)
        writer = csv.writer(fout)
        # Scriviamo l'header del file di output
        writer.writerow(['record_id_1', 'record_id_2', 'is_duplicate'])

        # Aspettandoci l'header bigram,record_id sulla prima riga
        header = next(reader)
        if header != ['bigram','record_id']:
            raise ValueError("Il file non ha le colonne attese ['bigram','record_id']")

        current_bigram = None
        current_ids = []

        for row in reader:
            bg, rec_id_str = row
            rec_id = int(rec_id_str)

            if bg != current_bigram:
                # Se siamo passati a un nuovo bigramma, generiamo le coppie per quello precedente
                if current_bigram is not None and len(current_ids) > 1:
                    # Tutte le combinazioni
                    for i in range(len(current_ids)):
                        for j in range(i + 1, len(current_ids)):
                            writer.writerow([current_ids[i], current_ids[j], 'FALSE'])

                # Ora resettiamo per il nuovo bigram
                current_bigram = bg
                current_ids = [rec_id]
            else:
                # Stesso bigramma, aggiungo rec_id alla lista
                current_ids.append(rec_id)

        # Fine file: non dimenticare l'ultimo gruppo
        if current_bigram is not None and len(current_ids) > 1:
            for i in range(len(current_ids)):
                for j in range(i + 1, len(current_ids)):
                    writer.writerow([current_ids[i], current_ids[j], 'FALSE'])

    print(f"Creato il file {output_ground_truth_csv} con coppie (record_id_1, record_id_2).")


generate_pairs_from_sorted("./bigrams_temp_sorted.csv", "./ground_truth_base.csv")

