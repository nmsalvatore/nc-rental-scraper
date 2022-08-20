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

conn.commit()
conn.close()

if new_listing_count == 1:
    print(f'{new_listing_count} new listing added to the database.\n')
else:
    print(f'{new_listing_count} new listings added to the database.\n')