"""Module reponsibles for calculating FIFO cost"""
from collections import deque

class FifoCalculator:
    """Class for calculating foreign exchange fifo cost"""
    def __init__(self, transactions: list) -> None:
        """
        Initializes the FifoCalculator instance with bank transactions.

        Args:
            transactions (dict): A list of dictionaries containing bank transaction data
        """
        self.transactions = transactions
        self.fifo_queue = deque()
        self.fifo_logs = []


    def fifo_calculation(self):
        """Calculates fifo cost of outflow transactions"""
        self.transactions.sort(key=lambda x: (x["transaction_side"], x["id"]))
        for transaction in self.transactions:
            if transaction["transaction_side"][0] == "C":
                self.fifo_queue.append(
                    (   transaction["id"],
                        transaction["transaction_amount"],
                        transaction["PLN_rate"],
                    )
                )
                self.fifo_logs.append(
                    {   "transaction_id": transaction["id"],
                        "transaction_type": transaction["transaction_side"][0],
                        "date": transaction["transaction_date"],
                        "inflow_amount": transaction["transaction_amount"],
                        "current_rate": transaction["PLN_rate"],
                    }
                )
            elif transaction["transaction_side"][0] == "D":
                outflow_amount = outflow_amount = transaction["transaction_amount"]
                outflow_rate = transaction["PLN_rate"]
                outflow_sources = []

                while outflow_amount > 0 and self.fifo_queue:
                    inflow_id, inflow_amount, inflow_rate = self.fifo_queue.popleft()
                    if inflow_amount <= outflow_amount:
                        outflow_amount -= inflow_amount
                        outflow_cost = inflow_amount * (outflow_rate - inflow_rate)
                        outflow_sources.append(
                            (
                                inflow_amount,
                                inflow_rate,
                                outflow_cost,
                                inflow_id,
                            )
                        )
                    else:
                        remaining_infow_amount = inflow_amount - outflow_amount
                        self.fifo_queue.appendleft(
                            (
                                inflow_id,
                                remaining_infow_amount,
                                inflow_rate,
                            )
                        )
                        outflow_cost = outflow_amount * (outflow_rate - inflow_rate)
                        outflow_sources.append(
                            (
                                outflow_amount,
                                inflow_rate,
                                outflow_cost,
                                inflow_id,
                                )
                        )
                        outflow_amount = 0

                self.fifo_logs.append(
                    {   "transaction_id": transaction["id"],
                        "transaction_type": transaction["transaction_side"][0],
                        "date": transaction["transaction_date"],
                        "current_rate": transaction["PLN_rate"],
                        "outflow_sources": outflow_sources,
                    }
                )
