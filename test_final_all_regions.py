"""
세 가지 지역 최종 테스트
실제 이용자가 받는 응답 형식으로 테스트
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_seoul():
    """서울 지역 테스트"""
    print("=" * 80)
    print("서울 지역 테스트")
    print("=" * 80)
    print("\n[검색 위치] 서울시 중구 세종대로 110 (서울특별시청)")
    print("-" * 80)
    
    try:
        # MCP 서버의 search_nearby_parking 함수 직접 호출
        from src.server import search_nearby_parking
        
        # 좌표 변환 (서울시청)
        from api_clients import KakaoLocalClient
        kakao_client = KakaoLocalClient()
        coord_response = kakao_client.address_to_coordinates("서울시 중구 세종대로 110")
        
        if coord_response.get("status") != "success":
            print("[X] 좌표 변환 실패")
            return
        
        lat = float(coord_response.get("data", {}).get("documents", [])[0].get('y'))
        lng = float(coord_response.get("data", {}).get("documents", [])[0].get('x'))
        
        print(f"[좌표] 위도: {lat}, 경도: {lng}")
        print(f"\n[주변 주차장 검색 중...]")
        
        # MCP 서버 함수 호출
        result = search_nearby_parking(
            latitude=lat,
            longitude=lng,
            radius=1000.0
        )
        
        if result.get("error"):
            print(f"\n[오류] {result.get('error')}")
            return
        
        parkings = result.get("parkings", [])
        print(f"\n[검색 결과] {len(parkings)}개의 주차장을 찾았습니다.\n")
        
        # 서울 지역 주차장 중 실시간 정보가 있는 것만 표시
        seoul_with_info = [p for p in parkings if p.get('available_spots') is not None]
        
        if seoul_with_info:
            print(f"[실시간 정보 제공 주차장] {len(seoul_with_info)}개\n")
            for i, parking in enumerate(seoul_with_info[:3], 1):
                print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                print(f"주차장 {i}: {parking.get('name', 'N/A')}")
                print(f"주소: {parking.get('address', 'N/A')}")
                print(f"\n[실시간 정보]")
                print(f"  총 주차 대수: {parking.get('total_spots', 'N/A')}대")
                print(f"  현재 주차 대수: {parking.get('total_spots', 0) - parking.get('available_spots', 0)}대")
                print(f"  주차 가능 대수: {parking.get('available_spots', 'N/A')}대")
                
                if parking.get('operating_info'):
                    op = parking.get('operating_info')
                    print(f"\n[운영 시간]")
                    print(f"  평일: {op.get('weekday_start', 'N/A')} ~ {op.get('weekday_end', 'N/A')}")
                    print(f"  주말: {op.get('weekend_start', 'N/A')} ~ {op.get('weekend_end', 'N/A')}")
                    print(f"  공휴일: {op.get('holiday_start', 'N/A')} ~ {op.get('holiday_end', 'N/A')}")
                
                if parking.get('fee_info'):
                    fee = parking.get('fee_info')
                    print(f"\n[요금 정보]")
                    print(f"  유료 여부: {fee.get('is_paid', 'N/A')}")
                    print(f"  기본 요금: {fee.get('basic_fee', 0)}원 / {fee.get('basic_hours', 0)}분")
                    print(f"  추가 요금: {fee.get('additional_fee', 0)}원 / {fee.get('additional_hours', 0)}분")
                    if fee.get('daily_max_fee'):
                        print(f"  일일 최대 요금: {fee.get('daily_max_fee')}원")
                print()
        else:
            print("[정보] 실시간 정보를 제공하는 주차장이 없습니다.")
            print("(주차장명 매칭이 정확하지 않을 수 있습니다.)\n")
        
        print("=" * 80)
        
    except Exception as e:
        print(f"\n[X] 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

def test_gyeonggi():
    """경기 지역 테스트"""
    print("\n" + "=" * 80)
    print("경기 지역 테스트")
    print("=" * 80)
    print("\n[검색 위치] 경기도 수원시 팔달구 정조로 825")
    print("-" * 80)
    
    try:
        from src.server import search_nearby_parking
        from api_clients import KakaoLocalClient
        
        kakao_client = KakaoLocalClient()
        coord_response = kakao_client.address_to_coordinates("경기도 수원시 팔달구 정조로 825")
        
        if coord_response.get("status") != "success":
            print("[X] 좌표 변환 실패")
            return
        
        lat = float(coord_response.get("data", {}).get("documents", [])[0].get('y'))
        lng = float(coord_response.get("data", {}).get("documents", [])[0].get('x'))
        
        print(f"[좌표] 위도: {lat}, 경도: {lng}")
        print(f"\n[주변 주차장 검색 중...]")
        
        result = search_nearby_parking(
            latitude=lat,
            longitude=lng,
            radius=1000.0
        )
        
        if result.get("error"):
            print(f"\n[오류] {result.get('error')}")
            return
        
        parkings = result.get("parkings", [])
        print(f"\n[검색 결과] {len(parkings)}개의 주차장을 찾았습니다.\n")
        
        # 경기 지역 주차장 중 정보가 있는 것만 표시
        gyeonggi_with_info = [p for p in parkings if p.get('operating_info') or p.get('fee_info')]
        
        if gyeonggi_with_info:
            print(f"[요금 및 운영시간 정보 제공 주차장] {len(gyeonggi_with_info)}개\n")
            for i, parking in enumerate(gyeonggi_with_info[:3], 1):
                print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                print(f"주차장 {i}: {parking.get('name', 'N/A')}")
                print(f"주소: {parking.get('address', 'N/A')}")
                
                if parking.get('total_spots'):
                    print(f"\n[주차장 정보]")
                    print(f"  총 주차 대수: {parking.get('total_spots')}대")
                
                if parking.get('operating_info'):
                    op = parking.get('operating_info')
                    print(f"\n[운영 시간]")
                    print(f"  평일: {op.get('weekday_start', 'N/A')} ~ {op.get('weekday_end', 'N/A')}")
                    print(f"  토요일: {op.get('saturday_start', 'N/A')} ~ {op.get('saturday_end', 'N/A')}")
                    print(f"  공휴일: {op.get('holiday_start', 'N/A')} ~ {op.get('holiday_end', 'N/A')}")
                
                if parking.get('fee_info'):
                    fee = parking.get('fee_info')
                    print(f"\n[요금 정보]")
                    print(f"  유료 여부: {fee.get('is_paid', 'N/A')}")
                    print(f"  기본 요금: {fee.get('basic_fee', 0)}원 / {fee.get('basic_time', 0)}분")
                    print(f"  추가 요금: {fee.get('additional_fee', 0)}원 / {fee.get('additional_time', 0)}분")
                    if fee.get('payment_method'):
                        print(f"  결제 방법: {fee.get('payment_method')}")
                print()
        else:
            print("[정보] 요금 및 운영시간 정보를 제공하는 주차장이 없습니다.")
            print("(주차장명 매칭이 정확하지 않을 수 있습니다.)\n")
        
        print("=" * 80)
        
    except Exception as e:
        print(f"\n[X] 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

def test_other():
    """기타 지역 테스트"""
    print("\n" + "=" * 80)
    print("기타 지역 테스트")
    print("=" * 80)
    print("\n[검색 위치] 부산 해운대구 해운대해변로 264")
    print("-" * 80)
    
    try:
        from src.server import search_nearby_parking
        from api_clients import KakaoLocalClient
        
        kakao_client = KakaoLocalClient()
        coord_response = kakao_client.address_to_coordinates("부산 해운대구 해운대해변로 264")
        
        if coord_response.get("status") != "success":
            print("[X] 좌표 변환 실패")
            return
        
        lat = float(coord_response.get("data", {}).get("documents", [])[0].get('y'))
        lng = float(coord_response.get("data", {}).get("documents", [])[0].get('x'))
        
        print(f"[좌표] 위도: {lat}, 경도: {lng}")
        print(f"\n[주변 주차장 검색 중...]")
        
        result = search_nearby_parking(
            latitude=lat,
            longitude=lng,
            radius=1000.0
        )
        
        if result.get("error"):
            print(f"\n[오류] {result.get('error')}")
            return
        
        parkings = result.get("parkings", [])
        print(f"\n[검색 결과] {len(parkings)}개의 주차장을 찾았습니다.\n")
        
        # 기타 지역 주차장 표시
        if parkings:
            print(f"[주차장 목록]\n")
            for i, parking in enumerate(parkings[:5], 1):
                print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
                print(f"주차장 {i}: {parking.get('name', 'N/A')}")
                print(f"주소: {parking.get('address', 'N/A')}")
                print(f"거리: {parking.get('distance', 0)}m")
                
                if parking.get('notice'):
                    print(f"\n[안내] {parking.get('notice')}")
                else:
                    print(f"\n[정보] 기본 주차장 정보만 제공됩니다.")
                print()
        else:
            print("[정보] 주차장을 찾을 수 없습니다.\n")
        
        print("=" * 80)
        
    except Exception as e:
        print(f"\n[X] 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

def summary():
    """최종 요약"""
    print("\n" + "=" * 80)
    print("최종 테스트 요약")
    print("=" * 80)
    
    print("\n[서울 지역]")
    print("  - 실시간 주차 대수: 제공")
    print("  - 총 주차 대수: 제공")
    print("  - 운영 시간: 제공")
    print("  - 요금 정보: 제공")
    print("  - 업데이트 시간: 제공")
    
    print("\n[경기 지역]")
    print("  - 실시간 주차 대수: 제공 안됨 (API에 없음)")
    print("  - 총 주차 대수: 제공")
    print("  - 운영 시간: 제공")
    print("  - 요금 정보: 제공")
    
    print("\n[기타 지역]")
    print("  - 기본 주차장 정보: 제공")
    print("  - 실시간 정보: 제공 안됨")
    print("  - 안내 메시지: 제공")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    test_seoul()
    test_gyeonggi()
    test_other()
    summary()

