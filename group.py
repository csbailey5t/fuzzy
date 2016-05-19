from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import pandas as pd
import csv

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

with open('filtered.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['dest', 'buyer', 'group_id'])
    count = 0
    for (name, group) in grouped:
        # here to 36 - abstract into function
        deduped = []
        buyers = set(group.buyer.tolist())
        while buyers:
            current_buyer = buyers.pop()
            dupes = process.extract(
                    current_buyer, buyers,
                    scorer=fuzz.token_set_ratio
                    )
            filtered = set(x for x in dupes if x[1] > threshold)
            filtered.add(current_buyer)
            deduped.append(filtered)
            buyers -= filtered
        print("while loop has ended")
        print("buyers", buyers)
        # for duduped in alldedupeds:
        for (group_id, dups) in enumerate(deduped):
            writer.writerows(
                (name, buyer, name + str(group_id))
                for buyer in dups
            )
        count += 1
        print("count", count)
        print("write row for loop has ended")

    print('for loop for name group has ended')
