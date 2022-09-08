import re
import requests
from bs4 import BeautifulSoup


def get_rentals():
    root_path = 'https://paullawpropertymanagement.managebuilding.com'
    res = requests.get(root_path + '/Resident/public/rentals')
    
    listings = None
    while not listings:
        soup = BeautifulSoup(res.text, 'lxml')
        listing_class_name = 'featured-listing'
        listings = soup.find_all(class_=listing_class_name)

    rentals = []

    for listing in listings:
        listing_data = {
            'title': get_title(listing),
            'city': get_city(listing),
            'price': get_price(listing),
            'bedrooms': get_bedrooms(listing),
            'bathrooms': get_bathrooms(listing),
            'sqft': get_square_feet(listing),
            'url': get_url(listing, root_path),
        }
        rentals.append(listing_data)
    return rentals


def get_url(listing, root):
    relative_path = listing.get('href')
    absolute_path = root + relative_path
    return absolute_path


def get_title(listing):
    title_class_name = 'featured-listing__title'
    title_el = listing.find(class_=title_class_name)
    title = title_el.getText()
    return title


def get_city(listing):
    city_regex = re.compile(r'^(.*),')
    city_match = re.search(city_regex, listing.get('data-location'))
    city = city_match.group(1)
    return city


def get_price(listing):
    price_str = listing.get('data-rent')
    price = int(price_str)
    return price


def get_bedrooms(listing):
    bedrooms = listing.get('data-bedrooms')
    if bedrooms == '0':
        return None
    return bedrooms


def get_bathrooms(listing):
    bathrooms = listing.get('data-bathrooms')
    if bathrooms == '0':
        return None
    return bathrooms


def get_square_feet(listing):
    sqft = listing.get('data-square-feet')
    if sqft == '0':
        return None
    return sqft
