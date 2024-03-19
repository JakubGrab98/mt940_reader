import re
from utils import mt940_patterns

mt940_content = """

"""

pattern = re.compile(mt940_patterns.get("description"), re.DOTALL)
match = re.findall(pattern, mt940_content)
print(str(match))  # Returns the entire matched opening balance line
