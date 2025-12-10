"""
서울 회기역 근처 주차장 검색 통합 테스트
카카오 API + 서울 실시간 정보
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_hoegi_parking():
    """서울 회기역 근처 주차장 검색 테스트"""
    print("=" * 70)
    print("서울 회기역 근처 주차장 검색 통합 테스트")
    print("=" * 70)
    
    test_address = "서울시 동대문구 회기로"
    search_radius = 1000  # 1km
    
    print(f"\n[1단계] 주소 -> 좌표 변환")
    print(f"주소: {test_address}")
    print("-" * 70)
    
    try:
        from api_clients import KakaoLocalClient
        from src.server import (
            _parse_kakao_parking_response,
            _get_region,
            _get_realtime_info_seoul,
            _format_parking_info
        )
        
        # 주소를 좌표로 변환
        kakao_client = KakaoLocalClient()
        coord_response = kakao_client.address_to_coordinates(test_address)
        
        if coord_response.get("status") != "success":
            print(f"[X] 좌표 변환 실패: {coord_response}")
            return
        
        coord_data = coord_response.get("data", {})
        coord_docs = coord_data.get("documents", [])
        
        if not coord_docs:
            print("[X] 주소를 찾을 수 없습니다.")
            return
        
        first_result = coord_docs[0]
        lat = float(first_result.get('y'))
        lng = float(first_result.get('x'))
        
        print(f"[OK] 좌표 변환 성공!")
        print(f"  위도: {lat}")
        print(f"  경도: {lng}")
        print(f"  주소: {first_result.get('address_name', 'N/A')}")
        
        # 주변 주차장 검색
        print(f"\n[2단계] 주변 주차장 검색 (카카오 API)")
        print(f"검색 반경: {search_radius}m")
        print("-" * 70)
        
        parking_response = kakao_client.search_parking_nearby(
            latitude=lat,
            longitude=lng,
            radius=search_radius,
            size=15
        )
        
        if parking_response.get("status") != "success":
            print(f"[X] 주차장 검색 실패: {parking_response}")
            return
        
        parking_data = parking_response.get("data", {})
        parking_docs = parking_data.get("documents", [])
        
        print(f"[OK] 주변 주차장 {len(parking_docs)}개 발견!")
        
        # 파싱
        parking_list = _parse_kakao_parking_response(parking_data)
        
        # 서울 지역 주차장 필터링 및 실시간 정보 추가
        print(f"\n[3단계] 서울 실시간 정보 추가")
        print("-" * 70)
        
        formatted_parkings = []
        seoul_count = 0
        other_count = 0
        
        for i, parking in enumerate(parking_list, 1):
            address = parking.get("address", "") or parking.get("road_address", "")
            region = _get_region(address)
            
            if region == "seoul":
                seoul_count += 1
            else:
                other_count += 1
            
            # 실시간 정보 조회 (서울 지역만)
            realtime_info = None
            if region == "seoul":
                realtime_info = _get_realtime_info_seoul(
                    parking.get("name", ""),
                    address
                )
            
            # 표준 형식으로 변환
            standard_parking = {
                "name": parking.get("name", ""),
                "address": address,
                "total_spots": None,
                "fee": parking.get("category", ""),
                "distance": parking.get("distance", 0),
                "phone": parking.get("phone", ""),
            }
            
            formatted_parking = _format_parking_info(standard_parking, region, realtime_info)
            formatted_parkings.append(formatted_parking)
        
        print(f"서울 지역: {seoul_count}개, 기타 지역: {other_count}개")
        
        # 결과 출력
        print(f"\n[4단계] 검색 결과")
        print("-" * 70)
        
        for i, parking in enumerate(formatted_parkings[:10], 1):  # 상위 10개만
            print(f"\n--- 주차장 {i} ---")
            print(f"이름: {parking.get('name', 'N/A')}")
            print(f"주소: {parking.get('address', 'N/A')}")
            print(f"거리: {parking.get('distance', 0)}m")
            
            if parking.get('available_spots') is not None:
                print(f"[실시간 정보]")
                print(f"  총 주차 대수: {parking.get('total_spots', 'N/A')}")
                print(f"  주차 가능 대수: {parking.get('available_spots', 'N/A')}")
            else:
                if parking.get('notice'):
                    print(f"[안내] {parking.get('notice')}")
                else:
                    print(f"[정보] 실시간 정보 없음")
        
        # 실시간 정보가 있는 주차장 개수
        realtime_count = sum(1 for p in formatted_parkings if p.get('available_spots') is not None)
        
        print(f"\n[테스트 완료]")
        print(f"총 주차장: {len(formatted_parkings)}개")
        print(f"실시간 정보 제공: {realtime_count}개")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n[X] 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_hoegi_parking()

