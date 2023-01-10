from datetime import datetime
import traceback
import scraper
import db_connect

def update():
    try:
        conn = db_connect.connect()
        cur = conn.cursor()
        changes_made_to_db = False

        rentals = scraper.get_all_rentals()
        for rental in rentals:
            duplicate = check_for_duplicate(cur, rental)
            if duplicate:
                url = rental.get('url')
                db_entry = get_db_entry_by_url(cur, url)
                
                price = rental.get('price')
                if price != db_entry[4]:
                    update_db_entry(cur, 'price', price, url)
                    changes_made_to_db = True

                title = rental.get('title')
                if title != db_entry[1]:
                    update_db_entry(cur, 'title', title, url)
                    changes_made_to_db = True

                bathrooms = rental.get('bathrooms')
                if bathrooms != db_entry[5]:
                    update_db_entry(cur, 'bathrooms', bathrooms, url)
                    changes_made_to_db = True

                bedrooms = rental.get('bedrooms')
                if bedrooms != db_entry[6]:
                    update_db_entry(cur, 'bedrooms', bedrooms, url)
                    changes_made_to_db = True

                sqft = rental.get('sqft')
                if sqft != db_entry[7]:
                    update_db_entry(cur, 'sqft', sqft, url)
                    changes_made_to_db = True

                city = rental.get('city')
                if city != db_entry[9]:
                    update_db_entry(cur, 'city', city, url)
                    changes_made_to_db = True

                company = rental.get('company')
                if company != db_entry[10]:
                    update_db_entry(cur, 'company', company, url)
                    changes_made_to_db = True
                    
            else:
                rental_data = get_rental_data(rental)
                add_to_db(cur, rental_data)
                changes_made_to_db = True
        
        listings_removed = remove_old_listings(cur, rentals)
        if listings_removed:
            changes_made_to_db = True

        if not changes_made_to_db:
            update_time = current_time_formatted()
            print(update_time, 'No changes made to database.')

        conn.commit()
        conn.close()
    except:
        update_time = current_time_formatted()
        with open('error_log.txt', 'a') as f:
            exception = traceback.format_exc()
            f.write('>>> ' + update_time + '\n\n' + exception + '\n')
        print(update_time, 'Update failed. Please view error log for details')


def update_db_entry(cur, update_field, update_value, url):
    if update_value:
        cur.execute(f"""
            UPDATE nc_rentals_listing 
            SET {update_field} = '{update_value}' 
            WHERE url = '{url}'
        """)
    else:
        cur.execute(f"""
            UPDATE nc_rentals_listing 
            SET {update_field} = Null 
            WHERE url = '{url}'
        """)
    update_time = current_time_formatted()
    cur.execute(f"""
        SELECT id FROM nc_rentals_listing WHERE url = '{url}'
    """)
    listing_id = cur.fetchone()[0]
    print(update_time, f'Update to {update_field} field on listing #{listing_id}.')


def get_rental_data(rental):
    return (
        rental.get('title'),
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        rental.get('city'),
        rental.get('price'),
        rental.get('bedrooms'),
        rental.get('bathrooms'),
        rental.get('sqft'),
        rental.get('url'),
        rental.get('company')
    )


def get_old_urls(cur, rentals):
    new_urls = [rental.get('url') for rental in rentals]
    db_urls = get_db_urls(cur)
    old_urls = []
    for url in db_urls:
        url = url[0]
        if url in new_urls:
            continue
        else:
            old_urls.append(url)
    return old_urls


def get_db_urls(cur):
    cur.execute(f'SELECT url FROM nc_rentals_listing')
    db_urls = cur.fetchall()
    return db_urls


def get_db_entry_by_url(cur, url):
    cur.execute(f"SELECT * FROM nc_rentals_listing WHERE url = '{url}'")
    return cur.fetchone()


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
            url,
            company
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, rental_data)
    update_time = current_time_formatted()
    print(update_time, f"'{rental_data[0]}' added to database.")


def remove_from_db(cur, url):
    cur.execute(f"DELETE FROM nc_rentals_listing WHERE url = '{url}'")


def remove_old_listings(cur, rentals):
    old_urls = get_old_urls(cur, rentals)

    if old_urls:
        print('Found old listings')
        rentals = scraper.get_all_rentals()
        old_urls_check = get_old_urls(cur, rentals)
        
        if old_urls == old_urls_check:
            print('Old listings confirmed.')
            for url in old_urls:
                cur.execute(f"""
                    SELECT title FROM nc_rentals_listing WHERE url = '{url}'
                """)
                title = cur.fetchone()[0]
                remove_from_db(cur, url)
                update_time = current_time_formatted()
                print(update_time, f"'{title}' removed from database.")
            return True
    return False


def check_for_duplicate(cur, rental):
    rental_url = rental.get('url')
    cur.execute(f"""
        SELECT url FROM nc_rentals_listing WHERE url = '{rental_url}'
    """)
    duplicate = cur.fetchone()
    return duplicate


def current_time_formatted():
    return datetime.now().strftime('%m/%d/%y %H:%M:%S')
