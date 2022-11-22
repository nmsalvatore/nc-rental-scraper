import time
import schedule
import db_update


def get_formatted_times_in_range(first_hour, final_hour):
    times = []
    for num in range(first_hour, final_hour+1):
        formatted_time = f'{str(num)}:00'
        if num < 10:
            formatted_time = '0' + formatted_time
        times.append(formatted_time)
    return times


def schedule_updates():
    update_times = get_formatted_times_in_range(6,20)
    for update_time in update_times:
        schedule.every().day.at(update_time).do(db_update.update)


print()

schedule_updates()
while True:
    schedule.run_pending()
    time.sleep(1)
