import re

def get_int(str):
    num_str = ''.join(re.findall(r'\d+', str))
    return int(num_str)
