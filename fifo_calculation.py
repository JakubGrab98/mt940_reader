import json


seen = set()
unique_dicts = []

def remove_duplicates(transactions):
    for d in transactions:
        serialized = json.dumps(d, sort_keys=True)
        if serialized not in seen:
            seen.add(serialized)
            unique_dicts.append(d)


filename = "transactions.json"


with open(filename, "r") as jsonfile:
    transactions_list = json.load(jsonfile)
    unique_transactions = remove_duplicates(transactions_list)

with open(filename, "w") as jsonfile:
    data = unique_transactions
    json.dump(data, jsonfile, indent=4)



inflows = []
outflows = []

for transactions in transactions_list:
    print(transactions)
    for transaction in transactions:
        if transaction["transaction_side"] == "CR" and transaction["transaction_date"][0:4] == "2015": #or transaction["transaction_date"][0:4] == "2016"):
            inflows.append(transaction["transaction_amount"])
        elif transaction["transaction_side"] == "DR" and transaction["transaction_date"][0:4] == "2015": # or transaction["transaction_date"][0:4] == "2016"):
            outflows.append(transaction["transaction_amount"])
            
print(f"inflows: {inflows}")
print(f"outflows: {outflows}")
print(sum(inflows) - sum(outflows))