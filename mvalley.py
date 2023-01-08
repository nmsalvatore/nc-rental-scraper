import re
from time import time
from bs4 import BeautifulSoup


def get_rentals(driver):
    # get source code and parse document as xml
    driver.get('https://www.mvalleypm.com/grass-valley-homes-for-rent')
    driver.switch_to.frame('af_iframe_0')

    # search for listings until listings are found or 20 seconds elapsed
    listings = []
    time_start = time()
    time_elapsed = 0
    while not listings and time_elapsed < 20:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        listings = soup.find_all(class_='listing-item')
        time_elapsed = time() - time_start

    # if 20 seconds elapsed and no listings found, return empty list
    if not listings:
        return listings

    rentals = []

    for listing in listings:
        listing_data = {
            'title': get_title(listing),
            'city': get_city(listing),
            'price': get_price(listing),
            'bedrooms': get_bedrooms(listing),
            'bathrooms': get_bathrooms(listing),
            'sqft': get_sqft(listing),
            'url': get_url(listing),
            'company': 'Mountain Valley Property Management, Inc.'
        }
        rentals.append(listing_data)

    return rentals


def get_url(listing):
    root_path = 'https://mountainvalleypm.appfolio.com'
    relative_path = listing.a.get('href')
    return root_path + relative_path


def get_title(listing):
    address = listing.find(class_='js-listing-address').getText()
    regex = re.compile(r'(.*),(.*),')
    title = re.search(regex, address).group(1).strip()
    return title


def get_city(listing):
    address = listing.find(class_='js-listing-address').getText()
    regex = re.compile(r'(.*),(.*),')
    title = re.search(regex, address).group(2).strip()
    return title


def get_price(listing):
    price_text = listing.find(class_='detail-box__value').getText()
    regex = re.compile(r'\d+')
    price = ''.join(re.findall(regex, price_text))
    return int(price)


def get_bedrooms(listing):
    details = listing.find_all(class_='detail-box__value')
    for detail in details:
        detail_value = detail.getText()
        if 'bd' in detail_value:
            try:
                regex = re.compile(r'(\d+)\s*bd')
                bedrooms = re.search(regex, detail_value).group(1)
                return bedrooms
            except:
                return None
    return None


def get_bathrooms(listing):
    details = listing.find_all(class_='detail-box__value')
    for detail in details:
        detail_value = detail.getText()
        if 'ba' in detail_value:
            try:
                regex = re.compile(r'(\d+\.*\d*)\s*ba')
                bathrooms = re.search(regex, detail_value).group(1)
                return bathrooms
            except:
                return None
    return None


def get_sqft(listing):
    detail_items = listing.find_all(class_='detail-box__item')
    for item in detail_items:
        detail_label = item.find(class_='detail-box__label').getText()
        if 'Square Feet' in detail_label:
            detail_value = item.find(class_='detail-box__value').getText()
            try:
                regex = re.compile(r'\d+')
                sqft = ''.join(re.findall(regex, detail_value))
                return sqft
            except:
                return None
    return None
