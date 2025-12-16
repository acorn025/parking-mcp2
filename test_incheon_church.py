"""
인천 신광교회 주차장 정보 테스트
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_incheon_church():
    """인천 신광교회 주차장 정보 테스트"""
    print("=" * 70)
    print("인천 신광교회 주차장 정보 테스트")
    print("=" * 70)
    
    test_address = "인천광역시"  # 더 구체적인 주소로 시도
    search_radius = 500  # 500m
    
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
        from src.server import _parse_kakao_parking_response, _get_region, _format_parking_info, _get_realtime_info_seoul, _get_realtime_info_gyeonggi
        
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
        
        # 3단계: 실시간 정보 확인
        print(f"\n[3단계] 주차장 정보 및 실시간 정보 확인")
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
            elif region == "gyeonggi":
                realtime_info = _get_realtime_info_gyeonggi(
                    parking.get("name", ""),
                    address
                )
            
            if realtime_info:
                print(f"    [실시간 정보]")
                if realtime_info.get('available_spots') is not None:
                    print(f"      주차 가능: {realtime_info.get('available_spots')}대")
                    print(f"      전체 대수: {realtime_info.get('total_spots', 'N/A')}대")
                if realtime_info.get('fee_info'):
                    print(f"      요금 정보 있음")
            else:
                if region == "other":
                    print(f"    [안내] 인천 지역은 기본 주차장 정보만 제공됩니다.")
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
        print("[최종 결과]")
        print("=" * 70)
        
        # 신광교회 관련 주차장 찾기
        church_parkings = [p for p in formatted_parkings if "신광" in p.get("name", "") or "교회" in p.get("name", "")]
        
        if church_parkings:
            print("\n[신광교회 관련 주차장]")
            for parking in church_parkings:
                print(f"\n{parking.get('name', 'N/A')}")
                print(f"  주소: {parking.get('address', 'N/A')}")
                if parking.get('available_spots') is not None:
                    print(f"  실시간: {parking.get('available_spots')}대 주차 가능 / 전체 {parking.get('total_spots', 'N/A')}대")
                else:
                    print(f"  실시간 정보: 제공되지 않음 (인천 지역)")
                    print(f"  전체 대수: {parking.get('total_spots', 'N/A')}대")
        else:
            print("\n[신광교회 관련 주차장을 찾을 수 없습니다]")
            print("\n[근처 주차장 목록]")
            for parking in formatted_parkings[:3]:
                print(f"\n{parking.get('name', 'N/A')}")
                print(f"  주소: {parking.get('address', 'N/A')}")
                if parking.get('available_spots') is not None:
                    print(f"  실시간: {parking.get('available_spots')}대 주차 가능")
                else:
                    print(f"  실시간 정보: 제공되지 않음")
        
        print(f"\n[지역 정보] 인천은 서울/경기 지역이 아니므로 실시간 주차 정보가 제공되지 않습니다.")
        
    except Exception as e:
        print(f"[X] 오류: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_incheon_church()

