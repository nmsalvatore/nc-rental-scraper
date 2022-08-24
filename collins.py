import re
import time
from bs4 import BeautifulSoup
from utils import get_int

def get_collins_data(driver):
    # render Collins Property Management rental list
    root_url = 'https://www.collinspropertymanagement.net'
    driver.get(root_url + '/grass-valley-homes-for-rent')
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    rentals = []

    listings = soup.find_all(class_='listing-container')
    for listing in listings:
        # get url
        href = listing.select('.view-details a.frs-btn')[0].get('href')
        url = root_url + href
        
        # get title
        title = listing.find(class_='address').getText()

        # get city groups with regex
        full_city = listing.find(class_='city').getText()
        city_regex = re.compile(r'(.*),(.*)\s(.*)')
        city_groups = re.search(city_regex, full_city)
        city = city_groups.group(1).strip()

        # get price
        price_str = listing.find(class_='rentAmount').getText()
        price_regex = re.compile(r'(\d+),*(\d+)')
        price_groups = re.search(price_regex, price_str).groups()
        price = int(''.join(price_groups))

        # get bedrooms
        info = listing.find(class_='info').getText()
        bed_regex = re.compile(r'(.*)Bed')
        bedrooms = re.search(bed_regex, info).group(1).strip()
        try:
            bedrooms = int(bedrooms)
        except:
            bedrooms = float(bedrooms)

        # get bathrooms
        bath_regex = re.compile(r'\s(\d.*)Bath')
        bathrooms = re.search(bath_regex, info).group(1).strip()
        try:
            bathrooms = int(bathrooms)
        except:
            bathrooms = float(bathrooms)

        # get square footage
        sqft_str = listing.find(class_='sqft').getText()
        sqft_num_str = ''.join(re.findall(r'\d+', sqft_str))
        try:
            sqft = int(sqft_num_str)
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
