"""Module provide a class which read and extract data from the MT940 bank statement file"""
import re
from utils import mt940_patterns
from nbp_rates import Rates

class Mt940Parser:
    """Read and retrieve data from the MT940 file"""
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.content = ""

    def read_file(self) -> str:
        """Context manager for reading mt940 file"""
        with open(self.file_path, "r") as file:
            self.content = file.read()
        return self.content

    def find_choosed_patern(self, regex, content, re_flag=re.MULTILINE) -> list:
        """Retrieve a string based on the regex pattern"""
        pattern = re.compile(regex, re_flag)
        matches = re.findall(pattern, content)
        return matches

    def get_opening_balance(self) -> float:
        """Retrieve opening balance of current account number"""
        mt940_opening_balance = self.find_choosed_patern(
            mt940_patterns.get("opening_balance"),
            self.content,
        )
        opening_balance = mt940_opening_balance[0][-1].replace(",", ".")
        return float(opening_balance)

    def get_closing_balance(self) -> float:
        """Retrieve closing balance of current account number"""
        mt940_closing_balance = self.find_choosed_patern(
            mt940_patterns.get("closed_balance"),
            self.content,
        )
        print(mt940_closing_balance)
        closing_balance = mt940_closing_balance[0][-1].replace(",", ".")
        return float(closing_balance)
    
    def get_account_number(self) -> str:
        """Retrieve owner's bank account from the bank statement"""
        mt940_account_number = self.find_choosed_patern(
            mt940_patterns.get("bank_account"),
            self.content,
        )
        account_number = mt940_account_number[0][-1]
        return str(account_number)
    
    def get_statement_number(self) -> str:
        """Retrieve number of the bank statement"""
        mt940_statement_number = self.find_choosed_patern(
            mt940_patterns.get("statement_number"),
            self.content,
        )
        statement_number = mt940_statement_number[0]
        return str(statement_number)
    
    def get_rate_details(self) -> str:
        """Retrieve statement/transactions date"""
        mt940_statement_date = self.find_choosed_patern(
            mt940_patterns.get("rate_details"),
            self.content,
        )
        currency_code = mt940_statement_date[0][2]
        statement_date_str = mt940_statement_date[0][1]
        year = f"20{statement_date_str[:2]}"
        month = statement_date_str[2:4]
        day = statement_date_str[4:]
        normalized_date_string = f"{year}-{month}-{day}"
        return normalized_date_string, currency_code

    def get_bank_rate(self, content) -> float | bool:
        """Getting bank rate in case of foregin exchange within the bank"""
        default_rate = "1,000000"
        mt940_bank_rate = self.find_choosed_patern(
            mt940_patterns.get("bank_rates"),
            content,
            re.DOTALL,
        )
        mt940_exchange_transaction = self.find_choosed_patern(
            mt940_patterns.get("exchange_transaction_rate"),
            content,
            re.DOTALL,
        )
        if mt940_bank_rate:
            if mt940_bank_rate[0][0] == default_rate:
                return float(mt940_bank_rate[0][1].replace(",", "."))
            if mt940_bank_rate[0][1] == default_rate:
                return float(mt940_bank_rate[0][0].replace(",", "."))
            return False
        if mt940_exchange_transaction:
            return float(mt940_exchange_transaction[0].replace(",", "."))
        return False

    def get_transaction_details(self) -> None:
        """Retrieve transaction amount and assign to inflow or outflow"""
        mt940_transaction_details = self.find_choosed_patern(
            mt940_patterns.get("transaction"),
            self.content,
            re.DOTALL,
        )
        transaction_date_string, currency_code = self.get_rate_details()
        rate_api = Rates(transaction_date_string, currency_code)
        transaction_nr = 0
        account_number = self.get_account_number()
        statement_number = self.get_statement_number()
        transaction_by_date = {}

        for transaction in mt940_transaction_details:
            transaction_side = transaction[1]
            amount_string = transaction[2]
            transaction_description = transaction[3]
            normalized_amount_string = amount_string.replace(",", ".")
            amount_float = float(normalized_amount_string)
            transaction_nr += 1
            is_bank_rate = self.get_bank_rate(transaction_description)
            if is_bank_rate:
                rate = is_bank_rate
            else:
                rate = rate_api.get_rate()

            if transaction_date_string not in transaction_by_date:
                transaction_by_date[transaction_date_string] = {}

            transaction_by_date[transaction_date_string][transaction_nr] = {
                        "transaction_number": transaction_nr,
                        "statement_number": statement_number,
                        "account_number": account_number,
                        "transaction_date": transaction_date_string,
                        "transaction_side": transaction_side,
                        "transaction_amount": amount_float,
                        "currency_code": currency_code,
                        "PLN_rate": rate,
                    }
        return transaction_by_date
