import re
from time import time
from bs4 import BeautifulSoup

def get_rentals(driver):
    # get source code and parse document as xml
    root_path = 'https://barrettpm.com/residential-rentals/'
    driver.get(root_path)

    # search for listings until listings are found or 20 seconds elapsed
    listings = []
    time_start = time()
    time_elapsed = 0
    while not listings and time_elapsed < 20:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        listings = soup.find_all(class_='tt-rental-row')
        time_elapsed = time() - time_start

    # if 20 seconds elapsed and no listings found, return empty list
    if not listings:
        return listings

    # initialize rental list
    rentals = []

    # get data from each rental listing and add to rental list
    for listing in listings:
        # ignore listing elements that don't have a header
        listing_header = listing.select('h4 a')
        if not listing_header:
            continue
        
        listing_data = {
            'title': get_title(listing),
            'city': get_city(listing),
            'price': get_price(listing),
            'bedrooms': get_bedrooms(listing),
            'bathrooms': get_bathrooms(listing),
            'sqft': get_sqft(listing),
            'url': get_url(listing),
            'company': 'Barrett & Associates',
        }
        rentals.append(listing_data)
    
    return rentals


def get_url(listing):
    try:
        listing_header = listing.select('h4 a')
        url = listing_header[0].get('href')
        return url
    except:
        return None


def get_title(listing):
    try:
        listing_header = listing.select('h4 a')
        title = listing_header[0].getText()
        return title
    except:
        return None


def get_city(listing):
    try:
        city = listing.get('data-city')
        return city
    except:
        return None


def get_price(listing):
    try:
        price = int(float(listing.get('data-rent-amount')))
        return price
    except:
        return None


def get_bedrooms(listing):
    try:
        bedrooms = listing.get('data-beds')
        return bedrooms
    except:
        return None


def get_bathrooms(listing):
    try:
        bathroom_text = listing.get('data-baths')
        regex = re.compile(r'(\d+)\.0')
        converts_to_int = re.search(regex, bathroom_text)
        if converts_to_int:
            bathrooms = converts_to_int.group(1)
            return bathrooms
        return bathrooms
    except:
        return None


def get_sqft(listing):
    try:
        description = listing.select('.rental-description p')[0]
        regex = re.compile(r'Square Feet:(.*?)<br\/>')
        sqft_text = re.search(regex, str(description)).group(1)
        sqft = ''.join(re.findall(r'\d+', sqft_text))
        return sqft
    except:
        return None
