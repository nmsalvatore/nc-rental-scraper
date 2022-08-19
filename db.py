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
for rental in rentals:
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

conn.commit()
conn.close()
