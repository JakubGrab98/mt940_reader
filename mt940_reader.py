"""Module provide a class which read and extract data from the MT940 bank statement file"""
import re
from utils import mt940_patterns
from nbp_rates import Rates

class MtReader:
    """Read and retrieve data from the MT940 file"""
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.transactions = []
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
            mt940_patterns.get("opening_balance")
        )
        opening_balance = mt940_opening_balance[0][-1].replace(",", ".")
        return float(opening_balance)

    def get_closing_balance(self) -> float:
        """Retrieve closing balance of current account number"""
        mt940_closing_balance = self.find_choosed_patern(
            mt940_patterns.get("closed_balance")
        )
        print(mt940_closing_balance)
        closing_balance = mt940_closing_balance[0][-1].replace(",", ".")
        return float(closing_balance)
    
    def get_account_number(self) -> str:
        """Retrieve owner's bank account from the bank statement"""
        mt940_account_number = self.find_choosed_patern(
            mt940_patterns.get("bank_account")
        )
        account_number = mt940_account_number[0][-1]
        return str(account_number)
    
    def get_statement_number(self) -> str:
        """Retrieve number of the bank statement"""
        mt940_statement_number = self.find_choosed_patern(
            mt940_patterns.get("statement_number")
        )
        statement_number = mt940_statement_number[0]
        return str(statement_number)
    
    def get_rate_details(self) -> str:
        """Retrieve statement/transactions date"""
        mt940_statement_date = self.find_choosed_patern(
            mt940_patterns.get("rate_details")
        )
        currency_code = mt940_statement_date[0][2]
        statement_date_str = mt940_statement_date[0][1]
        year = f"20{statement_date_str[:2]}"
        month = statement_date_str[2:4]
        day = statement_date_str[4:]
        normalized_date_string = f"{year}-{month}-{day}"
        return normalized_date_string, currency_code
          
    def get_transaction_details(self) -> None:
        """Retrieve transaction amount and assign to inflow or outflow"""
        mt940_transaction_details = self.find_choosed_patern(
            mt940_patterns.get("transaction_details")
        )
        transaction_date_string, currency_code = self.get_rate_details()
        rate_api = Rates(transaction_date_string, currency_code)
        rate = rate_api.get_rate()

        for transaction in mt940_transaction_details:
            amount_string = transaction[2]
            normalized_amount_string = amount_string.replace(",", ".")
            amount_float = float(normalized_amount_string)
            transaction_side = transaction[1]

            self.transactions.append({
                    "source_file": self.file_path,
                    "statement_number": self.get_statement_number(),
                    "account_number": self.get_account_number(),
                    "transaction_date": transaction_date_string,
                    "transaction_side": transaction_side,
                    "transaction_amount": amount_float,
                    "currency_code": currency_code,
                    "PLN_rate": rate,
                }
            )
