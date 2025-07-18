# backend/app/tools/calendar_tools.py

import os
import json
from datetime import datetime, timedelta, timezone
from langchain_core.tools import tool
from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import List

# --- GOOGLE CALENDAR AUTHENTICATION ---

# Define the scopes required for the Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID", "primary")

def get_calendar_service():
    """
    Authenticates with the Google Calendar API using service account credentials
    loaded from the GOOGLE_SERVICE_ACCOUNT_JSON environment variable.
    """
    # 1. Get the JSON credentials string from the environment variable
    creds_json_str = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if not creds_json_str:
        raise ValueError("The GOOGLE_SERVICE_ACCOUNT_JSON environment variable is not set.")

    # 2. Load the JSON string into a Python dictionary
    try:
        creds_info = json.loads(creds_json_str)
    except json.JSONDecodeError:
        raise ValueError("Failed to decode GOOGLE_SERVICE_ACCOUNT_JSON. Check its format in the .env file.")

    # 3. Define the required scopes
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']

    # 4. Create credentials from the dictionary
    creds = service_account.Credentials.from_service_account_info(creds_info, scopes=SCOPES)
    
    # 5. Build and return the service object
    service = build('calendar', 'v3', credentials=creds)
    return service

# --- LANGCHAIN TOOLS ---

@tool
def check_availability(date: str) -> str:
    """
    Checks for available appointment slots on a given date, assuming 9 AM to 5 PM working hours.
    Args:
        date (str): The date to check for availability in 'YYYY-MM-DD' format.
    Returns:
        str: A summary of available time slots for the given date.
    """
    try:
        service = get_calendar_service()
        
        # Parse the date and set the time range for the working day (9 AM to 5 PM)
        start_of_day = datetime.fromisoformat(f"{date}T09:00:00")
        end_of_day = datetime.fromisoformat(f"{date}T17:00:00")
        
        # Adjust to local timezone (or a specific one if needed)
        tz = timezone.utc # Or use a specific timezone
        start_of_day = start_of_day.astimezone(tz)
        
        end_of_day = end_of_day.astimezone(tz)

        # Fetch events from the calendar
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=start_of_day.isoformat(),
            timeMax=end_of_day.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items',)

        if not events:
            return f"The entire day from 9 AM to 5 PM is free on {date}."

        # Calculate free slots
        free_slots = []
        current_time = start_of_day
        for event in events:
            event_start = datetime.fromisoformat(event['start'].get('dateTime'))
            event_end = datetime.fromisoformat(event['end'].get('dateTime'))

            if current_time < event_start:
                free_slots.append(f"{current_time.strftime('%I:%M %p')} to {event_start.strftime('%I:%M %p')}")
            current_time = event_end

        if current_time < end_of_day:
            free_slots.append(f"{current_time.strftime('%I:%M %p')} to {end_of_day.strftime('%I:%M %p')}")

        if not free_slots:
            return f"No availability on {date} between 9 AM and 5 PM."
        
        return f"Available slots on {date}: {', '.join(free_slots)}."

    except Exception as e:
        return f"An error occurred while checking availability: {e}"


@tool
def book_appointment(start_time: str, end_time: str, summary: str) -> str:
    """
    Books an appointment on the Google Calendar.
    Args:
        start_time (str): The start time of the appointment in ISO format (e.g., '2024-07-18T10:00:00').
        end_time (str): The end time of the appointment in ISO format (e.g., '2024-07-18T11:00:00').
        summary (str): A brief summary or title for the appointment.
    Returns:
        str: A confirmation message with the event link if successful, or an error message.
    """
    try:
        service = get_calendar_service()
        
        # Assume UTC if no timezone is provided
        tz = timezone.utc
        start_dt = datetime.fromisoformat(start_time).astimezone(tz)
        end_dt = datetime.fromisoformat(end_time).astimezone(tz)

        event = {
            'summary': summary,
            'start': {
                'dateTime': start_dt.isoformat(),
                'timeZone': str(tz),
            },
            'end': {
                'dateTime': end_dt.isoformat(),
                'timeZone': str(tz),
            },
        }

        created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        return f"Appointment booked successfully! View event: {created_event.get('htmlLink')}"

    except Exception as e:
        return f"An error occurred while booking the appointment: {e}"