from mt940_reader import MtReader

mt940_reader = MtReader()


mt940_reader.read_file()
print(mt940_reader.content)
mt940_reader.get_transaction_amount()

print(f"inflows: {mt940_reader.inflows}")

print(f"outflows: {mt940_reader.outflows}")