patterns = {
    "bank_account": r"^:25:/(PL)(\d{26})",
    "opening_balance": r"^:60F:(C|D)\d{6}(EUR|USD|GBP)(\d+,\d{2})",
    "transaction_details": r"^:61:(\d{10})(CR|DR)(\d+,\d{2})",
    "closed_balance": r"^:62F:(C|D)\d{6}(EUR|USD|GBP)(\d+,\d{2})",
    "transaction_amount": r"(R)(\d+,\d{2})(N)",
}

