import csv
from fuzzywuzzy import fuzz, process
from multiprocessing import Pool
import pandas as pd

data = pd.read_csv('destxbuyer.csv', encoding='latin-1')

data.buyer = data.buyer.fillna('no_buyer')
data.dest = data.dest.fillna('no_dest')

dests = []
threshold = 90

for dest in data.dest:
    if dest not in dests:
        dests.append(dest)

print("dests", dests)

grouped = data.groupby(['dest'])


def find_dupes(name_group):
    name, group = name_group
    deduped = []
    buyers = set(group.buyer.tolist())
    while buyers:
        current_buyer = buyers.pop()
        dupes = process.extract(
                current_buyer, buyers,
                scorer=fuzz.token_set_ratio
                )
        filtered = set(x[0] for x in dupes if x[1] > threshold)
        if len(filtered) > 0:
            filtered.add(current_buyer)
        deduped.append(filtered)
        buyers -= filtered
    return (name, deduped)

with open('filtered.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['dest', 'buyer', 'group_id'])

    with Pool() as pool:
        deduped_groups = pool.map(find_dupes, grouped)

    for (name, group) in deduped_groups:
        for (group_id, dups) in enumerate(group):
            writer.writerows(
                (name, buyer, name + str(group_id))
                for buyer in dups
            )
