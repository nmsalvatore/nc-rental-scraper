import itertools

from selenium import webdriver

import paullaw
import collins
import pam
import acm
import grassroots
import barrett


def get_all_rentals():
    # get data using requests module
    paul_law_data = paullaw.get_rentals()

    # get data using selenium module
    driver = webdriver.Firefox()
    collins_data = collins.get_rentals(driver)
    pam_data = pam.get_rentals(driver)
    acm_data = acm.get_rentals(driver)
    grass_roots_data = grassroots.get_rentals(driver)
    barrett_data = barrett.get_rentals(driver)
    driver.close()
    
    all_rental_data = [
        paul_law_data,
        collins_data,
        pam_data,
        acm_data,
        grass_roots_data,
        barrett_data
    ]

    return list(itertools.chain(*all_rental_data))
