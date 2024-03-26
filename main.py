import json
import os
import logging
from mt940_reader import MtReader

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s %(name)s - %(levelname)s - %(message)s",
    # FileHandler do wyrzucenia logów do osobnego pliku
    handlers=[
        logging.FileHandler("my_logs.log"),
        logging.StreamHandler(),
    ]
)

DIR_PATH = r"N:\RED Business Support\MT940\PEKAO_CIP_EUR"
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
    except Exception as e:
        logging.error("Error processing file: %s", file)

filename = "transactions.json"

try:
    with open(filename, "r") as jsonfile:
        transactions = json.load(jsonfile)
except (FileNotFoundError, json.JSONDecodeError):
    transactions = []

transactions.extend(new_transactions)

with open(filename, "w") as jsonfile:
    json.dump(transactions, jsonfile, indent=4)
