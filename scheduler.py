import time
import schedule
import db_update

print('\nNOTE: Updates will occur every hour on the hour.\n')
schedule.every().hour.at(':00').do(db_update.update)
while True:
    schedule.run_pending()
    time.sleep(1)
