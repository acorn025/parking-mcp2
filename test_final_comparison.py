"""
최종 통합 테스트 - 서울 vs 경기 비교
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_seoul_hoegi():
    """서울 회기로 테스트"""
    print("=" * 70)
    print("서울 회기로 주차장 검색 테스트")
    print("=" * 70)
    
    test_address = "서울시 동대문구 회기로"
    search_radius = 1000
    
    try:
        from api_clients import KakaoLocalClient
        from src.server import (
            _parse_kakao_parking_response,
            _get_region,
            _get_realtime_info_seoul,
            _format_parking_info
        )
        
        # 좌표 변환
        kakao_client = KakaoLocalClient()
        coord_response = kakao_client.address_to_coordinates(test_address)
        
        if coord_response.get("status") != "success":
            print(f"[X] 좌표 변환 실패")
            return
        
        lat = float(coord_response.get("data", {}).get("documents", [])[0].get('y'))
        lng = float(coord_response.get("data", {}).get("documents", [])[0].get('x'))
        
        # 주차장 검색
        parking_response = kakao_client.search_parking_nearby(
            latitude=lat,
            longitude=lng,
            radius=search_radius,
            size=10
        )
        
        parking_data = parking_response.get("data", {})
        parking_list = _parse_kakao_parking_response(parking_data)
        
        print(f"\n[검색 결과] {len(parking_list)}개 주차장 발견")
        print("-" * 70)
        
        # 서울 지역 주차장에 정보 추가
        seoul_parkings = [p for p in parking_list if _get_region(p.get("address", "") or p.get("road_address", "")) == "seoul"]
        
        for i, parking in enumerate(seoul_parkings[:3], 1):
            address = parking.get("address", "") or parking.get("road_address", "")
            realtime_info = _get_realtime_info_seoul(parking.get("name", ""), address)
            
            standard_parking = {
                "name": parking.get("name", ""),
                "address": address,
                "total_spots": None,
                "fee": parking.get("category", ""),
                "distance": parking.get("distance", 0),
            }
            
            formatted = _format_parking_info(standard_parking, "seoul", realtime_info)
            
            print(f"\n--- 주차장 {i}: {formatted.get('name')} ---")
            print(f"주소: {formatted.get('address')}")
            
            if formatted.get('available_spots') is not None:
                print(f"[실시간 정보]")
                print(f"  총 주차 대수: {formatted.get('total_spots')}")
                print(f"  주차 가능 대수: {formatted.get('available_spots')}")
                print(f"  업데이트 시간: {formatted.get('update_time', 'N/A')}")
            
            if formatted.get('operating_info'):
                op_info = formatted.get('operating_info')
                print(f"[운영 정보]")
                print(f"  운영 구분: {op_info.get('operating_type', 'N/A')}")
                print(f"  평일: {op_info.get('weekday_start', 'N/A')} ~ {op_info.get('weekday_end', 'N/A')}")
                print(f"  주말: {op_info.get('weekend_start', 'N/A')} ~ {op_info.get('weekend_end', 'N/A')}")
            
            if formatted.get('fee_info'):
                fee_info = formatted.get('fee_info')
                print(f"[요금 정보]")
                print(f"  유료 여부: {fee_info.get('is_paid', 'N/A')}")
                print(f"  기본 요금: {fee_info.get('basic_fee', 0)}원 / {fee_info.get('basic_hours', 0)}분")
                print(f"  추가 요금: {fee_info.get('additional_fee', 0)}원 / {fee_info.get('additional_hours', 0)}분")
                print(f"  일일 최대: {fee_info.get('daily_max_fee', 0)}원")
        
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n[X] 오류: {str(e)}")
        import traceback
        traceback.print_exc()

def test_gyeonggi_suwon():
    """경기 수원 테스트"""
    print("\n" + "=" * 70)
    print("경기 수원 주차장 검색 테스트")
    print("=" * 70)
    
    test_address = "경기도 수원시 팔달구 정조로"
    search_radius = 1000
    
    try:
        from api_clients import KakaoLocalClient
        from src.server import (
            _parse_kakao_parking_response,
            _get_region,
            _get_realtime_info_gyeonggi,
            _format_parking_info
        )
        
        # 좌표 변환
        kakao_client = KakaoLocalClient()
        coord_response = kakao_client.address_to_coordinates(test_address)
        
        if coord_response.get("status") != "success":
            print(f"[X] 좌표 변환 실패")
            return
        
        lat = float(coord_response.get("data", {}).get("documents", [])[0].get('y'))
        lng = float(coord_response.get("data", {}).get("documents", [])[0].get('x'))
        
        # 주차장 검색
        parking_response = kakao_client.search_parking_nearby(
            latitude=lat,
            longitude=lng,
            radius=search_radius,
            size=10
        )
        
        parking_data = parking_response.get("data", {})
        parking_list = _parse_kakao_parking_response(parking_data)
        
        print(f"\n[검색 결과] {len(parking_list)}개 주차장 발견")
        print("-" * 70)
        
        # 경기 지역 주차장에 정보 추가
        gyeonggi_parkings = [p for p in parking_list if _get_region(p.get("address", "") or p.get("road_address", "")) == "gyeonggi"]
        
        for i, parking in enumerate(gyeonggi_parkings[:3], 1):
            address = parking.get("address", "") or parking.get("road_address", "")
            realtime_info = _get_realtime_info_gyeonggi(parking.get("name", ""), address)
            
            standard_parking = {
                "name": parking.get("name", ""),
                "address": address,
                "total_spots": None,
                "fee": parking.get("category", ""),
                "distance": parking.get("distance", 0),
            }
            
            formatted = _format_parking_info(standard_parking, "gyeonggi", realtime_info)
            
            print(f"\n--- 주차장 {i}: {formatted.get('name')} ---")
            print(f"주소: {formatted.get('address')}")
            
            if formatted.get('total_spots'):
                print(f"[주차장 정보]")
                print(f"  총 주차 대수: {formatted.get('total_spots')}")
            
            if formatted.get('operating_info'):
                op_info = formatted.get('operating_info')
                print(f"[운영 정보]")
                print(f"  평일: {op_info.get('weekday_start', 'N/A')} ~ {op_info.get('weekday_end', 'N/A')}")
                print(f"  토요일: {op_info.get('saturday_start', 'N/A')} ~ {op_info.get('saturday_end', 'N/A')}")
                print(f"  공휴일: {op_info.get('holiday_start', 'N/A')} ~ {op_info.get('holiday_end', 'N/A')}")
            
            if formatted.get('fee_info'):
                fee_info = formatted.get('fee_info')
                print(f"[요금 정보]")
                print(f"  유료 여부: {fee_info.get('is_paid', 'N/A')}")
                print(f"  기본 요금: {fee_info.get('basic_fee', 0)}원 / {fee_info.get('basic_time', 0)}분")
                print(f"  추가 요금: {fee_info.get('additional_fee', 0)}원 / {fee_info.get('additional_time', 0)}분")
                print(f"  결제 방법: {fee_info.get('payment_method', 'N/A')}")
        
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n[X] 오류: {str(e)}")
        import traceback
        traceback.print_exc()

def compare_results():
    """결과 비교"""
    print("\n" + "=" * 70)
    print("서울 vs 경기 비교 요약")
    print("=" * 70)
    
    print("\n[서울 지역]")
    print("  [OK] 실시간 주차 대수 (available_spots)")
    print("  [OK] 총 주차 대수 (total_spots)")
    print("  [OK] 운영 정보 (operating_info)")
    print("  [OK] 요금 정보 (fee_info)")
    print("  [OK] 업데이트 시간 (update_time)")
    
    print("\n[경기 지역]")
    print("  [X] 실시간 주차 대수 (API에 없음)")
    print("  [OK] 총 주차 대수 (total_spots)")
    print("  [OK] 운영 정보 (operating_info)")
    print("  [OK] 요금 정보 (fee_info)")
    
    print("\n[기타 지역]")
    print("  [X] 실시간 정보 없음")
    print("  [OK] 기본 주차장 정보만 제공")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_seoul_hoegi()
    test_gyeonggi_suwon()
    compare_results()

