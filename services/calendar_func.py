from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime

SCOPES = ["https://www.googleapis.com/auth/calendar"]

flow = InstalledAppFlow.from_client_secrets_file(
    'calendar_credentials.json',
    SCOPES
)

creds = flow.run_local_server(port=0)

service = build('calendar', 'v3', credentials=creds)

# 이벤트 조회 테스트 (5개)
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
    print(events)

    return events

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

    print("✅ 이벤트가 추가되었습니다:")
    print("📅 제목:", created_event["summary"])
    print("📎 링크:", created_event.get("htmlLink"))

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
        print(f"'{target_summary}' 이벤트가 존재하지 않습니다.")
        return

    for event in events:
        if event.get('summary') == target_summary:
            event_id = event['id']

            try:
                service.events().delete(calendarId='primary', eventId=event_id).execute()
                print(f"✅ 이벤트ID: {event_id}이(가) 성공적으로 삭제되었습니다")

            except Exception as e:
                print(f"❌ 이벤트를 제거하는데 실패하였습니다 (error: {e})")

        else:
            print(f"'{target_summary}'에 부합하는 이벤트가 존재하지 않습니다.")


if __name__ == '__main__':
    # 이벤트 조회 테스트
    # get_calendar_5events_dummy(service)

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
    delete_event_from_calendar(service, target_summary="테스트 by api")