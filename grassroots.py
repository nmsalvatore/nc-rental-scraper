import re
import time
from bs4 import BeautifulSoup
from utils import get_int

def get_grass_roots_data(driver):
    # Open Property Associates Management Co website in Firefox
    root_url = 'https://www.grassrootspm.com'
    driver.get(root_url + '/available-rentals')

    # Wait 2 seconds for page to fully load
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    rentals = []

    listings = soup.find_all(class_='listing-item')
    for listing in listings:
        # get url
        url = root_url + listing.find(class_='slider-link').get('href')
        
        # get address groups with regex
        address = listing.find(class_='slider-link').getText()
        address_regex = re.compile(r'(.*),(.*),(.*)')
        address_groups = re.search(address_regex, address)

        # get title
        title = address_groups.group(1).strip()

        # get city
        city = address_groups.group(2).strip()

        # get price
        price_str = listing.find(class_='rent').getText()
        price = get_int(price_str)

        # get bedrooms
        bedrooms_el = listing.find(class_='beds')
        if bedrooms_el is not None:
            bedrooms = get_int(bedrooms_el.getText())

        # get bathrooms
        bath_regex = re.compile(r'^\s*(.*)\sbath')
        bath_el = listing.find(class_='baths')
        if bath_el is not None:
            bath_str = re.search(bath_regex, bath_el.getText())
            try:
                bathrooms = int(bath_str.group(1))
            except:
                bathrooms = float(bath_str.group(1))
        
        # get square footage
        sqft_el = listing.find(class_='sqft')
        if sqft_el is not None:
            sqft = get_int(sqft_el.getText())
        else:
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

        print(listing_data)
        rentals.append(listing_data)

    return rentals
