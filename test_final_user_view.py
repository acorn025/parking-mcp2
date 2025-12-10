"""
최종 테스트 - 실제 이용자 응답 형식
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def format_user_response(parkings, region_name):
    """이용자가 받는 응답 형식으로 포맷팅"""
    print(f"\n{'='*80}")
    print(f"{region_name} 지역 주차장 검색 결과")
    print(f"{'='*80}\n")
    
    if not parkings:
        print("주변에서 주차장을 찾을 수 없습니다.")
        return
    
    print(f"총 {len(parkings)}개의 주차장을 찾았습니다.\n")
    
    for i, parking in enumerate(parkings[:5], 1):
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"[주차장 {i}] {parking.get('name', 'N/A')}")
        print(f"   주소: {parking.get('address', 'N/A')}")
        if parking.get('distance', 0) > 0:
            print(f"   거리: {parking.get('distance', 0)}m")
        
        # 실시간 정보 (서울만)
        if parking.get('available_spots') is not None:
            print(f"\n   [실시간 주차 정보]")
            print(f"   - 총 주차 대수: {parking.get('total_spots')}대")
            print(f"   - 주차 가능 대수: {parking.get('available_spots')}대")
            if parking.get('update_time'):
                print(f"   - 업데이트 시간: {parking.get('update_time')}")
        
        # 총 주차 대수 (경기)
        elif parking.get('total_spots'):
            print(f"\n   [주차장 정보]")
            print(f"   - 총 주차 대수: {parking.get('total_spots')}대")
        
        # 운영 시간
        if parking.get('operating_info'):
            op = parking.get('operating_info')
            print(f"\n   [운영 시간]")
            if op.get('operating_type'):
                print(f"   - 운영 구분: {op.get('operating_type')}")
            if op.get('weekday_start'):
                print(f"   - 평일: {op.get('weekday_start')} ~ {op.get('weekday_end')}")
            if op.get('weekend_start'):
                print(f"   - 주말: {op.get('weekend_start')} ~ {op.get('weekend_end')}")
            elif op.get('saturday_start'):
                print(f"   - 토요일: {op.get('saturday_start')} ~ {op.get('saturday_end')}")
            if op.get('holiday_start'):
                print(f"   - 공휴일: {op.get('holiday_start')} ~ {op.get('holiday_end')}")
        
        # 요금 정보
        if parking.get('fee_info'):
            fee = parking.get('fee_info')
            print(f"\n   [요금 정보]")
            if fee.get('is_paid'):
                print(f"   - 유료 여부: {fee.get('is_paid')}")
            if fee.get('basic_fee') or fee.get('basic_time'):
                basic_fee = fee.get('basic_fee', 0) or fee.get('basic_fee', 0)
                basic_time = fee.get('basic_hours', 0) or fee.get('basic_time', 0)
                if basic_fee or basic_time:
                    print(f"   - 기본 요금: {basic_fee}원 / {basic_time}분")
            if fee.get('additional_fee') or fee.get('additional_time'):
                add_fee = fee.get('additional_fee', 0) or fee.get('additional_fee', 0)
                add_time = fee.get('additional_hours', 0) or fee.get('additional_time', 0)
                if add_fee or add_time:
                    print(f"   - 추가 요금: {add_fee}원 / {add_time}분")
            if fee.get('daily_max_fee'):
                print(f"   - 일일 최대 요금: {fee.get('daily_max_fee')}원")
            if fee.get('payment_method'):
                print(f"   - 결제 방법: {fee.get('payment_method')}")
        
        # 안내 메시지 (기타 지역)
        if parking.get('notice'):
            print(f"\n   [안내] {parking.get('notice')}")
        
        print()

def test_seoul():
    """서울 지역 테스트"""
    print("\n" + "="*80)
    print("테스트 1: 서울 지역")
    print("="*80)
    print("\n[검색 위치] 서울시 중구 세종대로 110")
    
    try:
        from api_clients import KakaoLocalClient
        from src.server import (
            _parse_kakao_parking_response,
            _get_region,
            _get_realtime_info_seoul,
            _format_parking_info
        )
        
        kakao_client = KakaoLocalClient()
        coord_response = kakao_client.address_to_coordinates("서울시 중구 세종대로 110")
        
        lat = float(coord_response.get("data", {}).get("documents", [])[0].get('y'))
        lng = float(coord_response.get("data", {}).get("documents", [])[0].get('x'))
        
        parking_response = kakao_client.search_parking_nearby(lat, lng, 1000, 15)
        parking_data = parking_response.get("data", {})
        parking_list = _parse_kakao_parking_response(parking_data)
        
        formatted_parkings = []
        for parking in parking_list:
            address = parking.get("address", "") or parking.get("road_address", "")
            region = _get_region(address)
            
            if region == "seoul":
                realtime_info = _get_realtime_info_seoul(parking.get("name", ""), address)
                standard_parking = {
                    "name": parking.get("name", ""),
                    "address": address,
                    "total_spots": None,
                    "fee": parking.get("category", ""),
                    "distance": parking.get("distance", 0),
                }
                formatted = _format_parking_info(standard_parking, "seoul", realtime_info)
                formatted_parkings.append(formatted)
        
        format_user_response(formatted_parkings, "서울")
        
    except Exception as e:
        print(f"[오류] {str(e)}")

def test_gyeonggi():
    """경기 지역 테스트"""
    print("\n" + "="*80)
    print("테스트 2: 경기 지역")
    print("="*80)
    print("\n[검색 위치] 경기도 수원시 팔달구 정조로 825")
    
    try:
        from api_clients import KakaoLocalClient
        from src.server import (
            _parse_kakao_parking_response,
            _get_region,
            _get_realtime_info_gyeonggi,
            _format_parking_info
        )
        
        kakao_client = KakaoLocalClient()
        coord_response = kakao_client.address_to_coordinates("경기도 수원시 팔달구 정조로 825")
        
        lat = float(coord_response.get("data", {}).get("documents", [])[0].get('y'))
        lng = float(coord_response.get("data", {}).get("documents", [])[0].get('x'))
        
        parking_response = kakao_client.search_parking_nearby(lat, lng, 1000, 15)
        parking_data = parking_response.get("data", {})
        parking_list = _parse_kakao_parking_response(parking_data)
        
        formatted_parkings = []
        for parking in parking_list:
            address = parking.get("address", "") or parking.get("road_address", "")
            region = _get_region(address)
            
            if region == "gyeonggi":
                realtime_info = _get_realtime_info_gyeonggi(parking.get("name", ""), address)
                standard_parking = {
                    "name": parking.get("name", ""),
                    "address": address,
                    "total_spots": None,
                    "fee": parking.get("category", ""),
                    "distance": parking.get("distance", 0),
                }
                formatted = _format_parking_info(standard_parking, "gyeonggi", realtime_info)
                formatted_parkings.append(formatted)
        
        format_user_response(formatted_parkings, "경기")
        
    except Exception as e:
        print(f"[오류] {str(e)}")

def test_other():
    """기타 지역 테스트"""
    print("\n" + "="*80)
    print("테스트 3: 기타 지역")
    print("="*80)
    print("\n[검색 위치] 부산 해운대구 해운대해변로 264")
    
    try:
        from api_clients import KakaoLocalClient
        from src.server import (
            _parse_kakao_parking_response,
            _get_region,
            _format_parking_info
        )
        
        kakao_client = KakaoLocalClient()
        coord_response = kakao_client.address_to_coordinates("부산 해운대구 해운대해변로 264")
        
        lat = float(coord_response.get("data", {}).get("documents", [])[0].get('y'))
        lng = float(coord_response.get("data", {}).get("documents", [])[0].get('x'))
        
        parking_response = kakao_client.search_parking_nearby(lat, lng, 1000, 15)
        parking_data = parking_response.get("data", {})
        parking_list = _parse_kakao_parking_response(parking_data)
        
        formatted_parkings = []
        for parking in parking_list:
            address = parking.get("address", "") or parking.get("road_address", "")
            region = _get_region(address)
            
            if region == "other":
                standard_parking = {
                    "name": parking.get("name", ""),
                    "address": address,
                    "total_spots": None,
                    "fee": parking.get("category", ""),
                    "distance": parking.get("distance", 0),
                }
                formatted = _format_parking_info(standard_parking, "other", None)
                formatted_parkings.append(formatted)
        
        format_user_response(formatted_parkings, "기타")
        
    except Exception as e:
        print(f"[오류] {str(e)}")

if __name__ == "__main__":
    test_seoul()
    test_gyeonggi()
    test_other()
    
    print("\n" + "="*80)
    print("최종 테스트 완료")
    print("="*80)
    print("\n[결과 요약]")
    print("  서울: 실시간 정보 + 운영시간 + 요금 정보 제공")
    print("  경기: 총 주차 대수 + 운영시간 + 요금 정보 제공")
    print("  기타: 기본 정보 + 안내 메시지 제공")
    print("="*80)

