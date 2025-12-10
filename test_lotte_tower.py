"""
잠실 롯데타워 근처 주차장 검색 테스트
수정된 서버 코드 테스트
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_lotte_tower_parking():
    """잠실 롯데타워 근처 주차장 검색 테스트"""
    print("=" * 70)
    print("잠실 롯데타워 근처 주차장 검색 테스트")
    print("=" * 70)
    
    test_address = "서울 송파구 올림픽로 300"  # 롯데월드타워 정확한 주소
    search_radius = 1000  # 1km
    
    print(f"\n[1단계] 주소 -> 좌표 변환")
    print(f"주소: {test_address}")
    print("-" * 70)
    
    try:
        from api_clients import KakaoLocalClient
        
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
        
        # 주변 주차장 검색 (수정된 서버 로직 시뮬레이션)
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
        
        print(f"[OK] 주변 주차장 {len(parking_docs)}개 발견!\n")
        
        # 서버의 파싱 함수 시뮬레이션
        from src.server import _parse_kakao_parking_response, _get_region, _format_parking_info
        from api_clients import SeoulDataClient, GyeonggiDataClient
        
        parking_list = _parse_kakao_parking_response(parking_data)
        
        print(f"[3단계] 주차장 정보 포맷팅 및 실시간 정보 추가")
        print("-" * 70)
        
        formatted_parkings = []
        for i, parking in enumerate(parking_list[:10], 1):  # 상위 10개만
            address = parking.get("address", "") or parking.get("road_address", "")
            region = _get_region(address)
            
            print(f"\n--- 주차장 {i} ---")
            print(f"이름: {parking.get('name', 'N/A')}")
            print(f"주소: {address}")
            print(f"거리: {parking.get('distance', 0)}m")
            print(f"지역: {region}")
            
            # 실시간 정보 조회 (서울인 경우)
            realtime_info = None
            if region == "seoul":
                print(f"  → 서울 지역: 실시간 정보 조회 시도...")
                # 실제로는 _get_realtime_info_seoul 호출하지만 여기서는 간단히 표시만
                realtime_info = None  # 실제 구현에서는 조회
            elif region == "gyeonggi":
                print(f"  → 경기 지역: 실시간 정보 조회 시도...")
                realtime_info = None
            else:
                print(f"  → 기타 지역: 기본 정보만 제공")
            
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
            
            print(f"포맷팅 결과:")
            print(f"  - 이름: {formatted_parking.get('name')}")
            print(f"  - 주소: {formatted_parking.get('address')}")
            print(f"  - 실시간 주차 가능: {formatted_parking.get('available_spots')}")
            print(f"  - 총 주차 대수: {formatted_parking.get('total_spots')}")
            if formatted_parking.get('notice'):
                print(f"  - 안내: {formatted_parking.get('notice')}")
            
            formatted_parkings.append(formatted_parking)
        
        print(f"\n[테스트 완료]")
        print(f"총 {len(parking_list)}개의 주차장을 찾았습니다.")
        print(f"포맷팅된 주차장: {len(formatted_parkings)}개")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n[X] 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_lotte_tower_parking()

