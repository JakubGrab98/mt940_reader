mt940_patterns = {
    "bank_account": r"^:25:/(PL)(\d{26})",
    "statement_number": r":28C:(\d{5})",
    "opening_balance": r"^:60F:(C|D)\d{6}(EUR|USD|GBP)(\d+,\d{2})",
    "transaction_details": r"^:61:(\d{10})(CR|DR)(\d+,\d{2})",
    "closed_balance": r"^:62F:(C|D)\d{6}(EUR|USD|GBP)(\d+,\d{2})",
    "transaction_amount": r"(R)(\d+,\d{2})(N)",
    "rate_details": r"^:62F:(C|D)(\d{6})(EUR|USD|GBP)",
    "description": r":86:(.*?)(?=(:61:|:62F:))",
}

def remove_duplicates(transactions):
    unique_transactions = []
    seen = set()

    for transaction in transactions:
        # Create a tuple of the fields that determine uniqueness
        identifier = (
            transaction["statement_number"],
            transaction["transaction_date"],
            transaction['description'],
        )
        
        if identifier not in seen:
            seen.add(identifier)
            unique_transactions.append(transaction)

    return unique_transactions