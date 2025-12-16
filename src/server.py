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
        # 서울/경기 지역 정보 추가
        result["available_spots"] = realtime_info.get(
            "available_spots",
            realtime_info.get("available", None)
        )
        result["total_spots"] = realtime_info.get("total_spots") or result.get("total_spots")
        
        # 운영정보와 요금 정보 추가 (서울/경기 모두)
        if realtime_info.get("operating_info"):
            result["operating_info"] = realtime_info.get("operating_info")
        if realtime_info.get("fee_info"):
            result["fee_info"] = realtime_info.get("fee_info")
        
        # 서울은 실시간 정보, 경기는 요금/운영시간만
        if region == "seoul":
            result["update_time"] = realtime_info.get("update_time")
    else:
        # 실시간 정보가 없는 경우
        result["available_spots"] = None
        # notice는 각 주차장에 추가하지 않고, 최상단에 한 번만 표시
    
    return result


def _get_realtime_info_seoul(
    parking_name: str,
    address: str
) -> Optional[Dict[str, Any]]:
    """서울 주차장 실시간 정보 조회"""
    try:
        seoul_client = SeoulDataClient()
        # 서울 API는 최대 1000개까지 한 번에 조회 가능
        response = seoul_client.get_realtime_parking_info(
            start_index=1,
            end_index=1000
        )
        
        if response.get("status") == "success":
            data = response.get("data", {})
            parking_info = data.get("GetParkingInfo", {})
            parking_list = parking_info.get("row", [])
            
            # 주차장 이름이나 주소로 매칭 (부분 일치)
            for parking in parking_list:
                parking_nm = parking.get("PKLT_NM", "")
                parking_addr = parking.get("ADDR", "")
                
                # 이름이나 주소가 부분적으로 일치하는지 확인
                name_match = parking_name and (parking_name in parking_nm or parking_nm in parking_name)
                addr_match = address and (address in parking_addr or parking_addr in address)
                
                if name_match or addr_match:
                    total_spots = parking.get("TPKCT", 0)
                    current_spots = parking.get("NOW_PRK_VHCL_CNT", 0)
                    available_spots = max(0, float(total_spots) - float(current_spots))
                    
                    # 운영 정보
                    operating_info = {
                        "operating_type": parking.get("OPER_SE_NM", ""),
                        "status": parking.get("PRK_STTS_NM", ""),
                        "weekday_start": parking.get("WD_OPER_BGNG_TM", ""),
                        "weekday_end": parking.get("WD_OPER_END_TM", ""),
                        "weekend_start": parking.get("WE_OPER_BGNG_TM", ""),
                        "weekend_end": parking.get("WE_OPER_END_TM", ""),
                        "holiday_start": parking.get("LHLDY_OPER_BGNG_TM", ""),
                        "holiday_end": parking.get("LHLDY_OPER_END_TM", ""),
                    }
                    
                    # 요금 정보
                    fee_info = {
                        "is_paid": parking.get("PAY_YN_NM", ""),
                        "night_paid": parking.get("NGHT_PAY_YN_NM", ""),
                        "basic_fee": parking.get("BSC_PRK_CRG", 0),
                        "basic_hours": parking.get("BSC_PRK_HR", 0),
                        "additional_fee": parking.get("ADD_PRK_CRG", 0),
                        "additional_hours": parking.get("ADD_PRK_HR", 0),
                        "daily_max_fee": parking.get("DAY_MAX_CRG", 0),
                        "period_fee": parking.get("PRD_AMT", 0),
                    }
                    
                    return {
                        "available_spots": int(available_spots),
                        "total_spots": int(total_spots),
                        "current_spots": int(current_spots),
                        "update_time": parking.get("NOW_PRK_VHCL_UPDT_TM", ""),
                        "operating_info": operating_info,
                        "fee_info": fee_info,
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
    """경기 주차장 정보 조회 (요금 및 운영시간 포함)"""
    try:
        gyeonggi_client = GyeonggiDataClient()
        response = gyeonggi_client.get_realtime_parking_info(
            page=1,
            size=100
        )
        
        if response.get("status") == "success":
            data = response.get("data", {})
            parking_place = data.get("ParkingPlace", [])
            
            # 경기 API 응답 구조: ParkingPlace는 배열이고 [1]에 row가 있음
            if isinstance(parking_place, list) and len(parking_place) > 1:
                parking_list = parking_place[1].get("row", [])
            elif isinstance(parking_place, dict):
                parking_list = parking_place.get("row", [])
            else:
                parking_list = []
            
            # 주차장 이름이나 주소로 매칭
            for parking in parking_list:
                parking_nm = parking.get("PARKPLC_NM", "") or parking.get("parkplc_nm", "")
                parking_addr = (
                    parking.get("LOCPLC_ROADNM_ADDR", "") or 
                    parking.get("LOCPLC_LOTNO_ADDR", "") or
                    parking.get("locplc_roadnm_addr", "") or
                    parking.get("locplc_lotno_addr", "")
                )
                
                # 이름이나 주소가 부분적으로 일치하는지 확인
                name_match = parking_name and (parking_name in parking_nm or parking_nm in parking_name)
                addr_match = address and (address in parking_addr or parking_addr in address)
                
                if name_match or addr_match:
                    total_spots = parking.get("PARKNG_COMPRT_PLANE_CNT", 0) or parking.get("parkng_comprt_plane_cnt", 0)
                    
                    # 운영 정보
                    operating_info = {
                        "weekday_start": parking.get("WKDAY_OPERT_BEGIN_TM", ""),
                        "weekday_end": parking.get("WKDAY_OPERT_END_TM", ""),
                        "saturday_start": parking.get("SAT_OPERT_BEGIN_TM", ""),
                        "saturday_end": parking.get("SAT_OPERT_END_TM", ""),
                        "holiday_start": parking.get("HOLIDAY_OPERT_BEGIN_TM", ""),
                        "holiday_end": parking.get("HOLIDAY_OPERT_END_TM", ""),
                    }
                    
                    # 요금 정보
                    fee_info = {
                        "is_paid": parking.get("CHRG_INFO", ""),  # 유료/무료
                        "basic_time": parking.get("PARKNG_BASIS_TM", 0),  # 기본 시간 (분)
                        "basic_fee": parking.get("PARKNG_BASIS_USE_CHRG", 0),  # 기본 요금
                        "additional_time": parking.get("ADD_UNIT_TM", 0),  # 추가 시간 (분)
                        "additional_fee": parking.get("ADD_UNIT_TM2_WITHIN_USE_CHRG", 0),  # 추가 요금
                        "payment_method": parking.get("SETTLE_METH", ""),  # 결제 방법
                    }
                    
                    return {
                        "total_spots": int(total_spots) if total_spots else None,
                        "available_spots": None,  # 경기 API에는 실시간 주차 대수 정보가 없음
                        "operating_info": operating_info,
                        "fee_info": fee_info,
                    }
    except ValueError:
        # API 키 없음 등 - 조용히 실패
        pass
    except Exception:
        # 기타 에러 - 조용히 실패
        pass
    
    return None


def _parse_kakao_parking_response(kakao_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    카카오 API 응답을 파싱하여 주차장 목록 반환
    
    Args:
        kakao_data: 카카오 API 응답 데이터
    
    Returns:
        주차장 정보 딕셔너리 리스트
    """
    parking_list = []
    documents = kakao_data.get("documents", [])
    
    for doc in documents:
        parking = {
            "name": doc.get("place_name", ""),
            "address": doc.get("address_name", ""),
            "road_address": doc.get("road_address_name", ""),
            "distance": doc.get("distance", 0),
            "phone": doc.get("phone", ""),
            "category": doc.get("category_name", ""),
            "latitude": doc.get("y"),
            "longitude": doc.get("x"),
            "place_url": doc.get("place_url", ""),
        }
        parking_list.append(parking)
    
    return parking_list


def _address_to_coordinates(address: str) -> Tuple[Optional[float], Optional[float]]:
    """
    주소를 좌표로 변환
    
    Args:
        address: 검색할 주소
    
    Returns:
        (위도, 경도) 튜플, 실패 시 (None, None)
    """
    try:
        kakao_client = KakaoLocalClient()
        response = kakao_client.address_to_coordinates(address)
        
        if response.get("status") == "success":
            data = response.get("data", {})
            documents = data.get("documents", [])
            
            if documents:
                first_result = documents[0]
                latitude = float(first_result.get("y", 0))
                longitude = float(first_result.get("x", 0))
                return latitude, longitude
    except Exception:
        pass
    
    return None, None


@app.tool()
def search_nearby_parking(
    address: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    radius: float = 1000.0
) -> dict:
    """
    주변 주차장을 검색합니다.
    
    주소 또는 좌표(위도, 경도) 중 하나를 제공해야 합니다.
    주소가 제공되면 자동으로 좌표로 변환합니다.
    
    Args:
        address: 검색할 주소 (예: "서울시 중구 세종대로 110")
        latitude: 위도 (주소가 없을 때 필수)
        longitude: 경도 (주소가 없을 때 필수)
        radius: 검색 반경 (미터 단위, 기본값: 1000)
    
    Returns:
        주변 주차장 목록
    """
    # 주소 또는 좌표 중 하나는 필수
    if not address and (latitude is None or longitude is None):
        return {
            "success": False,
            "error": "주소 또는 좌표(위도, 경도)를 제공해주세요.",
            "parkings": [],
            "count": 0
        }
    
    # 주소가 제공되면 좌표로 변환
    if address:
        lat, lng = _address_to_coordinates(address)
        if lat is None or lng is None:
            return {
                "success": False,
                "error": f"주소 '{address}'를 찾을 수 없습니다. 주소를 확인해주세요.",
                "parkings": [],
                "count": 0
            }
        latitude = lat
        longitude = lng
    else:
        latitude = float(latitude)
        longitude = float(longitude)
    
    # 입력값 검증
    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        return {
            "success": False,
            "error": "유효하지 않은 위치 정보입니다. 확인 후 다시 시도해주세요.",
            "parkings": [],
            "count": 0
        }
    
    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        return {
            "success": False,
            "error": "유효하지 않은 위치 정보입니다. 확인 후 다시 시도해주세요.",
            "parkings": [],
            "count": 0
        }
    
    if radius <= 0:
        return {
            "success": False,
            "error": "검색 반경은 0보다 커야 합니다.",
            "parkings": [],
            "count": 0
        }
    
    # 카카오 API로 주차장 검색
    try:
        kakao_client = KakaoLocalClient()
        response = kakao_client.search_parking_nearby(
            latitude=latitude,
            longitude=longitude,
            radius=int(radius),
            size=15
        )
    except ValueError as e:
        # API 키 없음
        if "설정되지 않았습니다" in str(e) or "유효하지 않습니다" in str(e):
            return {
                "success": False,
                "error": "주차장 정보 제공 서비스가 준비 중입니다.",
                "parkings": [],
                "count": 0
            }
        return {
            "success": False,
            "error": "주차장 정보를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
            "parkings": [],
            "count": 0
        }
    except Exception:
        return {
            "success": False,
            "error": "주차장 정보를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
            "parkings": [],
            "count": 0
        }
    
    # 응답 파싱
    if response.get("status") != "success":
        return {
            "success": False,
            "error": "주차장 정보를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
            "parkings": [],
            "count": 0
        }
    
    # 카카오 API 응답 파싱
    kakao_data = response.get("data", {})
    parking_list = _parse_kakao_parking_response(kakao_data)
    
    # 결과가 없는 경우
    if not parking_list:
        return {
            "success": True,
            "message": "주변에서 주차장을 찾을 수 없습니다. 검색 범위를 넓혀보세요.",
            "parkings": [],
            "count": 0
        }
    
    # 각 주차장에 대해 실시간 정보 추가
    formatted_parkings = []
    has_other_region = False  # 기타 지역 주차장이 있는지 확인
    
    for parking in parking_list:
        address = parking.get("address", "") or parking.get("road_address", "")
        region = _get_region(address)
        
        # 기타 지역이 있는지 확인
        if region == "other":
            has_other_region = True
        
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
        
        # 카카오 API 데이터를 표준 형식으로 변환
        standard_parking = {
            "name": parking.get("name", ""),
            "address": address,
            "total_spots": None,  # 카카오 API에는 총 주차 대수 정보가 없음
            "fee": parking.get("category", ""),
            "distance": parking.get("distance", 0),
            "phone": parking.get("phone", ""),
        }
        
        formatted_parking = _format_parking_info(standard_parking, region, realtime_info)
        formatted_parkings.append(formatted_parking)
    
    # 응답 구성
    response = {
        "success": True,
        "parkings": formatted_parkings,
        "count": len(formatted_parkings)
    }
    
    # 기타 지역이 있는 경우 최상단에 안내 메시지 추가
    if has_other_region:
        response["notice"] = (
            "해당 지역은 기본 주차장 정보만 제공됩니다. "
            "실시간 정보는 서울 지역에서, 요금 및 운영시간 정보는 서울/경기 지역에서 이용 가능합니다."
        )
    
    return response


@app.tool()
def get_parking_info(
    parking_name: str,
    address: Optional[str] = None
) -> dict:
    """
    특정 주차장의 상세 정보를 조회합니다.
    
    Args:
        parking_name: 주차장 이름 (예: "시청 공영주차장")
        address: 주차장 주소 (선택사항, 정확한 검색을 위해 권장)
    
    Returns:
        주차장 상세 정보
    """
    # 입력값 검증
    if not parking_name or not isinstance(parking_name, str) or not parking_name.strip():
        return {
            "success": False,
            "error": "주차장 이름을 입력해주세요."
        }
    
    # 카카오 API로 주차장 검색
    try:
        kakao_client = KakaoLocalClient()
        # 주소가 제공되면 주소로 검색, 없으면 이름으로 검색
        query = address if address else parking_name
        response = kakao_client.search_place(
            query=query,
            category_group_code="PK6",  # 주차장 카테고리
            size=10
        )
    except ValueError as e:
        # API 키 없음
        if "설정되지 않았습니다" in str(e) or "유효하지 않습니다" in str(e):
            return {
                "success": False,
                "error": "주차장 정보 제공 서비스가 준비 중입니다."
            }
        return {
            "success": False,
            "error": "주차장 정보를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        }
    except Exception:
        return {
            "success": False,
            "error": "주차장 정보를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        }
    
    # 응답 파싱
    if response.get("status") != "success":
        return {
            "success": False,
            "error": "주차장 정보를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        }
    
    # 카카오 API 응답 파싱
    kakao_data = response.get("data", {})
    parking_list = _parse_kakao_parking_response(kakao_data)
    
    # 주차장 이름과 주소로 매칭
    parking = None
    for p in parking_list:
        name_match = parking_name in p.get("name", "") or p.get("name", "") in parking_name
        addr_match = False
        if address:
            addr_match = (
                address in p.get("address", "") or 
                address in p.get("road_address", "") or
                p.get("address", "") in address or
                p.get("road_address", "") in address
            )
        
        if name_match or (address and addr_match):
            parking = p
            break
    
    # 정확히 일치하는 것이 없으면 첫 번째 결과 사용
    if not parking and parking_list:
        parking = parking_list[0]
    
    if not parking:
        return {
            "success": False,
            "error": f"'{parking_name}' 주차장 정보를 찾을 수 없습니다."
        }
    
    # 지역 구분 및 실시간 정보 추가
    address = parking.get("address", "") or parking.get("road_address", "")
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
    
    # 카카오 API 데이터를 표준 형식으로 변환
    standard_parking = {
        "name": parking.get("name", ""),
        "address": address,
        "total_spots": None,
        "fee": parking.get("category", ""),
        "distance": parking.get("distance", 0),
        "phone": parking.get("phone", ""),
    }
    
    formatted_parking = _format_parking_info(standard_parking, region, realtime_info)
    formatted_parking["success"] = True
    
    return formatted_parking


def main():
    """MCP 서버 실행 함수 (entry point용)"""
    app.run()


if __name__ == "__main__":
    main()

