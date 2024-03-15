import re
from regex_dict import patterns

mt940_content = """
:20:1
:25:/PL50124062921978001062009446
:28C:00041
:60F:C240312EUR000001561522,39
:61:2403140314CR000000003655,00N230NONREF
:86:230^00PRZELEW                    ^34000
^3012400001^38PL37124000010000008211978100
^20/RFB/VAT ID 525157859      ^21        INVOICE FVS014EUR20
^2224
^2633B 3675,EUR 71F 0,EUR 71F ^2720,EUR                     
^321077664213                 ^33        JAMESTOWN LP
^623625 CUMBERLAND BLVD SE    ^63        KW00003655.00EUR PR
^64000.00
:62F:C240314EUR000001565177,39
:64:C240314EUR000001565177,39
-
"""

pattern = re.compile(patterns.get("transaction_details"), re.MULTILINE)
match = re.findall(pattern, mt940_content)
print(match[0][1])  # Returns the entire matched opening balance line
