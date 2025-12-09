"""
주차장 정보 조회 MCP 서버
"""

import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Any
from fastmcp import FastMCP

from .api_clients import (
    PublicDataClient,
    SeoulDataClient,
    GyeonggiDataClient,
)

# MCP 앱 인스턴스 생성
app = FastMCP("Parking Info Server")


def _is_seoul(address: str) -> bool:
    """주소가 서울 지역인지 확인"""
    return "서울" in address or "서울시" in address or "서울특별시" in address


def _is_gyeonggi(address: str) -> bool:
    """주소가 경기 지역인지 확인"""
    return "경기" in address or "경기도" in address


def _get_region(address: str) -> str:
    """주소에서 지역 구분 (seoul, gyeonggi, other)"""
    if _is_seoul(address):
        return "seoul"
    elif _is_gyeonggi(address):
        return "gyeonggi"
    else:
        return "other"


def _format_parking_info(
    parking_data: Dict[str, Any],
    region: str,
    realtime_info: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    주차장 정보를 표준 형식으로 포맷팅
    
    Args:
        parking_data: 기본 주차장 정보
        region: 지역 (seoul, gyeonggi, other)
        realtime_info: 실시간 정보 (서울/경기만)
    
    Returns:
        포맷팅된 주차장 정보
    """
    result = {
        "name": parking_data.get("name", parking_data.get("parking_name", "주차장")),
        "address": parking_data.get("address", parking_data.get("addr", "")),
        "total_spots": parking_data.get("total_spots", parking_data.get("capacity", None)),
        "fee": parking_data.get("fee", parking_data.get("rates", "")),
    }
    
    if region in ["seoul", "gyeonggi"] and realtime_info:
        # 실시간 정보가 있는 경우
        result["available_spots"] = realtime_info.get(
            "available_spots",
            realtime_info.get("available", None)
        )
    else:
        # 실시간 정보가 없는 경우
        result["available_spots"] = None
        if region == "other":
            result["notice"] = (
                "해당 지역은 기본 주차장 정보만 제공됩니다. "
                "실시간 정보는 서울/경기 지역에서 이용 가능합니다."
            )
    
    return result


def _get_realtime_info_seoul(
    parking_name: str,
    address: str
) -> Optional[Dict[str, Any]]:
    """서울 주차장 실시간 정보 조회"""
    try:
        seoul_client = SeoulDataClient()
        response = seoul_client.get_realtime_parking_info()
        
        if response.get("status") == "success":
            data = response.get("data", {})
            # 실제 API 응답 구조에 맞게 파싱 필요
            # 여기서는 예시로 구현
            parking_list = data.get("GetParkingInfo", {}).get("row", [])
            
            # 주차장 이름이나 주소로 매칭
            for parking in parking_list:
                if (parking_name in parking.get("PARKING_NAME", "") or
                    address in parking.get("ADDR", "")):
                    return {
                        "available_spots": parking.get("CAPACITY", 0) - parking.get("CUR_PARKING", 0),
                        "total_spots": parking.get("CAPACITY", 0),
                    }
    except ValueError:
        # API 키 없음 등 - 조용히 실패
        pass
    except Exception:
        # 기타 에러 - 조용히 실패
        pass
    
    return None


def _get_realtime_info_gyeonggi(
    parking_name: str,
    address: str
) -> Optional[Dict[str, Any]]:
    """경기 주차장 실시간 정보 조회"""
    try:
        gyeonggi_client = GyeonggiDataClient()
        response = gyeonggi_client.get_realtime_parking_info()
        
        if response.get("status") == "success":
            data = response.get("data", {})
            # 실제 API 응답 구조에 맞게 파싱 필요
            parking_list = data.get("Parking", [1], {}).get("row", [])
            
            # 주차장 이름이나 주소로 매칭
            for parking in parking_list:
                if (parking_name in parking.get("PARKING_NAME", "") or
                    address in parking.get("ADDR", "")):
                    return {
                        "available_spots": parking.get("CAPACITY", 0) - parking.get("CUR_PARKING", 0),
                        "total_spots": parking.get("CAPACITY", 0),
                    }
    except ValueError:
        # API 키 없음 등 - 조용히 실패
        pass
    except Exception:
        # 기타 에러 - 조용히 실패
        pass
    
    return None


def _parse_xml_response(xml_string: str) -> List[Dict[str, Any]]:
    """
    공공데이터포털 XML 응답을 파싱하여 주차장 목록 반환
    
    Args:
        xml_string: XML 응답 문자열
    
    Returns:
        주차장 정보 딕셔너리 리스트
    """
    try:
        root = ET.fromstring(xml_string)
        
        # 공공데이터포털 응답 구조에 따라 파싱
        # 일반적인 구조: response -> body -> items -> item
        items = root.findall(".//item")
        
        parking_list = []
        for item in items:
            parking = {}
            for child in item:
                # XML 태그명을 키로, 텍스트를 값으로
                tag = child.tag.replace("{http://www.data.go.kr/}", "")
                parking[tag] = child.text if child.text else ""
            
            # 필드명 정규화 (다양한 API 응답 형식 대응)
            if parking:
                # 주차장명
                parking["name"] = (
                    parking.get("parkingName") or
                    parking.get("parking_name") or
                    parking.get("PARKING_NAME") or
                    parking.get("name") or
                    ""
                )
                # 주소
                parking["address"] = (
                    parking.get("addr") or
                    parking.get("address") or
                    parking.get("ADDR") or
                    parking.get("addrNew") or
                    ""
                )
                # 총 주차 대수
                parking["total_spots"] = (
                    parking.get("capacity") or
                    parking.get("CAPACITY") or
                    parking.get("totalSpots") or
                    None
                )
                # 요금
                parking["fee"] = (
                    parking.get("rates") or
                    parking.get("RATES") or
                    parking.get("fee") or
                    parking.get("payNm") or
                    ""
                )
                
                parking_list.append(parking)
        
        return parking_list
    except ET.ParseError:
        # XML 파싱 실패
        return []
    except Exception:
        # 기타 에러
        return []


@app.tool()
def search_nearby_parking(
    latitude: float,
    longitude: float,
    radius: float = 1000.0
) -> dict:
    """
    주변 주차장을 검색합니다.
    
    Args:
        latitude: 위도
        longitude: 경도
        radius: 검색 반경 (미터 단위, 기본값: 1000)
    
    Returns:
        주변 주차장 목록
    """
    # 입력값 검증
    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        return {
            "error": "유효하지 않은 위치 정보입니다. 확인 후 다시 시도해주세요.",
            "parkings": []
        }
    
    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        return {
            "error": "유효하지 않은 위치 정보입니다. 확인 후 다시 시도해주세요.",
            "parkings": []
        }
    
    if radius <= 0:
        return {
            "error": "유효하지 않은 위치 정보입니다. 확인 후 다시 시도해주세요.",
            "parkings": []
        }
    
    # 기본 주차장 정보 검색
    try:
        public_client = PublicDataClient()
        response = public_client.search_nearby_parking(
            latitude=latitude,
            longitude=longitude,
            radius=radius
        )
    except ValueError as e:
        # API 키 없음
        if "설정되지 않았습니다" in str(e) or "유효하지 않습니다" in str(e):
            return {
                "error": "주차장 정보 제공 서비스가 준비 중입니다.",
                "parkings": []
            }
        return {
            "error": "주차장 정보를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
            "parkings": []
        }
    except Exception:
        return {
            "error": "주차장 정보를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
            "parkings": []
        }
    
    # 응답 파싱
    if response.get("status") != "success":
        return {
            "error": "주차장 정보를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
            "parkings": []
        }
    
    # XML 응답 파싱
    raw_data = response.get("data", "")
    parking_list = _parse_xml_response(raw_data)
    
    # 결과가 없는 경우
    if not parking_list:
        return {
            "error": "주변에서 주차장을 찾을 수 없습니다. 검색 범위를 넓혀보세요.",
            "parkings": []
        }
    
    # 각 주차장에 대해 실시간 정보 추가
    formatted_parkings = []
    for parking in parking_list:
        address = parking.get("address", parking.get("addr", ""))
        region = _get_region(address)
        
        realtime_info = None
        if region == "seoul":
            realtime_info = _get_realtime_info_seoul(
                parking.get("name", ""),
                address
            )
        elif region == "gyeonggi":
            realtime_info = _get_realtime_info_gyeonggi(
                parking.get("name", ""),
                address
            )
        
        formatted_parking = _format_parking_info(parking, region, realtime_info)
        formatted_parkings.append(formatted_parking)
    
    return {
        "parkings": formatted_parkings,
        "count": len(formatted_parkings)
    }


@app.tool()
def get_parking_info(
    parking_id: str
) -> dict:
    """
    특정 주차장의 상세 정보를 조회합니다.
    
    Args:
        parking_id: 주차장 ID
    
    Returns:
        주차장 상세 정보
    """
    # 입력값 검증
    if not parking_id or not isinstance(parking_id, str) or not parking_id.strip():
        return {
            "error": "유효하지 않은 주차장 정보입니다. 확인 후 다시 시도해주세요."
        }
    
    # 기본 주차장 정보 조회
    try:
        public_client = PublicDataClient()
        # 실제 API에 주차장 ID로 조회하는 엔드포인트가 있다고 가정
        # 여기서는 예시로 구현
        response = public_client.get_parking_list()
    except ValueError as e:
        # API 키 없음
        if "설정되지 않았습니다" in str(e) or "유효하지 않습니다" in str(e):
            return {
                "error": "주차장 정보 제공 서비스가 준비 중입니다."
            }
        return {
            "error": "주차장 정보를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        }
    except Exception:
        return {
            "error": "주차장 정보를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        }
    
    # 응답 파싱
    if response.get("status") != "success":
        return {
            "error": "주차장 정보를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        }
    
    # XML 응답 파싱
    raw_data = response.get("data", "")
    parking_list = _parse_xml_response(raw_data)
    
    # 해당 ID의 주차장 찾기
    parking = None
    for p in parking_list:
        if (p.get("id") == parking_id or 
            p.get("parking_id") == parking_id or
            p.get("parkingId") == parking_id or
            p.get("PARKING_ID") == parking_id):
            parking = p
            break
    
    if not parking:
        return {
            "error": "요청하신 주차장 정보를 찾을 수 없습니다."
        }
    
    # 지역 구분 및 실시간 정보 추가
    address = parking.get("address", parking.get("addr", ""))
    region = _get_region(address)
    
    realtime_info = None
    if region == "seoul":
        realtime_info = _get_realtime_info_seoul(
            parking.get("name", ""),
            address
        )
    elif region == "gyeonggi":
        realtime_info = _get_realtime_info_gyeonggi(
            parking.get("name", ""),
            address
        )
    
    formatted_parking = _format_parking_info(parking, region, realtime_info)
    
    return formatted_parking


if __name__ == "__main__":
    app.run()

