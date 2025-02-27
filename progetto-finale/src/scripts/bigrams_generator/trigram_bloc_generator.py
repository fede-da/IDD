import csv
from typing import Dict, Any


class UnionFind:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, item):
        # Trova il "genitore" radice del set a cui appartiene l'item
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, item1, item2):
        # Unisce i set di item1 e item2
        root1 = self.find(item1)
        root2 = self.find(item2)

        if root1 == root2:
            return

        # Unione per rango per bilanciare l'albero
        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
        else:
            self.parent[root2] = root1
            self.rank[root1] += 1

    def add(self, item):
        # Aggiunge un nuovo elemento se non esiste già
        if item not in self.parent:
            self.parent[item] = item
            self.rank[item] = 0


# File di input
input_file = '../../../data/processed/trigram_inverted_index.csv'

# Inizializza la struttura UnionFind
uf = UnionFind()

# Leggi il file degli indici inversi e unisci i record
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    row: Dict[str, Any]
    for row in reader:
        # Estrai la lista di record_ids dal campo "record_ids"
        record_ids = row['record_ids'].split(';')
        if len(record_ids) > 22:
            continue
        else:

            # Aggiungi ogni record_id all'union-find se non presente
            for rid in record_ids:
                uf.add(rid)

            # Esegui union tra tutti i record in questo gruppo
            # Uniamo il primo record con ciascuno degli altri per collegarli tutti
            if record_ids:
                base = record_ids[0]
                for other in record_ids[1:]:
                    uf.union(base, other)

# Raggruppa i record per componente connessa
blocks = {}
for record in uf.parent.keys():
    root = uf.find(record)
    if root not in blocks:
        blocks[root] = set()
    blocks[root].add(record)

# Converti i blocchi in una lista di insiemi
block_list = list(blocks.values())

# Stampa o salva i risultati
print("Numero di blocchi trovati:", len(block_list))
for i, block in enumerate(block_list):
    print(f"Blocco {i}: {block}")

# Se desideri salvare i blocchi su file CSV:
output_file = '../../../data/processed/trigram_blocs.csv'
with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['block_id', 'record_ids'])
    for i, block in enumerate(block_list):
        writer.writerow([i, ';'.join(sorted(block))])

print(f"Blocchi salvati in {output_file}")