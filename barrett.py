import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from utils import get_int

def get_barrett_data(driver):
    # render Collins Property Management rental list
    driver.get('https://barrettpm.com/residential-rentals/')
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    rentals = []
    listings = soup.find_all(class_='tt-rental-row')
    for listing in listings:
        # ignore listing elements that don't have a header
        listing_header = listing.select('h4 a')
        if not listing_header:
            continue

        # get url
        url = listing_header[0].get('href')
        
        # get title
        title = listing_header[0].getText()

        # get city
        city = listing.get('data-city')

        # get price
        price = int(float(listing.get('data-rent-amount')))

        # get bedrooms
        bed_str = listing.get('data-beds')
        try:
            bedrooms = int(bed_str)
        except:
            bedrooms = float(bed_str)

        # get bathrooms
        bath_str = listing.get('data-baths')
        try:
            bathrooms = int(bath_str)
        except:
            bathrooms = float(bath_str)

        # get square footage
        # TODO: remove dependence on 'Parking' in regex; clean up this whole section
        description = listing.select('.rental-description p')[0]
        sqft_regex = re.compile(r'Square Feet:(.*)<br/>Parking?')
        try:
            sqft = get_int(re.search(sqft_regex, str(description)).group(1))
        except:
            sqft = None
        
        listing_data = {
            'title': title,
            'city': city,
            'price': price,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'sqft': sqft,
            'url': url,
        }

        rentals.append(listing_data)
    
    return rentals
