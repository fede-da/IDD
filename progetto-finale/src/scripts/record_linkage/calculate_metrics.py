import csv
from typing import Dict, Any


def compute_metrics(predicted_set, gt_set):
    TP = len(predicted_set.intersection(gt_set))
    FP = len(predicted_set - gt_set)
    FN = len(gt_set - predicted_set)
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    return precision, recall, f1

# 1. Leggo la ground truth
gt_duplicates = set()
with open('../../../data/processed/prove/ground_truth.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row: Dict[str, Any]
        rec1 = int(row['record_id_1'])
        rec2 = int(row['record_id_2'])
        is_dup = row['is_duplicate'].strip().upper()
        pair = (min(rec1, rec2), max(rec1, rec2))
        gt_duplicates.add(pair)

# 2. Leggo i match trovati dalla strategia BIGRAMS
predicted_bigrams = set()
with open('../../../data/processed/prove/bigram_record_linkage.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for rec1, rec2 in reader:
        rec1, rec2 = int(rec1), int(rec2)
        pair = (min(rec1, rec2), max(rec1, rec2))
        predicted_bigrams.add(pair)

# 3. Leggo i match trovati dalla strategia TRIGRAMS
predicted_trigrams = set()
with open('../../../data/processed/prove/trigram_record_linkage.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for rec1, rec2 in reader:
        rec1, rec2 = int(rec1), int(rec2)
        pair = (min(rec1, rec2), max(rec1, rec2))
        predicted_trigrams.add(pair)

# 4. Calcolo metriche
precision_bi, recall_bi, f1_bi = compute_metrics(predicted_bigrams, gt_duplicates)
precision_tri, recall_tri, f1_tri = compute_metrics(predicted_trigrams, gt_duplicates)

print("### RISULTATI BIGRAMS ###")
print(f"Precision: {precision_bi:.3f}")
print(f"Recall:    {recall_bi:.3f}")
print(f"F1 Score:  {f1_bi:.3f}")

print("\n### RISULTATI TRIGRAMS ###")
print(f"Precision: {precision_tri:.3f}")
print(f"Recall:    {recall_tri:.3f}")
print(f"F1 Score:  {f1_tri:.3f}")