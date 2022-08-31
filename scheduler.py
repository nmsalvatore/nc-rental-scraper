import time
import schedule
import db_update

schedule.every().hour.do(db_update.update)
while True:
    schedule.run_pending()
    time.sleep(1)
