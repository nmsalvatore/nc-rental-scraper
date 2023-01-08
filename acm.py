import appfolio

def get_rentals(driver):
    root_path = 'https://www.acmrents.com'
    listing_path = '/residential-2'
    rentals = appfolio.get_rentals(driver, root_path, listing_path)

    # add company name to listing data
    for rental in rentals:
        rental['company'] = 'ACM Property Management';

    return rentals