import json
import pandas as pd
from collections import deque
from fifo_calculator import FifoCalculator
from fifo_excel_report import FifoExcelReport


FILE_NAME = "DEFINE-EUR.json"
EXPORT_PATH = r"C:\FIFO_APP\fifo-report-define.xlsx"

with open(FILE_NAME, "r") as jsonfile:
    transactions_list = json.load(jsonfile)

fifo_calculator = FifoCalculator(transactions_list)
fifo_calculator.fifo_calculation()
fifo_report = FifoExcelReport(fifo_calculator.fifo_logs)
fifo_report.export_to_excel(EXPORT_PATH)


inflows = []
outflows = []

for transaction in transactions_list:
    if transaction["transaction_side"][0] == "C":# and transaction["transaction_date"][0:7] == "2016-12": #or transaction["transaction_date"][0:4] == "2016"):
        inflows.append(transaction["transaction_amount"])
    elif transaction["transaction_side"][0] == "D":# and transaction["transaction_date"][0:7] == "2016-12": # or transaction["transaction_date"][0:4] == "2016"):
        outflows.append(transaction["transaction_amount"])

print(sum(inflows) - sum(outflows))
