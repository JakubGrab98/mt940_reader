from dataclasses import dataclass

@dataclass
class BankAccount:
    """Class for keeping details of a bank account"""
    name: str
    account_number: str
    currency: str
