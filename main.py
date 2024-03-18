from mt940_reader import MtReader
from nbp_rates import Rates

mt940_reader = MtReader(r"N:\RED Business Support\MT940\PEKAO_CIP_EUR\Proffice MT940_CIP_EUR_WB_20240229071021_20240229100307.old")


mt940_reader.read_file()
mt940_reader.get_transaction_details()

print(f"inflows: {mt940_reader.inflows}")

print(f"outflows: {mt940_reader.outflows}")
