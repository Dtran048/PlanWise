import requests 
from icalendar import Calendar 

CANVAS_ICAL_URL = "https://csufullerton.instructure.com/feeds/calendars/user_hQixLZNNkOaHsiyE60nh4Wp5bWgJbfLMwH2ggkr1.ics"

def fetch_canvas_assignments():
    response = requests.get(CANVAS_ICAL_URL)

    if response.status_code == 200:
        cal = Calendar.from_ical(response.content)
        print("Successfully fetched Canvas assignments:\n")

        #this parses the assignments
        for component in cal.walk('vevent'):
            task_name = component.get('summary')
            due_date = component.get('dtstart').dt
            print(f"Task: {task_name}, Due Date: {due_date}")

    else:
        print("Failed to connect to the Canvas feed.")

fetch_canvas_assignments()
