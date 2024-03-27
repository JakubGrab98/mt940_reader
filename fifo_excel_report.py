"""Module responsibles for preparing report from FIFO data."""
import pandas as pd

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
            for source in entry["outflow_sources"]:
                row = {
                    "outflow_id": entry["outflow_id"],
                    "date": entry["date"],
                    "outflow_amount": entry["outflow_amount"],
                    "outflow_rate": entry["outflow_rate"],
                    "source_amount": source[0],
                    "source_rate": source[1],
                    "outflow_cost": source[2]
                }
                rows.append(row)
        df = pd.DataFrame(rows)
        self.df = df

    def export_to_excel(self, file_path: str) -> None:
        """
            Exports FIFO data to excel file.
        Args:
            file_path (str): A destination path for excel export 
        """
        if self.df is None:
            self.prepare_dataframe()
        self.df.to_excel(file_path, index=False)
        