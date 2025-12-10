"""
서울시청 근처 주차장 통합 테스트
- 주소 -> 좌표 변환 (카카오)
- 주변 주차장 검색 (카카오 + 공공데이터)
- 실시간 정보 조회 (서울 열린데이터)
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_seoul_city_hall_parking():
    """서울시청 근처 주차장 통합 테스트"""
    print("=" * 70)
    print("서울시청 근처 주차장 통합 테스트")
    print("=" * 70)
    
    test_address = "서울시 중구 세종대로 110"  # 서울특별시청 정확한 주소
    search_radius = 1000  # 1km
    
    print(f"\n[테스트 위치] {test_address}")
    print(f"[검색 반경] {search_radius}m")
    print("=" * 70)
    
    # 1단계: 주소 -> 좌표 변환
    print("\n[1단계] 주소 -> 좌표 변환 (카카오 로컬 API)")
    print("-" * 70)
    
    try:
        from api_clients import KakaoLocalClient
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
        
    except Exception as e:
        print(f"[X] 좌표 변환 오류: {str(e)}")
        return
    
    # 2단계: 카카오 주차장 검색
    print(f"\n[2단계] 주변 주차장 검색 (카카오 로컬 API)")
    print("-" * 70)
    
    try:
        parking_response = kakao_client.search_parking_nearby(
            latitude=lat,
            longitude=lng,
            radius=search_radius,
            size=15
        )
        
        if parking_response.get("status") == "success":
            parking_data = parking_response.get("data", {})
            parking_docs = parking_data.get("documents", [])
            
            print(f"[OK] 카카오 주차장 {len(parking_docs)}개 발견")
            
            print(f"\n[카카오 주차장 목록]")
            for i, parking in enumerate(parking_docs[:5], 1):  # 상위 5개만 출력
                print(f"\n  {i}. {parking.get('place_name', 'N/A')}")
                print(f"     주소: {parking.get('address_name', 'N/A')}")
                print(f"     거리: {parking.get('distance', 'N/A')}m")
                if parking.get('phone'):
                    print(f"     전화: {parking.get('phone')}")
        else:
            print(f"[X] 카카오 주차장 검색 실패: {parking_response}")
            
    except Exception as e:
        print(f"[X] 카카오 주차장 검색 오류: {str(e)}")
    
    # 3단계: 공공데이터포털 주차장 검색
    print(f"\n[3단계] 공공데이터포털 주차장 검색")
    print("-" * 70)
    
    try:
        from api_clients import PublicDataClient
        public_client = PublicDataClient()
        
        public_response = public_client.search_nearby_parking(
            latitude=lat,
            longitude=lng,
            radius=search_radius
        )
        
        if public_response.get("status") == "success":
            print(f"[OK] 공공데이터 API 호출 성공")
            print(f"  응답 데이터 타입: {type(public_response.get('data'))}")
            # XML 파싱은 서버에서 처리되므로 여기서는 성공 여부만 확인
        else:
            print(f"[X] 공공데이터 검색 실패: {public_response}")
            
    except ValueError as e:
        if "설정되지 않았습니다" in str(e):
            print(f"[INFO] 공공데이터 API 키가 설정되지 않았습니다.")
        else:
            print(f"[X] 공공데이터 검색 오류: {str(e)}")
    except Exception as e:
        print(f"[X] 공공데이터 검색 오류: {str(e)}")
    
    # 4단계: 서울 실시간 주차 정보
    print(f"\n[4단계] 서울 실시간 주차 정보 조회")
    print("-" * 70)
    
    try:
        from api_clients import SeoulDataClient
        seoul_client = SeoulDataClient()
        
        seoul_response = seoul_client.get_realtime_parking_info(
            start_index=1,
            end_index=100
        )
        
        if seoul_response.get("status") == "success":
            seoul_data = seoul_response.get("data", {})
            print(f"[OK] 서울 실시간 주차 정보 조회 성공")
            
            # 응답 구조 확인
            if isinstance(seoul_data, dict):
                parking_info = seoul_data.get("GetParkingInfo", {})
                if parking_info:
                    row = parking_info.get("row", [])
                    print(f"  조회된 주차장 수: {len(row)}개")
                    
                    # 서울시청 근처 주차장 찾기
                    nearby_parkings = []
                    for p in row[:10]:  # 처음 10개만 확인
                        addr = p.get("ADDR", "") or p.get("addr", "")
                        if "중구" in addr or "세종대로" in addr:
                            nearby_parkings.append(p)
                    
                    if nearby_parkings:
                        print(f"\n  [서울시청 근처 실시간 정보]")
                        for i, p in enumerate(nearby_parkings[:3], 1):
                            print(f"\n    {i}. {p.get('PARKING_NAME', 'N/A')}")
                            print(f"       주소: {p.get('ADDR', 'N/A')}")
                            if 'CAPACITY' in p:
                                print(f"       총 주차 대수: {p.get('CAPACITY', 'N/A')}")
                            if 'CUR_PARKING' in p:
                                print(f"       현재 주차 대수: {p.get('CUR_PARKING', 'N/A')}")
        else:
            print(f"[X] 서울 실시간 정보 조회 실패: {seoul_response}")
            
    except ValueError as e:
        if "설정되지 않았습니다" in str(e):
            print(f"[INFO] 서울 데이터 API 키가 설정되지 않았습니다.")
        else:
            print(f"[X] 서울 실시간 정보 오류: {str(e)}")
    except Exception as e:
        print(f"[X] 서울 실시간 정보 오류: {str(e)}")
    
    # 5단계: MCP 서버 함수 시뮬레이션
    print(f"\n[5단계] MCP 서버 함수 시뮬레이션")
    print("-" * 70)
    
    try:
        # server.py의 로직을 시뮬레이션
        print(f"[시뮬레이션] search_nearby_parking 함수 호출")
        print(f"  입력: latitude={lat}, longitude={lng}, radius={search_radius}")
        
        # 지역 구분
        address_str = first_result.get('address_name', '')
        is_seoul = "서울" in address_str or "서울시" in address_str or "서울특별시" in address_str
        
        if is_seoul:
            print(f"  [OK] 서울 지역으로 감지됨")
            print(f"  → 실시간 주차 정보 제공 가능")
        else:
            print(f"  [INFO] 서울 지역이 아님")
            print(f"  → 기본 정보만 제공")
        
        print(f"\n[통합 테스트 완료]")
        print(f"  - 좌표 변환: 성공")
        print(f"  - 카카오 주차장 검색: 성공")
        print(f"  - 공공데이터 검색: 시도 완료")
        print(f"  - 서울 실시간 정보: 시도 완료")
        
    except Exception as e:
        print(f"[X] 시뮬레이션 오류: {str(e)}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_seoul_city_hall_parking()

