import appfolio

def get_rentals(driver):
    root_path = 'https://www.grassrootspm.com'
    listing_path = '/available-rentals'
    rentals = appfolio.get_rentals(driver, root_path, listing_path)
    return rentals
