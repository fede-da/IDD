import csv
from typing import Dict, Any

import pandas as pd

# ==============================================================
# 1) Caricamento dei dataset e dei match
# ==============================================================

old_file = 'vecchie_aziende.csv'
new_file = 'nuove_aziende.csv'
matches_file = 'matches_old_new.csv'
output_fused = 'fused_companies.csv'

df_old = pd.read_csv(old_file)
df_new = pd.read_csv(new_file)

# Assicuriamoci che gli indici siano coerenti con quelli usati nello script di RL
df_old.index = df_old.index.map(str)
df_new.index = df_new.index.map(lambda x: "NEW_" + str(x))

# Leggiamo i match
matches = []
with open(matches_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row: Dict[str, Any]
        old_id = row['old_record_id']
        new_id = row['new_record_id']
        matches.append((old_id, new_id))

# ==============================================================
# 2) Data Fusion: per ogni coppia (old_id, new_id),
#    prendiamo i campi extra da df_new e li aggiungiamo a df_old.
# ==============================================================

# Prima scopriamo quali colonne extra ha df_new rispetto a df_old
old_cols = set(df_old.columns)
new_cols = set(df_new.columns)
extra_cols = new_cols - old_cols  # quelle che non esistevano prima
print("Colonne extra da fondere:", extra_cols)

# Opzione 1: aggiungiamo al volo le colonne mancanti a df_old
for col in extra_cols:
    df_old[col] = None  # o np.nan

# Adesso, per ogni match, copiamo i valori nuovi sul record corrispondente
for (oid, nid) in matches:
    if oid in df_old.index and nid in df_new.index:
        # Prendiamo i valori dal nuovo
        for col in extra_cols:
            df_old.loc[oid, col] = df_new.loc[nid, col]

# ==============================================================
# 3) Salvataggio del DataFrame fuso
# ==============================================================

df_old.to_csv(output_fused, index=True)
print(f"Data fusion completata. File salvato in {output_fused}")