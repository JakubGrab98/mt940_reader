import re
from utils import mt940_patterns

mt940_content = """
:20:1
:25:/PL1111111111111111111
:28C:00041
:60F:C240312EUR000001561522,39
:61:2403140314CR000000003655,00N230NONREF
:86:230^00PRZELEW                    ^34000
^3012400001^38PL37124000010000008211978100
^20/TEST      ^21        TEST
^2224
^2633B 3675,EUR 71F 0,EUR 71F ^2720,EUR                     
^321077664213                 ^33        TEST
^623625 TEST    ^63        KW00003655.00EUR PR
^64000.00
:62F:C240314EUR000001565177,39
:64:C240314EUR000001565177,39
-
"""

pattern = re.compile(mt940_patterns.get("rate_details"), re.MULTILINE)
match = re.findall(pattern, mt940_content)
print(match)  # Returns the entire matched opening balance line
