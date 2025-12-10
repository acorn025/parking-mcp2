"""
주변 주차장 검색 테스트
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_parking_search():
    """주소 -> 좌표 변환 -> 주변 주차장 검색 테스트"""
    print("=" * 60)
    print("주변 주차장 검색 테스트")
    print("=" * 60)
    
    test_address = "서울특별시 을지로 65"
    print(f"\n[1단계] 주소 -> 좌표 변환")
    print(f"주소: {test_address}")
    print("-" * 60)
    
    try:
        from api_clients import KakaoLocalClient
        
        # 주소를 좌표로 변환
        kakao_client = KakaoLocalClient()
        response = kakao_client.address_to_coordinates(test_address)
        
        if response.get("status") != "success":
            print(f"[X] 좌표 변환 실패: {response}")
            return
        
        data = response.get("data", {})
        documents = data.get("documents", [])
        
        if not documents:
            print("[X] 주소를 찾을 수 없습니다.")
            return
        
        first_result = documents[0]
        lat = float(first_result.get('y'))
        lng = float(first_result.get('x'))
        
        print(f"[OK] 좌표 변환 성공!")
        print(f"위도: {lat}")
        print(f"경도: {lng}")
        print(f"주소명: {first_result.get('address_name', 'N/A')}")
        
        # 주변 주차장 검색
        print(f"\n[2단계] 주변 주차장 검색")
        print(f"검색 반경: 1000m")
        print("-" * 60)
        
        parking_response = kakao_client.search_parking_nearby(
            latitude=lat,
            longitude=lng,
            radius=1000,
            size=10
        )
        
        if parking_response.get("status") != "success":
            print(f"[X] 주차장 검색 실패: {parking_response}")
            return
        
        parking_data = parking_response.get("data", {})
        parking_docs = parking_data.get("documents", [])
        
        print(f"[OK] 주변 주차장 {len(parking_docs)}개 발견!\n")
        
        for i, parking in enumerate(parking_docs, 1):
            print(f"--- 주차장 {i} ---")
            print(f"이름: {parking.get('place_name', 'N/A')}")
            print(f"주소: {parking.get('address_name', 'N/A')}")
            print(f"도로명 주소: {parking.get('road_address_name', 'N/A')}")
            print(f"거리: {parking.get('distance', 'N/A')}m")
            print(f"전화번호: {parking.get('phone', 'N/A')}")
            print(f"카테고리: {parking.get('category_name', 'N/A')}")
            
            # 좌표 정보
            if parking.get('y') and parking.get('x'):
                print(f"위치: 위도 {parking.get('y')}, 경도 {parking.get('x')}")
            
            # URL 정보
            if parking.get('place_url'):
                print(f"상세 정보: {parking.get('place_url')}")
            
            print()
        
        print("=" * 60)
        print(f"[테스트 완료] 총 {len(parking_docs)}개의 주차장을 찾았습니다.")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[X] 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_parking_search()


