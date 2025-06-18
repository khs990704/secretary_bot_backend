def get_weather(location: str) -> str:
    dummy_weather_data = {
        "서울": "서울은 맑고 25도입니다.",
        "부산": "부산은 흐리고 22도입니다.",
        "제주": "제주는 흐리고 비가 옵니다.",
    }

    # location이 정확히 없으면 기본 메시지 반환
    return dummy_weather_data.get(location, f"{location}의 날씨 정보를 찾을 수 없습니다.")