import json
from pathlib import Path
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


if __name__ == "__main__":
    setup_logging()
    OUTPUT_FILE_NAME = "FILE.json"
    EXPORT_PATH = r"TEST.xlsx"
    SOURCE_DIRECTORY = r"C:\"
    mt940_files = [
        file for file in Path(SOURCE_DIRECTORY).iterdir()
        if str(file)[-6:] == ".mt940"
        or str(file)[-4:] == ".old"
    ]

    new_transactions = []
    for file in mt940_files:
        try:
            full_path = Path(SOURCE_DIRECTORY) / file
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
        with open(OUTPUT_FILE_NAME, "r") as jsonfile:
            transactions = json.load(jsonfile)
    except (FileNotFoundError, json.JSONDecodeError):
        logger.error("Transaction's file not found, initialize empty list")
        transactions = []

    transactions.extend(new_transactions)

    with open(OUTPUT_FILE_NAME, "w") as jsonfile:
        json.dump(transactions, jsonfile, indent=4)

    try:
        with open(OUTPUT_FILE_NAME, "r") as jsonfile:
            transactions_list = json.load(jsonfile)
    except FileNotFoundError:
        logger.error("Transaction's file not found")

    fifo_calculator = FifoCalculator(transactions_list)
    fifo_calculator.fifo_calculation()
    fifo_report = FifoExcelReport(fifo_calculator.fifo_logs)
    fifo_report.export_to_excel(EXPORT_PATH)
