from paullaw import get_paul_law_data
from collins import get_collins_data

print('\nRetrieving all available rental data...\n')

paul_law_data = get_paul_law_data()
collins_data = get_collins_data()

print('Rental data retrieved successfully.\n')
