mt940_patterns = {
    "bank_account": r"^:25:/(PL)(\d{26})",
    "statement_number": r":28C:(\d{5})",
    "opening_balance": r"^:60F:(C|D)\d{6}(EUR|USD|GBP)(\d+,\d{2})",
    "closed_balance": r"^:62F:(C|D)\d{6}(EUR|USD|GBP)(\d+,\d{2})",
    "transaction_amount": r"(R)(\d+,\d{2})(N)",
    "rate_details": r"^:62F:(C|D)(\d{6})(EUR|USD|GBP)",
    "description": r":86:(.*?)(?=(:61:|:62F:))",
    "bank_rates": r"(\d{1}+,\d{6}) :S: (\d+,\d{6})",
    "bank_sell_rate": r"S: (\d+,\d{6})",
    "exchange_transaction_rate": r"WYM: (\d+,\d{6})",
    "transaction": r"1:(\d{10})(CR|DR|CD|DD)(\d+,\d{2})(.+?)\:6",
}
