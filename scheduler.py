import time
import schedule
import db_update

schedule.every().day.at('02:00').do(db_update.update)
while True:
    schedule.run_pending()
    time.sleep(1)
