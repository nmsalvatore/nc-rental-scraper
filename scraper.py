from paullaw import get_paul_law_data
from collins import get_collins_data
from pam import get_pam_data
from acm import get_acm_data
from grassroots import get_grass_roots_data
from selenium import webdriver

print('\nChecking for new listings...\n')

paul_law_data = get_paul_law_data()
collins_data = get_collins_data()

# get data from websites requiring selenium
driver = webdriver.Firefox()
pam_data = get_pam_data(driver)
acm_data = get_acm_data(driver)
grass_roots_data = get_grass_roots_data(driver)
driver.close()

def get_all_rentals():
    rentals = paul_law_data + collins_data + pam_data + acm_data + grass_roots_data
    return rentals
