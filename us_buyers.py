import csv
from fuzzywuzzy import fuzz, process
import pandas as pd

data = pd.read_csv('destxbuyer.csv', encoding='latin-1')

# re-code empty cells
data.buyer = data.buyer.fillna('no_buyer')
data.dest = data.dest.fillna('no_dest')

# narrow the data to just US dest
us_data = data[data.dest == 'US']

# set a threshold level for similarity
threshold = 80

# start an empty list to hold the possible duplicates
all_dupes = []
# create a set of all buyers from us

# open the file to write to
with open('us_filtered_small.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['buyer', 'group_id'])

    buyers = set(us_data.buyer.tolist())
    # iterate over the buyers and check against all other buyers
    while buyers:
        current_buyer = buyers.pop()
        # gather all the strings that are similar
        dupes = process.extract(
                current_buyer, buyers,
                scorer=fuzz.token_set_ratio
                )
        # filter the dupes based on threshold of similarity
        filtered = set(x[0] for x in dupes if x[1] > threshold)
        # since process.extract doesn't return the search term, add it in
        if len(filtered) > 0:
            filtered.add(current_buyer)
        # add the group of dupes to the collection of all dupes
        all_dupes.append(filtered)
        # remove the group of buyers from the overall list to speed things up
        for buyer in filtered:
            buyers.discard(buyer)
    # iterate over the groups of dupes with the large collection of all dupes
    for (group_id, dupes) in enumerate(all_dupes):
        # write a new row for each buyer within the dupe
        writer.writerows(
            (buyer, 'US' + str(group_id))
            for buyer in dupes
        )
