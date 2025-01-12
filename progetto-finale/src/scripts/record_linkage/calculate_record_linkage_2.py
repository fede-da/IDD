import pandas as pd
import recordlinkage
from recordlinkage.classifiers import LogisticRegressionClassifier
from recordlinkage import precision, recall, fscore


def main():
    # 1) Caricamento dei dati
    # -------------------------------------------------------
    # Carica la ground truth (colonne: record_id_1, record_id_2, is_duplicate)
    df_ground_truth = pd.read_csv('../../../data/processed/prove/ground_truth_base.csv')
    # Carica il dataset di compagnie (colonne: record_id, CompanyName, MarketCap, EmployeesTotalAmount, ...)
    df_companies = pd.read_csv('../../../data/processed/prove/tabella_risultante_raffinata.csv')

    # Converti in float le colonne numeriche e gestisci i NaN
    df_companies['MarketCap'] = pd.to_numeric(df_companies['MarketCap'], errors='coerce').fillna(0)
    df_companies['EmployeesTotalAmount'] = pd.to_numeric(df_companies['EmployeesTotalAmount'], errors='coerce').fillna(0)

    # Imposta record_id come indice (se non lo è già)
    if 'record_id' in df_companies.columns:
        df_companies.set_index('record_id', inplace=True)

    print("Ground Truth:\n", df_ground_truth.head())
    print("Companies:\n", df_companies.head())

    # 2) Creazione delle coppie candidate (blocking)
    # -------------------------------------------------------
    # In questo esempio usiamo block('CompanyName') → matching esatto sul nome,
    # se vuoi un blocking più "elastico", valuta n-gram blocking
    indexer = recordlinkage.Index()
    indexer.block('CompanyName')
    candidate_links = indexer.index(df_companies)

    # 3) Confronto dei campi (Compare) per calcolare le feature
    # -------------------------------------------------------
    compare = recordlinkage.Compare()

    compare.string('CompanyName', 'CompanyName',
                   method='levenshtein', threshold=0.8,
                   label='cmp_CompanyName')

    compare.numeric('MarketCap', 'MarketCap',
                    method='gauss', offset=1, scale=0.1,
                    label='cmp_MarketCap')

    compare.numeric('EmployeesTotalAmount', 'EmployeesTotalAmount',
                    method='gauss', offset=1, scale=1,
                    label='cmp_Employees')

    # Calcoliamo le feature su tutte le coppie candidate
    features = compare.compute(candidate_links, df_companies)
    # Imposta i nomi dei livelli dell'indice
    features.index.names = ['record_id_1', 'record_id_2']

    # 4) Creazione di ground_truth_series come Series indicizzata
    # -------------------------------------------------------
    #   con MultiIndex (record_id_1, record_id_2)
    ground_truth_index = pd.MultiIndex.from_arrays(
        [
            df_ground_truth['record_id_1'],
            df_ground_truth['record_id_2']
        ],
        names=['record_id_1', 'record_id_2']
    )
    # Converti 'is_duplicate' in bool (se serve) e crea la Series
    df_ground_truth['is_duplicate'] = df_ground_truth['is_duplicate'].map({'TRUE': True, 'FALSE': False, 'True': True, 'False': False}).fillna(False)
    ground_truth_series = pd.Series(
        data=df_ground_truth['is_duplicate'].values,
        index=ground_truth_index,
        name='is_duplicate'
    )

    # 5) Unione delle feature con la ground truth
    # -------------------------------------------------------
    # Usiamo un join su indice (MultiIndex): incrocia solo le coppie in comune
    print(features.index)
    print(ground_truth_series.index)

    training_features = features.join(ground_truth_series, how='inner')

    if training_features.empty:
        raise Exception('training_features is empty (nessun match tra features e ground_truth)')

    # Dividiamo i dati: X_train e match_index
    # * In Python Record Linkage Toolkit, "match_index" deve contenere
    #   l'elenco delle coppie vere (True)
    X_train = training_features.drop(columns=['is_duplicate'])
    # Individua i pair con is_duplicate == True
    true_match_index = training_features.index[training_features['is_duplicate'] == True]

    # 6) Addestramento classificatore (supervised)
    # -------------------------------------------------------
    classifier = LogisticRegressionClassifier()
    # In recordlinkage, la firma di fit è (X, match_index)
    # 'match_index' = MultiIndex delle coppie con is_duplicate=True
    classifier.fit(X_train, match_index=true_match_index)

    # 7) Predizione
    # -------------------------------------------------------
    # Predici duplicati su tutte le coppie candidate (features)
    y_pred = classifier.predict(features)

    # 8) Calcolo metriche (Precision, Recall, F-score)
    # -------------------------------------------------------
    # Per valutare, allineiamo la ground truth con y_pred
    common_index = ground_truth_series.index.intersection(y_pred.index)
    if not common_index.empty:
        y_true = ground_truth_series.loc[common_index]
        y_hat = y_pred.loc[common_index]

        p = precision(y_true, y_hat)
        r = recall(y_true, y_hat)
        f = fscore(y_true, y_hat)

        print("Precision:", p)
        print("Recall:", r)
        print("F-score:", f)
    else:
        print("Nessun indice in comune tra ground truth e predizioni: non posso calcolare metriche.")


if __name__ == '__main__':
    main()