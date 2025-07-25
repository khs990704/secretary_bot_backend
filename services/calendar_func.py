from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import json


SCOPES = ["https://www.googleapis.com/auth/calendar"]

flow = InstalledAppFlow.from_client_secrets_file(
    'calendar_credentials.json',
    SCOPES
)

creds = flow.run_local_server(
    port=0,
    open_browser=True
)

service = build('calendar', 'v3', credentials=creds)

# 이벤트 조회 (5개)
def get_calendar_5events_dummy(service):

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    events_result = service.events().list(
        calendarId = 'primary',
        timeMin=now,
        maxResults=5,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    print(json.dumps(events, indent=2, ensure_ascii=False))

    return events

# 이벤트 조회 (필터링)
def get_calendar_events_filtered(
        service,
        attendee_email=None,
        summary_keyword=None,
        description_keyword=None,
        location_keyword=None,
        creator_email=None,
        date_from=None,
        date_to=None,
        max_results=100
):

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    time_min = date_from.isoformat() if date_from else now
    time_max = date_to.isoformat() if date_to else None

    request_args = {
        "calendarId": "primary",
        "timeMin": time_min,
        "maxResults": max_results,
        "singleEvents": True,
        "orderBy": "startTime"
    }

    if time_max:
        request_args["timeMax"] = time_max

    events_result = service.events().list(**request_args).execute()
    events = events_result.get("items", [])

    filtered = []
    for event in events:
        if summary_keyword and summary_keyword.lower() not in event.get("summary", "").lower():
            continue

        if description_keyword and description_keyword.lower() not in event.get("description", "").lower():
            continue

        if location_keyword and location_keyword.lower() not in event.get("location", "").lower():
            continue

        if creator_email and creator_email.lower() != event.get("creator", {}).get("email", "").lower():
            continue

        if attendee_email:
            attendees = event.get("attendees", [])
            if not any(attendee_email.lower() == a.get("email", "").lower() for a in attendees):
                continue

        filtered.append(event)

    for filter_event in filtered:
        print(json.dumps(filter_event, indent=2, ensure_ascii=False))

    return filtered

# 이벤트 추가
def add_event_to_calendar(service, summary, description, start_time, end_time, timezone, location, attendees_emails=None):

    if attendees_emails is None:
        attendees_emails = []

    attendees = [{"email": email} for email in attendees_emails]

    event = {
        "summary": summary,
        "location": location,
        "description": description,
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": timezone,
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": timezone,
        },
        "attendees": attendees,
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 30},
                {"method": "popup", "minutes": 10},
            ],
        }
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()

    print("[INFO] Event has been added")
    print(f"[INFO] Title : {created_event["summary"]}")
    print(f"[INFO] Link : {created_event.get("htmlLink")}")

# 이벤트 삭제
def delete_event_from_calendar(service, target_summary):

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        q=target_summary,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        print(f"[ERROR] {target_summary} do not exists")
        return

    for event in events:
        if event.get('summary') == target_summary:
            event_id = event['id']

            try:
                service.events().delete(calendarId='primary', eventId=event_id).execute()
                print(f"[INFO] {target_summary} has been deleted successfully")

            except Exception as e:
                print(f"[ERROR] Failed to delete event : {e}")

        else:
            print(f"[ERROR]'{target_summary}' do not exists")

# 이벤트 패치
def patch_event_from_calendar(
        service,
        target_summary,
        new_summary=None,
        new_description=None,
        new_start_time=None,
        new_end_time=None,
        new_timezone=None,
        new_location=None,
        new_attendees_emails=None
):

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        q=target_summary,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        print(f"[ERROR]'{target_summary}' do not exists")
        return

    for event in events:
        if event.get('summary') == target_summary:
            event_id = event['id']
            print(f"[INFO] Event has been detected : {event_id}")

            patch_body = {}

            if new_summary is not None:
                patch_body["summary"] = new_summary

            if new_description is not None:
                patch_body["description"] = new_description

            if new_start_time is not None:
                patch_body.setdefault("start", {})["dateTime"] = new_start_time.isoformat()
                patch_body["start"]["timeZone"] = new_timezone if new_timezone else event["start"].get("timeZone")

            if new_end_time is not None:
                patch_body.setdefault("end", {})["dateTime"] = new_end_time.isoformat()
                patch_body["end"]["timeZone"] = new_timezone if new_timezone else event["end"].get("timeZone")

            if new_location is not None:
                patch_body["location"] = new_location

            if new_attendees_emails is not None:
                patch_body["attendees"] = [{"email": email} for email in new_attendees_emails]

            result = service.events().patch(
                calendarId='primary',
                eventId=event_id,
                body=patch_body
            ).execute()

            print(f"[INFO] {target_summary} has been updated successfully")
            return result

        else:
            print(f"[ERROR] {target_summary} do not exists")


if __name__ == '__main__':
    # 이벤트 조회 테스트
    # get_calendar_5events_dummy(service)

    # 이벤트 조회 필터링 테스트 (교집합)
    get_calendar_events_filtered(
        service,
        # attendee_email="user1@example.com",
        # summary_keyword="테스트",
        # description_keyword="이슈",
        # location_keyword="zoom",
        # creator_email="rlagmltjq74@gmail.com",
        # date_from=datetime.datetime(2025,7,25,17,58, tzinfo=datetime.timezone(datetime.timedelta(hours=9))),
        # date_to=datetime.datetime(2025,7,25,18,58, tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
    )

    # 이벤트 등록 테스트
    # now = datetime.datetime.now(datetime.timezone.utc)
    # start = now + datetime.timedelta(hours=1)
    # end = start + datetime.timedelta(hours=1)
    #
    # add_event_to_calendar(
    #     service=service,
    #     summary="테스트 by api",
    #     description="진행 상황 공유 및 이슈 정리",
    #     start_time=start,
    #     end_time=end,
    #     timezone='Asia/Seoul',
    #     location="온라인 Zoom",
    #     attendees_emails=["user1@example.com", "user2@example.com"]
    # )

    # 이벤트 삭제 테스트
    # delete_event_from_calendar(service, target_summary="테스트 by api 수정")

    # 이벤트 패치 테스트
    # patch_event_from_calendar(
    #     service,
    #     target_summary="테스트 by api",
    #     new_summary="테스트 by api 수정",
    #     new_location="서울",
    #     new_attendees_emails=["origin@example.com", "origin2@example.com"]
    # )