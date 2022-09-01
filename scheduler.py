import time
import schedule
import db_update

schedule.every().hour.at(':00').do(db_update.update)
while True:
    schedule.run_pending()
    time.sleep(1)
