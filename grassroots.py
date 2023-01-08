import appfolio

def get_rentals(driver):
    root_path = 'https://www.grassrootspm.com'
    listing_path = '/available-rentals'
    rentals = appfolio.get_rentals(driver, root_path, listing_path)

    # add company name to listing data
    for rental in rentals:
        rental['company'] = 'Grass Roots Property Management';

    return rentals
