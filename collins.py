import re
from requests_html import HTMLSession
from utils import get_int

def get_collins_data():
    # render Collins Property Management rental list
    session = HTMLSession()
    r = session.get('https://www.collinspropertymanagement.net/grass-valley-homes-for-rent')
    r.html.render()

    rentals = []

    listings = r.html.find('.listing-container .view-details')
    for listing in listings:
        # get url
        url = list(listing.absolute_links)[0]

        # render page
        details = session.get(url)
        details.html.render()
        html = details.html

        # get title
        title = html.find('span.street-address', first=True).text

        # get city
        city_regex = re.compile(r'\n(.*),')
        full_address = html.find('div.prop-address', first=True).text
        city = city_regex.search(full_address).group(1)

        # get list price
        price_str = html.find('div.prop-rent.text-alt', first=True).text
        price = get_int(price_str)

        # get bedrooms
        bed_str = html.find('div.prop-beds', first=True).text
        bedrooms = get_int(bed_str)

        # get bathrooms
        bath_regex = re.compile(r'\s*(.*)\sba')
        bath_str = html.find('div.prop-baths', first=True).text
        try:
            bathrooms = int(bath_regex.search(bath_str).group(1))
        except:
            bathrooms = float(bath_regex.search(bath_str).group(1))

        # get square footage
        sqft_str = html.find('div.prop-area', first=True).text
        sqft = get_int(sqft_str)

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
