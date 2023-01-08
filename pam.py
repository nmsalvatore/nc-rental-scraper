import appfolio

def get_rentals(driver):
    root_path = 'https://www.nevadacounty4rent.com'
    listing_path = '/available-rentals'
    rentals = appfolio.get_rentals(driver, root_path, listing_path)

    # add company name to listing data
    for rental in rentals:
        rental['company'] = 'Property Associates Management Co.';

    return rentals
