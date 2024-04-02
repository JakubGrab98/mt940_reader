import json
import pandas as pd
from collections import deque
from fifo_calculator import FifoCalculator
from fifo_excel_report import FifoExcelReport


FILE_NAME = "transactions.json"
EXPORT_PATH = r"C:\FIFO_APP\fifo-report-USD.xlsx"

with open(FILE_NAME, "r") as jsonfile:
    transactions_list = json.load(jsonfile)

fifo_calculator = FifoCalculator(transactions_list)
fifo_calculator.fifo_calculation()
fifo_report = FifoExcelReport(fifo_calculator.fifo_logs)
fifo_report.export_to_excel(EXPORT_PATH)


# inflows = []
# outflows = []

# for transaction in transactions_list:
#     if transaction["transaction_side"][0] == "C":# and transaction["transaction_date"][0:7] == "2016-12": #or transaction["transaction_date"][0:4] == "2016"):
#         inflows.append(transaction["transaction_amount"])
#     elif transaction["transaction_side"][0] == "D":# and transaction["transaction_date"][0:7] == "2016-12": # or transaction["transaction_date"][0:4] == "2016"):
#         outflows.append(transaction["transaction_amount"])

# print(sum(inflows) - sum(outflows))
# transactions_list.sort(key=lambda x: x["id"])

# fifo_queue = deque()
# fifo_log = []


# for transaction in transactions_list:
#     if transaction["transaction_side"] == "CR":
#         fifo_queue.append(
#             (
#                 transaction["transaction_amount"],
#                 transaction["PLN_rate"],
#             )
#         )
#     elif transaction["transaction_side"] == "DR":
#         outflow_amount = outflow_amount = transaction["transaction_amount"]
#         outflow_rate = transaction["PLN_rate"]
#         outflow_sources = []
#         outflow_cost = 0

#         while outflow_amount > 0 and fifo_queue:
#             inflow_amount, inflow_rate = fifo_queue.popleft()
#             if inflow_amount <= outflow_amount:
#                 outflow_amount -= inflow_amount
#                 outflow_sources.append((inflow_amount, inflow_rate))
#                 outflow_cost += inflow_amount * (outflow_rate - inflow_rate)
#             else:
#                 remaining_infow_amount = inflow_amount - outflow_amount
#                 fifo_queue.appendleft((remaining_infow_amount, inflow_rate))
#                 outflow_cost += outflow_amount * (outflow_rate - inflow_rate)
#                 outflow_sources.append((outflow_amount, inflow_rate))
#                 outflow_amount = 0

#         fifo_log.append(
#             {"outflow_id": transaction["id"],
#             "date": transaction["transaction_date"],
#             "outflow_amount": transaction["transaction_amount"],
#             "outflow_rate": transaction["PLN_rate"],
#             "outflow_sources": outflow_sources,
#             "outflow_cost": outflow_cost}
#         )

# # Save FIFO log to a file
# with open('fifo_report.json', 'w') as f:
#     json.dump(fifo_log, f, indent=4)

# print("FIFO report saved as fifo_report.json.")
