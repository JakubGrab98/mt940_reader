import re
from utils import mt940_patterns

mt940_content = """

:20:1
:25:/PL50124062921978001062009446
:28C:00075
:60F:C230527EUR000002376582,31
:61:2305290529DR000000500000,00N767NONREF
:86:767^00PRZEKAZ EURO-KRAJOWY       ^34000
^3012401037^38PL12124010371111001045285562
^20Transakcja w obrocie dewizo^21wym, 235T000172FX/4885 :K: 
^224,500000 :S: 1,000000 :O: 2^23 250 000,00 PLN
:61:2305290529CR000000016000,00N491NONREF
:86:491^00PRZELEW SEPA ODEBRANY      ^34000
^3027CITI99^38IE27CITI99005133974035
^20/INV S/105/EUR/2023 05/08/2^21023
^26SEPA 33B 16000EUR
^32APTIV Svsc Poland S.A.     ^33        2,ULICA PODGORKI TY
^62NIECKIE KRAKOW,30-399 LESSE^63R POLAND,PL
:62F:C230529EUR000001892582,31
:64:C230529EUR000001892582,31
-
"""



# pattern = re.compile(mt940_patterns.get("transaction_details"), re.DOTALL)
# matches = re.findall(pattern, mt940_content)

# print(matches)
pattern = re.compile(mt940_patterns.get("bank_rates"), re.DOTALL)

# Find all matches of the pattern in the text
matches = re.findall(pattern, mt940_content)
print(matches)

# for match in matches:
#     content = match[3]
#     pattern = re.compile(mt940_patterns.get("exchange_transaction"), re.MULTILINE)
#     rates = re.findall(pattern, content)
#     print(rates)

# Processing matches
# for match in matches:
#     # Trim leading and trailing whitespace for each match
#     cleaned_match = match.strip()
#     print(cleaned_match)