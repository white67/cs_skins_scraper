import sys
sys.path.append('')
from config.config import *
from config.config_database import *
from config.config_buff import *

file = read_json_file("database/skinbid buy take 100.json")
count = len(file["items"])
print(f"count: {count}")