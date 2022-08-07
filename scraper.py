import re
import requests
from bs4 import BeautifulSoup
from paullaw import extract_paul_law_data

paul_law_data = extract_paul_law_data()
rentals = paul_law_data
print(rentals)