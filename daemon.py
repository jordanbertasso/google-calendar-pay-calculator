import datetime
import threading
import time

next_call = time.time()

def main(service, CALENDAR_ID, PAY_RATE):
    # Call the calendar API
    now = datetime.datetime.utcnow()
    begin = now - datetime.timedelta(days=7)
    begin = begin.isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(
        calendarId=CALENDAR_ID, timeMin=begin,
        singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return

    for event in events:
        try:
            if 'work' in event['summary'].lower() and '$' not in event['summary']:
                print(f'Old Title: {event["summary"]}')
                update_title(service, event, CALENDAR_ID, PAY_RATE)
        except Exception as e:
            continue

    global next_call
    next_call = next_call+5
    threading.Timer(next_call - time.time(), main, [service, CALENDAR_ID, PAY_RATE]).start()


def calculate_seconds(service, event):
    startTimeString = event['start']['dateTime']
    date_time_obj_start = datetime.datetime.strptime(
        startTimeString, '%Y-%m-%dT%H:%M:%S%z')

    endTimeString = event['end']['dateTime']
    date_time_obj_end = datetime.datetime.strptime(
        endTimeString, '%Y-%m-%dT%H:%M:%S%z')

    length_obj = date_time_obj_end - date_time_obj_start

    return length_obj.total_seconds()


def update_title(service, event, CALENDAR_ID, PAY_RATE):
    hours = calculate_seconds(service, event)/3600
    if hours >= 5.0:
        pay = PAY_RATE * (hours-0.5)
    else:
        pay = hours * PAY_RATE

    pay = round(pay, 2)

    new_summary = f'{event["summary"]} - ${pay}'
    event['summary'] = new_summary

    print(f'[{datetime.datetime.now()}]: New Title: {new_summary}')

    service.events().update(
        calendarId=CALENDAR_ID,
        eventId=event['id'],
        body=event
    ).execute()


if __name__ == '__main__':
    print("Please run this module via main.py")
    exit(1)
