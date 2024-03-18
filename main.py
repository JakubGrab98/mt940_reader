import json
import os
from mt940_reader import MtReader

DIR_PATH = r"TEST"
mt940_files = [file for file in os.listdir(DIR_PATH) if file[-4:] == ".old"]

new_transactions = []
for file in mt940_files:
    try:
        full_path = os.path.join(DIR_PATH, file)
        mt940_reader = MtReader(full_path)
        mt940_reader.read_file()
        mt940_reader.get_transaction_details()
        new_transactions.append(
            mt940_reader.transactions
        )
    except:
        pass

filename = "transactions.json"

try:
    with open(filename, "r") as jsonfile:
        transactions = json.load(jsonfile)
except (FileNotFoundError, json.JSONDecodeError):
    transactions = []

transactions.extend(new_transactions)
    
for index, transaction in enumerate(transactions):
    transaction["id"] = index + 1

with open(filename, "w") as jsonfile:
    json.dump(transactions, jsonfile, indent=4)
