"""
서울 API 통합 테스트 - 잠실 롯데타워 근처
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_integration():
    """서울 API 통합 테스트"""
    print("=" * 70)
    print("서울 API 통합 테스트 - 잠실 롯데타워 근처")
    print("=" * 70)
    
    # 1. 카카오로 주차장 검색
    print("\n[1단계] 카카오 API로 주차장 검색")
    print("-" * 70)
    
    try:
        from api_clients import KakaoLocalClient
        kakao_client = KakaoLocalClient()
        
        # 롯데월드타워 좌표
        lat = 37.5137129859207
        lng = 127.104301829165
        
        parking_response = kakao_client.search_parking_nearby(
            latitude=lat,
            longitude=lng,
            radius=1000,
            size=10
        )
        
        if parking_response.get("status") != "success":
            print(f"[X] 카카오 API 실패: {parking_response}")
            return
        
        parking_data = parking_response.get("data", {})
        parking_docs = parking_data.get("documents", [])
        
        print(f"[OK] 카카오 주차장 {len(parking_docs)}개 발견")
        
        # 2. 서버의 파싱 함수 사용
        from src.server import _parse_kakao_parking_response, _get_region, _get_realtime_info_seoul, _format_parking_info
        
        parking_list = _parse_kakao_parking_response(parking_data)
        
        print(f"\n[2단계] 서울 실시간 정보 추가")
        print("-" * 70)
        
        # 서울 지역 주차장만 필터링
        seoul_parkings = [p for p in parking_list if _get_region(p.get("address", "") or p.get("road_address", "")) == "seoul"]
        
        print(f"서울 지역 주차장: {len(seoul_parkings)}개")
        
        # 각 주차장에 실시간 정보 추가
        for i, parking in enumerate(seoul_parkings[:5], 1):  # 상위 5개만
            print(f"\n--- 주차장 {i}: {parking.get('name')} ---")
            address = parking.get("address", "") or parking.get("road_address", "")
            print(f"주소: {address}")
            
            # 실시간 정보 조회
            realtime_info = _get_realtime_info_seoul(
                parking.get("name", ""),
                address
            )
            
            if realtime_info:
                print(f"[OK] 실시간 정보 조회 성공!")
                print(f"  총 주차 대수: {realtime_info.get('total_spots')}")
                print(f"  현재 주차 대수: {realtime_info.get('current_spots')}")
                print(f"  주차 가능 대수: {realtime_info.get('available_spots')}")
                print(f"  업데이트 시간: {realtime_info.get('update_time')}")
            else:
                print(f"[INFO] 실시간 정보를 찾을 수 없습니다.")
            
            # 포맷팅
            standard_parking = {
                "name": parking.get("name", ""),
                "address": address,
                "total_spots": None,
                "fee": parking.get("category", ""),
                "distance": parking.get("distance", 0),
                "phone": parking.get("phone", ""),
            }
            
            formatted = _format_parking_info(standard_parking, "seoul", realtime_info)
            print(f"포맷팅 결과:")
            print(f"  주차 가능: {formatted.get('available_spots')}")
            print(f"  총 대수: {formatted.get('total_spots')}")
        
        print(f"\n[테스트 완료]")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n[X] 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_integration()

