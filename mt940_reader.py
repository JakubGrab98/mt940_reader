"""Module provide a class which read and extract data from the MT940 bank statement file"""
import re
from regex_dict import patterns

class MtReader:
    """Read and retrieve data from the MT940 file"""
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.inflows = []
        self.outflows = []
        self.content = ""

    def read_file(self) -> str:
        """Context manager for reading mt940 file"""
        with open(self.file_path, "r") as file:
            self.content = file.read()
        return self.content

    def find_choosed_patern(self, regex) -> list:
        """Retrieve a string based on the regex pattern"""
        pattern = re.compile(regex, re.MULTILINE)
        matches = re.findall(pattern, self.read_file())
        return matches

    def get_opening_balance(self) -> float:
        """Retrieve opening balance of current account number"""
        mt940_opening_balance = self.find_choosed_patern(
            patterns.get("opening_balance")
        )
        opening_balance = mt940_opening_balance[0][-1]
        return float(opening_balance)

    def get_closing_balance(self) -> float:
        """Retrieve closing balance of current account number"""
        mt940_closing_balance = self.find_choosed_patern(
            patterns.get("closed_balance")
        )
        closing_balance = mt940_closing_balance[0][-1]
        return float(closing_balance)
    
    def get_transaction_amount(self) -> None:
        """Retrieve transaction amount and assign to inflow or outflow"""
        mt940_transaction_details = self.find_choosed_patern(
            patterns.get("transaction_details")
        )

        for transaction in mt940_transaction_details:
            amount_string = transaction[2]
            normalized_amount_string = amount_string.replace(",", ".")
            amount_float = float(normalized_amount_string)
            if transaction[1]=="CR":
                self.inflows.append(amount_float)
            elif transaction[1]=="DR":
                self.outflows.append(amount_float)
