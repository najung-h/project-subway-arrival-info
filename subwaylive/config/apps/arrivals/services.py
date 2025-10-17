import os, requests
from urllib.parse import quote

SEOUL_API_KEY = os.getenv("SEOUL_SUBWAY_API_KEY", "")

def fetch_realtime_arrivals_by_station(station_name: str) -> dict:
    """
    서울교통공사/서울열린데이터포털 실시간 도착 정보 API 예시.
    실제 엔드포인트는 발급 받은 API에 맞춰 수정하세요.
    여기서는 '역명' 단위로 묶어서 호선/상행·하행을 분류하는 형태로 가공.
    """
    if not SEOUL_API_KEY:
        return {"error": "SEOUL_SUBWAY_API_KEY missing"}

    # (예시) /realtimeArrivalStation/<인증키>/json/  ... 는 실제 스펙에 맞추세요.
    url = f"http://swopenapi.seoul.go.kr/api/subway/{SEOUL_API_KEY}/json/realtimeStationArrival/0/100/{quote(station_name)}"
    resp = requests.get(url, timeout=5)
    data = resp.json()

    arrivals = []
    for row in data.get("realtimeArrivalList", []):
        arrivals.append({
            "line": row.get("subwayId"),       # 1001=1호선, ... (실제 맵핑 필요)
            "updnLine": row.get("updnLine"),   # 상행/하행
            "trainLineNm": row.get("trainLineNm"),  # 방면/도착지 설명
            "arvlMsg2": row.get("arvlMsg2"),   # 도착 메시지(2번째)
            "barvlDt": row.get("barvlDt"),     # 도착예정(초)
        })
    # 라인/방향 분류
    grouped = {}
    for a in arrivals:
        key = (a["line"], a["updnLine"])
        grouped.setdefault(key, []).append(a)
    return {"station": station_name, "groups": grouped}
