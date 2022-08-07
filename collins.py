from requests_html import HTMLSession

def get_collins_data():
    session = HTMLSession()
    r = session.get('https://www.collinspropertymanagement.net/grass-valley-homes-for-rent')
    r.html.render()

    rentals = []

    listings = r.html.find('.listing-container .view-details')
    for listing in listings:
        url = list(listing.absolute_links)[0]
        details = session.get(url)
        details.html.render()

        listing_data = {
            'title': details.html.find('span.street-address', first=True).text,
            'city': details.html.find('div.prop-address', first=True).text
        }
        rentals.append(listing_data)

    print(rentals)
    return rentals

get_collins_data()