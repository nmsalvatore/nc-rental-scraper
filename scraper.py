import itertools

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import paullaw
import collins
import pam
import acm
import grassroots
import barrett
import mvalley
import tk


def get_all_rentals():
    # get data using requests module
    paul_law_data = paullaw.get_rentals()
    tk_data = tk.get_rentals()

    # get data using selenium module
    options = Options()
    options.add_argument('--headless')
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'), options=options)
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
        mvalley_data,
        tk_data
    ]

    return list(itertools.chain(*all_rental_data))
