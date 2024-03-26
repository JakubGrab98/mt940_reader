mt940_patterns = {
    "bank_account": r"^:25:/(PL)(\d{26})",
    "statement_number": r":28C:(\d{5})",
    "opening_balance": r"^:60F:(C|D)\d{6}(EUR|USD|GBP)(\d+,\d{2})",
    "transaction_details": r"^:61:(\d{10})(CR|DR|CD|DD)(\d+,\d{2})\n",
    "closed_balance": r"^:62F:(C|D)\d{6}(EUR|USD|GBP)(\d+,\d{2})",
    "transaction_amount": r"(R)(\d+,\d{2})(N)",
    "rate_details": r"^:62F:(C|D)(\d{6})(EUR|USD|GBP)",
    "description": r":86:(.*?)(?=(:61:|:62F:))",
    "bank_rates": r"(\d+,\d{6}) :S: (\d+,\d{6})",
    "bank_sell_rate": r"S: (\d+,\d{6})",
    "exchange_transaction_rate": r"WYM: (\d+,\d{6})",
    "transaction": r":61:(\d{10})(CR|DR|CD|DD)(\d+,\d{2})(.+?)\^32",
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

FRAME_COLUMNS = [
    "account_number",
    "transaction_date",
    "transaction_side",
    "transaction_amount",
    "currency_code",
    "PLN_rate",
]

def calculate_fifo(inflows, outflows):
    fifo_values = []
    transaction_list = []
    inflows = []
    total_inflow = 0
    total_outflow = 0
    for transaction in transactions:
        fifo_value = 0
        amount = transaction["transaction_amount"]
        rate = transaction["PLN_rate"]
        transaction_list.append([amount, rate])

        if amount > 0:
            total_inflow += amount
            inflows.append([amount, rate])

        elif amount < 0:
            total_outflow += -amount
            sell_amount = -amount
            sell_value = sell_amount * rate

            while sell_amount > 0 and inflows:
                first_inflow = inflows[0]
                first_amount, first_rate = first_inflow
                del inflows[0]

                if first_amount <= sell_amount:
                    first_value = first_amount * first_rate
                    fifo_value -= first_value
                    sell_amount -= first_amount
                    if sell_amount == 0:
                        fifo_value += sell_value

                else:
                    remaining_value = sell_amount * first_rate
                    fifo_value -= remaining_value
                    fifo_value += sell_value
                    inflows.insert(0, [first_amount - sell_amount, first_rate])
                    sell_amount = 0

        fifo_values.append(round(fifo_value, 2))
    return fifo_values
