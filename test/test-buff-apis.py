import sys
sys.path.append('')
from config.config import *

file1 = read_json_file("database/buff-ak-pg1-size100.json")

counter = 0
for item in file1["data"]["items"]:
    counter += 1
    
print(f"Item counter: {counter}")