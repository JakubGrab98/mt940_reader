import json
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

# DIR_PATH = r"N:\RED Business Support\MT940\PEKAO_CIP_EUR"
# mt940_files = [file for file in os.listdir(DIR_PATH) if file[-4:] == ".old"]
# # test_files = [
# #     r"N:\RED Business Support\MT940\PEKAO_CIP_EUR\Proffice MT940_CIP_EUR_WB_20240326071051_20240326091953.old",
# #     r"N:\RED Business Support\MT940\PEKAO_CIP_EUR\Proffice MT940_CIP_EUR_WB_20240325071034_20240325095146.old",
# #     r"N:\RED Business Support\MT940\PEKAO_CIP_EUR\Proffice MT940_CIP_EUR_WB_20231002071018.old",
# #     r"N:\RED Business Support\MT940\PEKAO_CIP_EUR\export20230930191314_20230930192456.old",
# #     r"N:\RED Business Support\MT940\PEKAO_CIP_EUR\Proffice MT940_CIP_EUR_WB_20231222071057_20231222095819.old",
# #     r"N:\RED Business Support\MT940\PEKAO_CIP_EUR\Proffice MT940_CIP_EUR_WB_20240321071030_20240321100335.old",
# # ]

# new_transactions = []
# for file in mt940_files:
#     try:
#         full_path = os.path.join(DIR_PATH, file)
#         mt940_reader = Mt940Parser(full_path)
#         mt940_reader.read_file()
#         transaction_data = mt940_reader.get_transaction_details()
#         for transaction_date, transactions in transaction_data.items():
#             for transaction_id, transaction_details in transactions.items():
#                 transaction_date_id = transaction_date.replace("-", "")
#                 unique_transaction_id = f"{transaction_date_id}{transaction_id}"

#                 if not any(
#                     transaction["id"] == unique_transaction_id for transaction in new_transactions
#                 ):
#                     transaction_details["id"] = unique_transaction_id
#                     new_transactions.append(transaction_details)
#     except Exception as e:
#         logging.error("Error processing file: %s", file)

filename = "transactions.json"

try:
    with open(filename, "r") as jsonfile:
        transactions = json.load(jsonfile)
except (FileNotFoundError, json.JSONDecodeError):
    transactions = []

transactions.extend(new_transactions)

with open(filename, "w") as jsonfile:
    json.dump(transactions, jsonfile, indent=4)


