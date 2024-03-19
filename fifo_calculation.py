import json


def remove_duplicates(transactions):
    unique_transactions = []
    seen = set()

    for transaction in transactions:
        # Create a tuple of the fields that determine uniqueness
        identifier = (transaction['date'], transaction['amount'], transaction['description'])
        
        if identifier not in seen:
            seen.add(identifier)
            unique_transactions.append(transaction)

    return unique_transactions

filename = "transactions.json"

try:
    with open(filename, "r") as jsonfile:
        transactions_list = json.load(jsonfile)
except (FileNotFoundError, json.JSONDecodeError):
    transactions_list = []


inflows = []
outflows = []

for transactions in transactions_list:
    print(transactions)
    for transaction in transactions:
        if transaction["transaction_side"] == "CR" and transaction["transaction_date"][0:7] == "2016-02": #or transaction["transaction_date"][0:4] == "2016"):
            inflows.append(transaction["transaction_amount"])
        elif transaction["transaction_side"] == "DR" and transaction["transaction_date"][0:7] == "2016-02": # or transaction["transaction_date"][0:4] == "2016"):
            outflows.append(transaction["transaction_amount"])
            
print(f"inflows: {inflows}")
print(f"outflows: {outflows}")
print(sum(inflows) - sum(outflows))