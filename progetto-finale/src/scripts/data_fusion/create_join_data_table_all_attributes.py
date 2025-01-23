import os
import pandas as pd

from src.utils.attributes_map import attributes_local_map


def combina_csv(cartella_sorgente, cartella_destinazione, nome_output="tabella_risultante_compelta_attributi.csv"):
    """
    Combina tutti i file CSV presenti nella cartella_sorgente in un unico file CSV,
    includendo tutte le colonne presenti nei singoli file.

    :param cartella_sorgente: Percorso della cartella contenente i file CSV da combinare.
    :param cartella_destinazione: Percorso della cartella dove salvare il file combinato.
    :param nome_output: Nome del file CSV risultante (default: "tabella_risultante.csv").
    """
    # Lista per memorizzare i DataFrame di ogni file CSV
    lista_df = []
    colonne_attese = {"CompanyName", "MarketCap", "EmployeesTotalAmount"}

    # Itera su tutti i file nella cartella sorgente
    for filename in os.listdir(cartella_sorgente):
        # Verifica se il file ha estensione .csv
        if filename.lower().endswith('.csv'):
            percorso_file = os.path.join(cartella_sorgente, filename)
            try:
                # Leggi il file CSV
                df = pd.read_csv(percorso_file)

                # Se il filename è presente in attributes_local_map, rinominiamo solo le colonne effettivamente presenti
                if filename in attributes_local_map:
                    mapping = attributes_local_map[filename]
                    # Creiamo un rename_dict per le sole colonne esistenti in df
                    rename_dict = {old_col: new_col for old_col, new_col in mapping.items()
                                   if old_col in df.columns}

                    # Se c'è almeno una colonna da rinominare, la rinominiamo
                    if rename_dict:
                        df.rename(columns=rename_dict, inplace=True)

                    # Ora verifichiamo se dopo la rinomina le colonne attese sono presenti
                    if colonne_attese.issubset(df.columns):
                        lista_df.append(df)
                        print(f"File '{filename}' aggiunto con successo (colonne rinominate).")
                    else:
                        print(f"File '{filename}' saltato: colonne mancanti dopo la rinomina.")

                else:
                    # Se il file non è presente nel dizionario, verifichiamo se ha già le colonne attese
                    if colonne_attese.issubset(df.columns):
                        lista_df.append(df)
                        print(f"File '{filename}' aggiunto con successo (nessuna rinomina).")
                    else:
                        print(f"File '{filename}' saltato: colonne mancanti (nessuna rinomina).")

            except Exception as e:
                print(f"Errore nella lettura del file '{filename}': {e}")

    if lista_df:
        # Combina tutti i DataFrame in uno solo, unendo tutte le colonne disponibili
        df_combinato = pd.concat(lista_df, ignore_index=True)

        # Definisci il percorso completo del file di output
        percorso_output = os.path.join(cartella_destinazione, nome_output)

        try:
            # Salva il DataFrame combinato in un nuovo file CSV
            df_combinato.to_csv(percorso_output, index=False)
            print(f"File combinato salvato come '{percorso_output}'.")
        except Exception as e:
            print(f"Errore nel salvataggio del file combinato: {e}")
    else:
        print("Nessun file CSV valido trovato nella cartella sorgente.")


if __name__ == "__main__":
    # Specifica il percorso della cartella contenente i file CSV
    cartella_sorgente = '../../../data/to_process'

    # Specifica il percorso della cartella dove salvare il file combinato
    cartella_destinazione = '../../../data/processed'

    # Chiama la funzione per combinare i file CSV
    combina_csv(cartella_sorgente, cartella_destinazione)