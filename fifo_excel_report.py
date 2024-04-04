"""Module responsibles for preparing report from FIFO data."""
import pandas as pd
import numpy as np

class FifoExcelReport():
    """
    Class for preparing and exporting FIFO data to an Excel report.
    """
    def __init__(self, fifo_data: list) -> None:
        """
        Initializes the FifoExcelReport instance with FIFO data.
        Args:
            fifo_data (list): A list of dictionaries containing FIFO transaction data
        """
        self.fifo_data = fifo_data
        self.df = None

    def prepare_dataframe(self):
        """
        Prepares a pandas DataFrame from the FIFO data.
        """
        rows = []
        for entry in self.fifo_data:
            if entry["transaction_type"] == "C":
                row = {
                    "transaction_id": entry["transaction_id"],
                    "transaction_type": entry["transaction_type"],
                    "date": entry["date"],
                    "amount": entry["inflow_amount"],
                    "current_rate": entry["current_rate"],
                    "outflow_cost": 0,
                }
                rows.append(row)
            else:
                for source in entry["outflow_sources"]:
                    row = {
                        "transaction_id": entry["transaction_id"],
                        "transaction_type": entry["transaction_type"],
                        "date": entry["date"],
                        "current_rate": entry["current_rate"],
                        "inflow_id": source[3],
                        "amount": source[0],
                        "inflow_rate": source[1],
                        "outflow_cost": source[2],
                    }
                    rows.append(row)
        df = pd.DataFrame(rows)
        sorted_df = df.sort_values(by=["transaction_id", "transaction_type"])
        self.df = sorted_df

    def export_to_excel(self, file_path: str) -> None:
        """
            Exports FIFO data to excel file.
        Args:
            file_path (str): A destination path for excel export 
        """
        if self.df is None:
            self.prepare_dataframe()
        self.df.to_excel(file_path, index=False)
        