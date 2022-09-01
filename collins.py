import re
import time
from bs4 import BeautifulSoup


def get_rentals(driver):
    # get source code and parse document as xml
    root_path = 'https://www.collinspropertymanagement.net'
    driver.get(root_path + '/grass-valley-homes-for-rent')

    # check for listings until listings are found
    # TODO: check if there are no actual listings
    listings = None
    while not listings:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        listing_class_name = 'listing-container'
        listings = soup.find_all(class_=listing_class_name)

    # initialize rental list
    rentals = []

    print(f'Scanning {len(listings)} listings on {root_path}/')

    # get data from each rental listing and add to rental list
    for listing in listings:
        listing_data = {
            'title': get_title(listing),
            'city': get_city(listing),
            'price': get_price(listing),
            'bedrooms': get_bedrooms(listing),
            'bathrooms': get_bathrooms(listing),
            'sqft': get_sqft(listing),
            'url': get_url(listing, root_path),
        }
        rentals.append(listing_data)    

    return rentals


def get_url(listing, root_path):
    selectors = '.view-details a.frs-btn';
    relative_path = listing.select(selectors)[0].get('href')
    absolute_path = root_path + relative_path
    return absolute_path


def get_title(listing):
    title_el = listing.find(class_='address')
    title = title_el.getText()
    return title


def get_city(listing):
    full_city_el = listing.find(class_='city')
    full_city_str = full_city_el.getText()
    city_regex = re.compile(r'^(.*),\s*[A-Z]{2}')
    city_match = re.search(city_regex, full_city_str)
    city = city_match.group(1).strip()
    return city


def get_price(listing):
    price_el = listing.find(class_='rentAmount')
    price_str = price_el.getText()
    price_regex = re.compile(r'(\d+),*(\d+)')
    price_groups = re.search(price_regex, price_str).groups()
    price = int(''.join(price_groups))
    return price


def get_bedrooms(listing):
    info_el = listing.find(class_='info')
    info_str = info_el.getText()
    bed_regex = re.compile(r'(\d.*)Bed')
    bed_match = re.search(bed_regex, info_str)
    bedrooms = bed_match.group(1).strip()
    return bedrooms


def get_bathrooms(listing):
    info_el = listing.find(class_='info')
    info_str = info_el.getText()
    bath_regex = re.compile(r'\s(\d.*)Bath')
    bath_match = re.search(bath_regex, info_str)
    bathrooms = bath_match.group(1).strip()
    return bathrooms


def get_sqft(listing):
    sqft_el = listing.find(class_='sqft')
    sqft_str = sqft_el.getText()
    sqft = ''.join(re.findall(r'\d+', sqft_str))
    return sqft
