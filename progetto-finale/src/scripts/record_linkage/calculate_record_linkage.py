import pandas as pd
import recordlinkage
from recordlinkage import LogisticRegressionClassifier, precision, recall, fscore

# 1) Caricamento dei dati
# ------------------------

# Ground truth (informazioni su coppie di record duplicati o meno)
df_ground_truth = pd.read_csv('../../../data/processed/prove/ground_truth_base.csv')

# Dataset sorgente (lista di aziende con informazioni)
df_companies = pd.read_csv('../../../data/processed/prove/tabella_risultante_raffinata.csv')

# Convertire colonne numeriche e gestire NaN
df_companies['MarketCap'] = pd.to_numeric(df_companies['MarketCap'], errors='coerce').fillna(0)
df_companies['EmployeesTotalAmount'] = pd.to_numeric(df_companies['EmployeesTotalAmount'], errors='coerce').fillna(0)

# Impostare 'record_id' come indice, se presente
if 'record_id' in df_companies.columns:
    df_companies.set_index('record_id', inplace=True)


# Stampa per controllo
print("Ground Truth:\n", df_ground_truth.head())
print("Companies:\n", df_companies.head())

# 3) Creazione dell'indexer con bigram blocking
indexer = recordlinkage.Index()
indexer.block('CompanyName')  # o ngram_block, dipende dalla versione / logica
candidate_links = indexer.index(df_companies)

# 4) Impostazione delle regole di confronto
compare = recordlinkage.Compare()

compare.string('CompanyName', 'CompanyName', method='levenshtein', threshold=0.8,
               label='cmp_CompanyName')

# Ora le colonne MarketCap ed EmployeesTotalAmount sono float
compare.numeric('MarketCap', 'MarketCap',
                method='gauss', offset=1, scale=0.1,
                label='cmp_MarketCap')

compare.numeric('EmployeesTotalAmount', 'EmployeesTotalAmount',
                method='gauss', offset=1, scale=1,
                label='cmp_Employees')

features = compare.compute(candidate_links, df_companies)
features.index.names = ['record_id_1', 'record_id_2']

# 5) Preparazione dei dati di training
ground_truth_index = pd.MultiIndex.from_arrays(
    [df_ground_truth['record_id_1'], df_ground_truth['record_id_2']],
    names=['record_id_1', 'record_id_2']
)
ground_truth_series = pd.Series(
    data=df_ground_truth['is_duplicate'].values,
    index=ground_truth_index,
    name='is_duplicate'
)
ground_truth_series.name = 'is_duplicate'

if len(features) == 0:
    raise Exception('features is empty')

if len(ground_truth_series) == 0:
    raise Exception('ground_truth_series is empty')

# Supponendo che 'features' abbia MultiIndex (record_id_1, record_id_2)
df_features = features.reset_index()  # adesso avrà colonne 'record_id_1', 'record_id_2', 'cmp_CompanyName', etc.

# Anche ground_truth_series ha lo stesso MultiIndex, lo convertiamo in DataFrame
df_ground = ground_truth_series.reset_index()  # avrà colonne 'record_id_1', 'record_id_2', 'is_duplicate'

print("Ground Truth:\n", df_features.head())
print("Companies:\n", df_ground.head())

print("Starting merge\n")

# Unione classica su record_id_1 e record_id_2

training_features = features.join(ground_truth_series, how='inner')

print("Merge completed\n")

# Controlla il risultato
if training_features.empty:
    raise Exception('training_features is empty (anche con merge su colonne)')


X_train = training_features.drop(columns=['is_duplicate'])
y_train = training_features['is_duplicate']

# 6) Addestramento classificatore
classifier = LogisticRegressionClassifier()
# Filtra y_train per ottenere solo le coppie vere (duplicati)
true_matches_index = training_features.index[training_features['is_duplicate']]


# Addestra il classificatore fornendo i comparison_vectors (X_train)
# e l'indice dei match reali
if len(training_features.drop(columns=['is_duplicate'])) == 0:
    raise Exception('X_train is empty')

print("Start training\n")

classifier.fit(X_train, match_index=true_matches_index)
print("Training completed\n")

print("Start predict\n")
# 7) Predizione su tutte le coppie candidate
y_pred = classifier.predict(features)
print("End predict\n")

# 8) Valutazione (se abbiamo la ground truth per le stesse coppie)
common_index = ground_truth_series.index.intersection(y_pred.index)
y_true = ground_truth_series.loc[common_index]
y_hat = y_pred.loc[common_index]

print("Precision:", precision(y_true, y_hat))
print("Recall:", recall(y_true, y_hat))
print("F-score:", fscore(y_true, y_hat))

# 9) Risultati finali
results_df = features.copy()
results_df['pred_duplicate'] = y_pred
print(results_df.head(20))
