"""
부산 해운대 지역 주차장 검색 테스트
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_busan_haeundae():
    """부산 해운대 지역 주차장 검색"""
    print("=" * 80)
    print("부산 해운대 지역 주차장 검색")
    print("=" * 80)
    
    test_address = "부산 해운대"
    
    try:
        from api_clients import KakaoLocalClient
        from src.server import (
            _parse_kakao_parking_response,
            _get_region,
            _format_parking_info
        )
        
        # 좌표 변환
        kakao_client = KakaoLocalClient()
        coord_response = kakao_client.address_to_coordinates(test_address)
        
        if coord_response.get("status") != "success":
            print("[X] 좌표 변환 실패")
            return
        
        coord_data = coord_response.get("data", {})
        coord_docs = coord_data.get("documents", [])
        
        if not coord_docs:
            print("[X] 주소를 찾을 수 없습니다.")
            return
        
        first_result = coord_docs[0]
        lat = float(first_result.get('y'))
        lng = float(first_result.get('x'))
        
        print(f"\n[검색 위치] {test_address}")
        print(f"[좌표] 위도: {lat}, 경도: {lng}")
        print(f"[주소] {first_result.get('address_name', 'N/A')}")
        print("-" * 80)
        
        # 주차장 검색
        print(f"\n[주변 주차장 검색 중...]")
        parking_response = kakao_client.search_parking_nearby(
            latitude=lat,
            longitude=lng,
            radius=1500,
            size=15
        )
        
        if parking_response.get("status") != "success":
            print(f"[X] 주차장 검색 실패")
            return
        
        parking_data = parking_response.get("data", {})
        parking_list = _parse_kakao_parking_response(parking_data)
        
        print(f"[검색 결과] {len(parking_list)}개의 주차장을 찾았습니다.\n")
        
        # 지역별 분류
        seoul_count = 0
        gyeonggi_count = 0
        other_count = 0
        
        formatted_parkings = []
        for parking in parking_list:
            address = parking.get("address", "") or parking.get("road_address", "")
            region = _get_region(address)
            
            if region == "seoul":
                seoul_count += 1
            elif region == "gyeonggi":
                gyeonggi_count += 1
            else:
                other_count += 1
            
            standard_parking = {
                "name": parking.get("name", ""),
                "address": address,
                "total_spots": None,
                "fee": parking.get("category", ""),
                "distance": parking.get("distance", 0),
            }
            
            formatted = _format_parking_info(standard_parking, region, None)
            formatted_parkings.append(formatted)
        
        print(f"[지역 분류]")
        print(f"  서울: {seoul_count}개")
        print(f"  경기: {gyeonggi_count}개")
        print(f"  기타: {other_count}개")
        print("-" * 80)
        
        # 결과 출력
        print(f"\n[주차장 목록]\n")
        for i, parking in enumerate(formatted_parkings[:10], 1):
            print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"[주차장 {i}] {parking.get('name', 'N/A')}")
            print(f"   주소: {parking.get('address', 'N/A')}")
            if parking.get('distance', 0) > 0:
                print(f"   거리: {parking.get('distance', 0)}m")
            
            if parking.get('notice'):
                print(f"\n   [안내] {parking.get('notice')}")
            else:
                print(f"\n   [정보] 기본 주차장 정보만 제공됩니다.")
            print()
        
        print("=" * 80)
        
    except Exception as e:
        print(f"\n[X] 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_busan_haeundae()

