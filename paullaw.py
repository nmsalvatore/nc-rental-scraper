import re
import requests
from bs4 import BeautifulSoup
from utils import get_int

def get_paul_law_data():
    root = 'https://paullawpropertymanagement.managebuilding.com'
    res = requests.get(root + '/Resident/public/rentals')
    soup = BeautifulSoup(res.text, 'lxml')

    rentals = []

    listings = soup.find_all(class_='featured-listing')
    for listing in listings:
        # get url
        url = root + listing.get('href')

        # get title
        title = listing.find(class_='featured-listing__title').getText()

        # get city
        full_address = listing.find(class_='featured-listing__address').getText()
        city_regex = re.compile(r'^(.*),')
        city = city_regex.search(full_address).group(1)

        # get price
        price_str = listing.find(class_='featured-listing__price').getText()
        price = get_int(price_str)

        # render listing detail view
        detail_view = requests.get(url)
        detail_html = BeautifulSoup(detail_view.text, 'lxml')

        # get bed, bath and square footage
        unit_info = detail_html.find_all(class_='unit-detail__unit-info-item')
        for item in unit_info:
            bed_regex = re.compile(r'.*Bed.*')
            if bed_regex.search(item.getText()):
                bedrooms = get_int(item.getText())

            bath_regex = re.compile(r'.*Bath.*')
            if bath_regex.search(item.getText()):
                bathrooms = get_int(item.getText())

            sqft_regex = re.compile(r'.*sqft.*')
            if sqft_regex.search(item.getText()):
                sqft = get_int(item.getText())

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
