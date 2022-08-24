from datetime import datetime

import psycopg2
import dotenv
import os

from scraper import get_all_rentals

dotenv.load_dotenv()

conn = psycopg2.connect(
    dbname=os.environ['DB_NAME'],
    user=os.environ['DB_USER'],
)
cur = conn.cursor()

rentals = get_all_rentals()
new_listing_count = 0

for rental in rentals:
    # check if listing is already in the database
    rental_url = rental.get('url')
    cur.execute(f"SELECT url FROM nc_rentals_listing WHERE url = '{rental_url}'")
    db_entry = cur.fetchone()
    
    # if listing is not in the database, insert it into database
    if not db_entry:
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
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""", 
            (
                rental.get('title'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                rental.get('city'),
                rental.get('price'),
                rental.get('bedrooms'),
                rental.get('bathrooms'),
                rental.get('sqft'),
                rental.get('url')
            ))

        new_listing_count += 1

# remove old listings
new_listing_urls = [rental.get('url') for rental in rentals]
cur.execute(f'SELECT url FROM nc_rentals_listing')
db_listing_urls = cur.fetchall()
db_removed_count = 0

for db_listing_url in db_listing_urls:
    db_listing_url = db_listing_url[0]
    if db_listing_url in new_listing_urls:
        continue
    cur.execute(f"DELETE FROM nc_rentals_listing WHERE url = '{db_listing_url}'")
    db_removed_count += 1

conn.commit()
conn.close()

if new_listing_count == 1:
    print(f'{new_listing_count} new listing added to the database.\n')
else:
    print(f'{new_listing_count} new listings added to the database.\n')

if db_removed_count == 1:
    print(f'{db_removed_count} listing removed from database.\n')
else:
    print(f'{db_removed_count} listings removed from database.\n')