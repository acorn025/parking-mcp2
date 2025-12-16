"""
잠실 롯데타워 실시간 주차 정보 테스트
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_lotte_tower_realtime():
    """잠실 롯데타워 실시간 주차 정보 테스트"""
    print("=" * 70)
    print("잠실 롯데타워 실시간 주차 정보 테스트")
    print("=" * 70)
    
    test_address = "서울 송파구 올림픽로 300"  # 롯데월드타워 주소
    search_radius = 1000  # 1km
    
    print(f"\n[테스트 위치] {test_address}")
    print(f"[검색 반경] {search_radius}m")
    print("=" * 70)
    
    # 1단계: 주소 -> 좌표 변환
    print("\n[1단계] 주소 -> 좌표 변환")
    print("-" * 70)
    
    try:
        from src.server import _address_to_coordinates
        
        lat, lng = _address_to_coordinates(test_address)
        
        if not lat or not lng:
            print("[X] 좌표 변환 실패")
            return
        
        print(f"[OK] 좌표 변환 성공")
        print(f"  위도: {lat}")
        print(f"  경도: {lng}")
        
    except Exception as e:
        print(f"[X] 좌표 변환 오류: {str(e)}")
        return
    
    # 2단계: 주변 주차장 검색
    print(f"\n[2단계] 주변 주차장 검색")
    print("-" * 70)
    
    try:
        from src.api_clients import KakaoLocalClient
        from src.server import _parse_kakao_parking_response, _get_region, _format_parking_info, _get_realtime_info_seoul
        
        kakao_client = KakaoLocalClient()
        response = kakao_client.search_parking_nearby(
            latitude=lat,
            longitude=lng,
            radius=search_radius,
            size=15
        )
        
        if response.get("status") != "success":
            print(f"[X] 주차장 검색 실패: {response}")
            return
        
        kakao_data = response.get("data", {})
        parking_list = _parse_kakao_parking_response(kakao_data)
        
        if not parking_list:
            print("[X] 주차장을 찾을 수 없습니다.")
            return
        
        print(f"[OK] 주차장 {len(parking_list)}개 발견")
        
        # 3단계: 실시간 정보 추가
        print(f"\n[3단계] 실시간 정보 조회 (서울 지역)")
        print("-" * 70)
        
        formatted_parkings = []
        for i, parking in enumerate(parking_list[:5], 1):  # 상위 5개만
            address = parking.get("address", "") or parking.get("road_address", "")
            region = _get_region(address)
            
            print(f"\n[{i}] {parking.get('name', 'N/A')}")
            print(f"    주소: {address}")
            print(f"    지역: {region}")
            
            realtime_info = None
            if region == "seoul":
                realtime_info = _get_realtime_info_seoul(
                    parking.get("name", ""),
                    address
                )
                
                if realtime_info:
                    print(f"    [실시간 정보]")
                    print(f"      주차 가능: {realtime_info.get('available_spots', 'N/A')}대")
                    print(f"      전체 대수: {realtime_info.get('total_spots', 'N/A')}대")
                    print(f"      현재 주차: {realtime_info.get('current_spots', 'N/A')}대")
                    if realtime_info.get('update_time'):
                        print(f"      업데이트: {realtime_info.get('update_time')}")
                else:
                    print(f"    [실시간 정보] 조회 실패 또는 정보 없음")
            
            # 표준 형식으로 변환
            standard_parking = {
                "name": parking.get("name", ""),
                "address": address,
                "total_spots": None,
                "fee": parking.get("category", ""),
                "distance": parking.get("distance", 0),
            }
            
            formatted_parking = _format_parking_info(standard_parking, region, realtime_info)
            formatted_parkings.append(formatted_parking)
        
        # 최종 결과 출력
        print("\n" + "=" * 70)
        print("[최종 결과] 실시간 정보가 있는 주차장")
        print("=" * 70)
        
        realtime_count = 0
        for parking in formatted_parkings:
            if parking.get("available_spots") is not None:
                realtime_count += 1
                print(f"\n{parking.get('name', 'N/A')}")
                print(f"  주소: {parking.get('address', 'N/A')}")
                print(f"  실시간: {parking.get('available_spots')}대 주차 가능 / 전체 {parking.get('total_spots', 'N/A')}대")
                if parking.get('fee_info'):
                    fee = parking.get('fee_info', {})
                    if fee.get('basic_fee'):
                        print(f"  요금: 기본 {fee.get('basic_hours', 0)}분 {fee.get('basic_fee', 0)}원, 추가 {fee.get('additional_hours', 0)}분당 {fee.get('additional_fee', 0)}원")
        
        print(f"\n[요약] 총 {len(formatted_parkings)}개 주차장 중 {realtime_count}개에 실시간 정보 제공")
        
    except Exception as e:
        print(f"[X] 오류: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_lotte_tower_realtime()

