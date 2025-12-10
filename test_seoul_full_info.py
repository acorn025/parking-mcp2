"""
서울 API 전체 정보 테스트 (운영정보 + 요금정보 포함)
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_seoul_full_info():
    """서울 API 전체 정보 테스트"""
    print("=" * 70)
    print("서울 API 전체 정보 테스트 (운영정보 + 요금정보)")
    print("=" * 70)
    
    test_address = "서울시 중구 세종대로 110"  # 서울시청
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
        
        coord_data = coord_response.get("data", {})
        coord_docs = coord_data.get("documents", [])
        lat = float(coord_docs[0].get('y'))
        lng = float(coord_docs[0].get('x'))
        
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
        
        # 서울 지역 주차장에 실시간 정보 추가
        for i, parking in enumerate(parking_list[:5], 1):
            address = parking.get("address", "") or parking.get("road_address", "")
            region = _get_region(address)
            
            if region == "seoul":
                print(f"\n--- 주차장 {i}: {parking.get('name')} ---")
                
                realtime_info = _get_realtime_info_seoul(
                    parking.get("name", ""),
                    address
                )
                
                if realtime_info:
                    print(f"[실시간 정보]")
                    print(f"  총 주차 대수: {realtime_info.get('total_spots')}")
                    print(f"  현재 주차 대수: {realtime_info.get('current_spots')}")
                    print(f"  주차 가능 대수: {realtime_info.get('available_spots')}")
                    print(f"  업데이트 시간: {realtime_info.get('update_time')}")
                    
                    operating_info = realtime_info.get("operating_info", {})
                    if operating_info:
                        print(f"\n[운영 정보]")
                        print(f"  운영 구분: {operating_info.get('operating_type')}")
                        print(f"  운영 상태: {operating_info.get('status')}")
                        print(f"  평일 운영: {operating_info.get('weekday_start')} ~ {operating_info.get('weekday_end')}")
                        print(f"  주말 운영: {operating_info.get('weekend_start')} ~ {operating_info.get('weekend_end')}")
                        print(f"  공휴일 운영: {operating_info.get('holiday_start')} ~ {operating_info.get('holiday_end')}")
                    
                    fee_info = realtime_info.get("fee_info", {})
                    if fee_info:
                        print(f"\n[요금 정보]")
                        print(f"  유료 여부: {fee_info.get('is_paid')}")
                        print(f"  야간 유료: {fee_info.get('night_paid')}")
                        print(f"  기본 요금: {fee_info.get('basic_fee')}원 / {fee_info.get('basic_hours')}분")
                        print(f"  추가 요금: {fee_info.get('additional_fee')}원 / {fee_info.get('additional_hours')}분")
                        print(f"  일일 최대 요금: {fee_info.get('daily_max_fee')}원")
                        print(f"  기간 요금: {fee_info.get('period_fee')}원")
                else:
                    print(f"[정보] 실시간 정보를 찾을 수 없습니다.")
        
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"\n[X] 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_seoul_full_info()

