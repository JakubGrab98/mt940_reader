import json
import datetime
import os
import logging
from mt940_parser import Mt940Parser

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s %(name)s - %(levelname)s - %(message)s",
    # FileHandler do wyrzucenia logów do osobnego pliku
    handlers=[
        logging.FileHandler("my_logs.log"),
        logging.StreamHandler(),
    ]
)

# file_path = r"N:\RED Business Support\MT940\PEKAO_CIP_EUR\Proffice MT940_CIP_EUR_WB_20240328071025_20240328092919.old"
# creation_time = os.path.getctime(file_path)
# formatted_time = datetime.datetime.fromtimestamp(creation_time).date()
# print(formatted_time)
# today = datetime.datetime.now().date()
# print(today)


DIR_PATH = r"N:\RED Business Support\MT940\PEKAO_CDBP_EUR"
mt940_files = [
    file for file in os.listdir(DIR_PATH) 
    if file[-6:] == ".mt940"
    or file[-4:] == ".old"
]

new_transactions = []
for file in mt940_files:
    try:
        full_path = os.path.join(DIR_PATH, file)
        mt940_reader = Mt940Parser(full_path)
        mt940_reader.read_file()
        transaction_data = mt940_reader.get_transaction_details()
        for transaction_date, transactions in transaction_data.items():
            for transaction_id, transaction_details in transactions.items():
                transaction_date_id = transaction_date.replace("-", "")
                unique_transaction_id = f"{transaction_date_id}{transaction_id}"

                if not any(
                    transaction["id"] == unique_transaction_id for transaction in new_transactions
                ):
                    transaction_details["id"] = unique_transaction_id
                    new_transactions.append(transaction_details)
    except Exception as e:
        logging.error("Error processing file: %s %s", file, e)

filename = "DEFINE-EUR.json"

try:
    with open(filename, "r") as jsonfile:
        transactions = json.load(jsonfile)
except (FileNotFoundError, json.JSONDecodeError):
    transactions = []

transactions.extend(new_transactions)

with open(filename, "w") as jsonfile:
    json.dump(transactions, jsonfile, indent=4)
