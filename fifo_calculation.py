import json
import operator
import pandas as pd

def remove_duplicates(transactions):
    seen = set()
    result = []
    for sublist in transactions:
        unique_sublist = []
        for item in sublist:
            print(item)
            serialized_item = json.dumps(item, sort_keys=True)
            if serialized_item not in seen:
                seen.add(serialized_item)
                unique_sublist.append(item)
        result.append(unique_sublist)
    return result


FILE_NAME = "transactions.json"


with open(FILE_NAME, "r") as jsonfile:
    transactions_list = json.load(jsonfile)


# unique_transactions = remove_duplicates(transactions_list)


# with open(FILE_NAME, "w") as jsonfile:
#     data = unique_transactions
#     json.dump(data, jsonfile, indent=4)

def get_inflows_and_outflows(data: list):
    inflows = []
    outflows = []
    for sublist in data:
        for statements_dict in sublist:
            for transaction_dict in statements_dict.values():
                for transaction in transaction_dict.values():
                    if transaction["transaction_side"] == "CR":
                        inflows.append(transaction)
                    elif transaction["transaction_side"] == "DR":
                        outflows.append(transaction)
    return inflows, outflows

inflows, outflows = get_inflows_and_outflows(transactions_list)
print(sorted(inflows, key=operator.itemgetter("transaction_date")))

def fifo_calculator(inflows, outflows):
    pass
