from datetime import datetime
import scraper
import db_connect


def update():
    print('\nPerforming update on database...\n')
    conn = db_connect.connect()
    cur = conn.cursor()
    rentals = scraper.get_all_rentals()
    for rental in rentals:
        duplicate = check_for_duplicate(cur, rental)
        if not duplicate:
            rental_data = get_rental_data(rental)
            add_to_db(cur, rental_data)
            print(f"'{rental.get('title')}' added to database.")
    remove_old_listings(cur, rentals)
    conn.commit()
    conn.close()
    print('\nUpdate complete.\n')


def get_rental_data(rental):
    return (
        rental.get('title'),
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        rental.get('city'),
        rental.get('price'),
        rental.get('bedrooms'),
        rental.get('bathrooms'),
        rental.get('sqft'),
        rental.get('url')
    )


def get_old_urls(cur, rentals):
    new_urls = [rental.get('url') for rental in rentals]
    db_urls = get_db_urls(cur)
    old_urls = []
    for url in db_urls:
        url = url[0]
        if url in new_urls:
            continue
        old_urls.append(url)
    return old_urls


def get_db_urls(cur):
    cur.execute(f'SELECT url FROM nc_rentals_listing')
    db_urls = cur.fetchall()
    return db_urls


def add_to_db(cur, rental_data):
    cur.execute("""
        INSERT INTO nc_rentals_listing (
            title, 
            date_added, 
            city, 
            price, 
            bedrooms, 
            bathrooms, 
            sqft, 
            url
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, rental_data)


def remove_from_db(cur, url):
    cur.execute(f"DELETE FROM nc_rentals_listing WHERE url = '{url}'")


def remove_old_listings(cur, rentals):
    old_urls = get_old_urls(cur, rentals)
    if old_urls:
        for url in old_urls:
            cur.execute(f"""
                SELECT title FROM nc_rentals_listing WHERE url = '{url}'
            """)
            title = cur.fetchone()[0]
            remove_from_db(cur, url)
            print(f"'{title}' removed from database.")


def check_for_duplicate(cur, rental):
    rental_url = rental.get('url')
    cur.execute(f"""
        SELECT url FROM nc_rentals_listing WHERE url = '{rental_url}'
    """)
    duplicate = cur.fetchone()
    return duplicate
