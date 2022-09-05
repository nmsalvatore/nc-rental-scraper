import itertools

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import paullaw
import collins
import pam
import acm
import grassroots
import barrett
import mvalley


def get_all_rentals():
    # get data using requests module
    paul_law_data = paullaw.get_rentals()

    # get data using selenium module
    firefox_options = Options()
    firefox_options.headless = True
    driver = webdriver.Firefox(options=firefox_options)
    collins_data = collins.get_rentals(driver)
    pam_data = pam.get_rentals(driver)
    acm_data = acm.get_rentals(driver)
    grass_roots_data = grassroots.get_rentals(driver)
    barrett_data = barrett.get_rentals(driver)
    mvalley_data = mvalley.get_rentals(driver)
    driver.close()
    
    all_rental_data = [
        paul_law_data,
        collins_data,
        pam_data,
        acm_data,
        grass_roots_data,
        barrett_data,
        mvalley_data
    ]

    return list(itertools.chain(*all_rental_data))
