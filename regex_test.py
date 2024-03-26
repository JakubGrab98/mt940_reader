import re
from utils import mt940_patterns

mt940_content = """

:20:1
:25:/PL26124062921787001062009534
:28C:00016
:60F:C230708USD000000181716,24
:61:2307110711CD000000300000,00N172NONREF
:86:172^00PRZELEW                    ^34000
^3012401037^38PL12124010371111001045285562
^20Transakcja w obrocie dewizo^21wym, 237B003405FX/83568 :K:
^22 1,000000 :S: 4,070000 :O: ^231 221 000,00 PLN
^32COLLIERS POLAND SPOŁKA Z O.^33O.      PL PIŁSUDSKIEGO 3
^6200-078    WARSZAWA         ^63   PL
:62F:C230711USD000000481716,24
:64:C230711USD000000481716,24
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