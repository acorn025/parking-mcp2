"""
주차장 정보 조회 MCP 서버
"""

from typing import List, Dict, Optional, Any, Tuple
from fastmcp import FastMCP

from src.api_clients import (
    KakaoLocalClient,
    SeoulDataClient,
    GyeonggiDataClient,
)

app = FastMCP("Parking Info Server")


def _is_seoul(address: str) -> bool:
    return "서울" in address or "서울시" in address or "서울특별시" in address


def _is_gyeonggi(address: str) -> bool:
    return "경기" in address or "경기도" in address


def _get_region(address: str) -> str:
    if _is_seoul(address):
        return "seoul"
    elif _is_gyeonggi(address):
        return "gyeonggi"
    return "other"


# -------------------------------
# 공통 포맷 함수 (⭐️ 핵심 수정)
# -------------------------------
def _format_parking_info(
    parking_data: Dict[str, Any],
    region: str,
    realtime_info: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:

    result = {
        "name": parking_data.get("name", "주차장"),
        "address": parking_data.get("address", ""),
        "total_spots": parking_data.get("total_spots"),
        "fee": parking_data.get("fee"),
    }

    # 모든 실패 / 미제공 케이스 통합 처리
    if not isinstance(realtime_info, dict) or realtime_info.get("status") == "unavailable":
        result["available_spots"] = None
        result["realtime_message"] = "주차 정보가 없습니다"
        return result

    # 정상 데이터만 아래로 내려옴
    result["available_spots"] = realtime_info.get("available_spots")
    result["total_spots"] = realtime_info.get("total_spots") or result.get("total_spots")

    if realtime_info.get("operating_info"):
        result["operating_info"] = realtime_info.get("operating_info")

    if realtime_info.get("fee_info"):
        result["fee_info"] = realtime_info.get("fee_info")

    if region == "seoul":
        result["update_time"] = realtime_info.get("update_time")

    return result


# -------------------------------
# 서울 실시간 정보
# -------------------------------
def _get_realtime_info_seoul(parking_name: str, address: str) -> Dict[str, Any]:
    try:
        client = SeoulDataClient()
        response = client.get_realtime_parking_info(1, 1000)

        if response.get("status") == "success":
            rows = response.get("data", {}).get("GetParkingInfo", {}).get("row", [])
            for p in rows:
                if parking_name in p.get("PKLT_NM", "") or address in p.get("ADDR", ""):
                    total = int(p.get("TPKCT", 0))
                    current = int(p.get("NOW_PRK_VHCL_CNT", 0))
                    return {
                        "available_spots": max(0, total - current),
                        "total_spots": total,
                        "update_time": p.get("NOW_PRK_VHCL_UPDT_TM"),
                        "operating_info": {
                            "status": p.get("PRK_STTS_NM", "")
                        },
                        "fee_info": {
                            "basic_fee": p.get("BSC_PRK_CRG", 0),
                            "daily_max_fee": p.get("DAY_MAX_CRG", 0),
                        }
                    }
    except Exception:
        pass

    return {
        "status": "unavailable",
        "message": "주차 정보가 없습니다"
    }


# -------------------------------
# 경기 정보 (실시간 대수 없음)
# -------------------------------
def _get_realtime_info_gyeonggi(parking_name: str, address: str) -> Dict[str, Any]:
    try:
        client = GyeonggiDataClient()
        response = client.get_realtime_parking_info(page=1, size=100)

        if response.get("status") == "success":
            places = response.get("data", {}).get("ParkingPlace", [])
            rows = places[1].get("row", []) if isinstance(places, list) and len(places) > 1 else []

            for p in rows:
                if parking_name in p.get("PARKPLC_NM", ""):
                    return {
                        "total_spots": p.get("PARKNG_COMPRT_PLANE_CNT"),
                        "available_spots": None,
                        "operating_info": {},
                        "fee_info": {}
                    }
    except Exception:
        pass

    return {
        "status": "unavailable",
        "message": "주차 정보가 없습니다"
    }


# -------------------------------
# 주소 → 좌표
# -------------------------------
def _address_to_coordinates(address: str) -> Tuple[Optional[float], Optional[float]]:
    try:
        client = KakaoLocalClient()
        response = client.address_to_coordinates(address)
        docs = response.get("data", {}).get("documents", [])
        if docs:
            return float(docs[0]["y"]), float(docs[0]["x"])
    except Exception:
        pass
    return None, None


# -------------------------------
# MCP Tool
# -------------------------------
@app.tool()
def search_nearby_parking(address: str) -> dict:
    lat, lng = _address_to_coordinates(address)
    if lat is None or lng is None:
        return {
            "success": True,
            "parkings": [],
            "count": 0,
            "notice": "주차 정보가 없습니다"
        }

    kakao = KakaoLocalClient()
    response = kakao.search_parking_nearby(lat, lng, 1000, 10)
    parkings = []

    for p in response.get("data", {}).get("documents", []):
        addr = p.get("address_name", "")
        region = _get_region(addr)

        realtime = (
            _get_realtime_info_seoul(p["place_name"], addr) if region == "seoul"
            else _get_realtime_info_gyeonggi(p["place_name"], addr) if region == "gyeonggi"
            else {"status": "unavailable"}
        )

        standard = {
            "name": p["place_name"],
            "address": addr,
            "total_spots": None,
            "fee": None
        }

        parkings.append(_format_parking_info(standard, region, realtime))

    return {
        "success": True,
        "parkings": parkings,
        "count": len(parkings)
    }


@app.tool()
def mcp_health_check(address: str) -> dict:
    return {
        "content": [
            {
                "type": "text",
                "text": f"MCP Tool 호출이 정상적으로 동작했습니다. 입력 주소: {address}"
            }
        ]
    }


def main():
    app.run()


if __name__ == "__main__":
    main()
