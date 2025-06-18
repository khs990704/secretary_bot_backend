import json
from api.tools import get_weather

def process_function_call(model_response: dict) -> str:
    # 모델이 function_call을 응답했는지 확인
    message = model_response.get("choices", [{}])[0].get("message", {})

    if "function_call" in message:
        name = message["function_call"]["name"]
        args_str = message["function_call"].get("arguments", "{}")

        try:
            args = json.loads(args_str)
        except json.JSONDecodeError:
            return "⚠️ 인식된 함수 인자가 올바르지 않습니다."

        # 함수 이름이 get_weather인 경우
        if name == "get_weather":
            location = args.get("location", "")
            return get_weather(location)

        return f"⚠️ 지원되지 않는 함수: {name}"

    # function_call이 없고 일반 응답만 있는 경우
    return message.get("content", "⚠️ 응답이 비어 있습니다.")