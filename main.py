import json
from pathlib import Path
import datetime
import logging
import logging.config
from mt940_parser import Mt940Parser
from fifo_calculator import FifoCalculator
from fifo_excel_report import FifoExcelReport

logger = logging.getLogger(__name__)

def setup_logging() -> None:
    """Function setups logging confguration using config.json file.
    """
    config_file = Path("logging_configs/config.json")
    try:
        with open(config_file) as file:
            config = json.load(file)
        logging.config.dictConfig(config)
    except FileNotFoundError:
        logging.error("Logging configuration file not found.")
    except json.JSONDecodeError:
        logger.error("Invalid JSON in the logging configuration file.")

# file_path = r"N:\RED Business Support\MT940\PEKAO_CIP_EUR\Proffice MT940_CIP_EUR_WB_20240328071025_20240328092919.old"
# creation_time = os.path.getctime(file_path)
# formatted_time = datetime.datetime.fromtimestamp(creation_time).date()
# print(formatted_time)
# today = datetime.datetime.now().date()
# print(today)

if __name__ == "__main__":
    setup_logging()
    FILE_NAME = "CdbP-EUR-test.json"
    EXPORT_PATH = r"C:\FIFO_APP\fifo-report-cdbpp-test.xlsx"
    DIR_PATH = r"N:\RED Business Support\MT940\PEKAO_CDBP_EUR"
    mt940_files = [
        file for file in Path(DIR_PATH).iterdir()
        if str(file)[-6:] == ".mt940"
        or str(file)[-4:] == ".old"
    ]

    new_transactions = []
    for file in mt940_files:
        try:
            full_path = Path(DIR_PATH) / file
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
            logger.error("Error processing file: %s %s", file, e)

    try:
        with open(FILE_NAME, "r") as jsonfile:
            transactions = json.load(jsonfile)
    except (FileNotFoundError, json.JSONDecodeError):
        logger.error("Transaction's file not found, initialize empty list")
        transactions = []

    transactions.extend(new_transactions)

    with open(FILE_NAME, "w") as jsonfile:
        json.dump(transactions, jsonfile, indent=4)

    try:
        with open(FILE_NAME, "r") as jsonfile:
            transactions_list = json.load(jsonfile)
    except FileNotFoundError:
        logger.error("Transaction's file not found")

    fifo_calculator = FifoCalculator(transactions_list)
    fifo_calculator.fifo_calculation()
    fifo_report = FifoExcelReport(fifo_calculator.fifo_logs)
    fifo_report.export_to_excel(EXPORT_PATH)
