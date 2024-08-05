<<<<<<< HEAD
class BankAccount:
    """Create bank accounts"""
    def __init__(self, name: str, account_number: str, currency: str) -> None:
        self.name = name
        self.account_number = account_number
        self.currency = currency


# tutaj może użyjemy dataclass??
=======
from dataclasses import dataclass

@dataclass
class BankAccount:
    """Class for keeping details of a bank account"""
    name: str
    account_number: str
    currency: str
>>>>>>> develop
