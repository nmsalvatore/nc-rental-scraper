import re
import requests
from bs4 import BeautifulSoup
from utils import get_int

def extract_paul_law_data():
    res = requests.get('https://paullawpropertymanagement.managebuilding.com/Resident/public/rentals')
    soup = BeautifulSoup(res.text, 'lxml')

    rentals = []
    rentals_html = soup.find_all(class_='featured-listing')

    for listing in rentals_html:
        listing_data = {
            'title': listing.find(class_='featured-listing__title').getText(),
            'price': get_int(listing.find(class_='featured-listing__price').getText()),
            'url': 'https://paullawpropertymanagement.managebuilding.com' + listing.get('href')
        }

        listing_url = listing_data.get('url')
        listing_detail_page = requests.get(listing_url)
        listing_detail_html = BeautifulSoup(listing_detail_page.text, 'lxml')
        listing_description = listing_detail_html.find_all(class_='unit-detail__description')
        listing_data['description'] = listing_description[0].getText() or listing_description[1].getText()

        # Find bed, bath and square footage data
        unit_info_items = listing_detail_html.find_all(class_='unit-detail__unit-info-item')
        bed_regex = re.compile(r'.*Bed.*')
        bath_regex = re.compile(r'.*Bath.*')
        sqft_regex = re.compile(r'.*sqft.*')

        for item in unit_info_items:
            if bed_regex.search(item.getText()):
                bedroom_num = get_int(item.getText())
                listing_data['bedrooms'] = bedroom_num
            if bath_regex.search(item.getText()):
                bathroom_num = get_int(item.getText())
                listing_data['bathrooms'] = bathroom_num
            if sqft_regex.search(item.getText()):
                sqft_num = get_int(item.getText())
                listing_data['sqft'] = sqft_num
        
        rentals.append(listing_data)

    return rentals
