import re
import time
from bs4 import BeautifulSoup

def get_rentals(driver, root_path, listing_path):
    # get source code and parse document as xml
    driver.get(root_path + listing_path)
    
    # check for listings until listings are found
    # TODO: check if there are no actual listings    
    listings = None
    while not listings:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        listings = soup.find_all(class_='listing-item')

    # initialize rental list
    rentals = []

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
    relative_url_path = listing.find(class_='slider-link').get('href')
    return root_path + relative_url_path


def get_title(listing):
    try:
        address = listing.find(class_='slider-link').getText()
        regex = re.compile(r'(.*),.*,.*')
        title = re.search(regex, address).group(1).strip()
        return title
    except:
        return None


def get_city(listing):
    try:
        address = listing.find(class_='slider-link').getText()
        regex = re.compile(r'.*,(.*),.*')
        city = re.search(regex, address).group(1).strip()
        return city
    except:
        return None


def get_price(listing):
    try:
        price_element = listing.find(class_='rent')
        price_text = price_element.getText().split('.')[0]
        price = int(''.join(re.findall(r'\d+', price_text)))
        return price
    except:
        return None


def get_bedrooms(listing):
    try:
        bed_element = listing.find(class_='beds')
        bed_text = bed_element.getText()
        regex = re.compile(r'^(.*)beds')
        return re.search(regex, bed_text).group(1).strip()
    except:
        return None


def get_bathrooms(listing):
    try:
        bath_element = listing.find(class_='baths')
        bath_text = bath_element.getText()
        regex = re.compile(r'^(.*)bath')
        return re.search(regex, bath_text).group(1).strip()
    except:
        return None


def get_sqft(listing):
    try:
        sqft_element = listing.find(class_='sqft')
        sqft_text = sqft_element.getText()
        regex = re.compile(r'\d+')
        sqft = ''.join(re.findall(regex, sqft_text))
        return sqft
    except:
        return None
