"""
인천 신광교회 주차장 상세 테스트
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_incheon_church_detailed():
    """인천 신광교회 주차장 상세 테스트"""
    print("=" * 70)
    print("인천 신광교회 주차장 정보 테스트")
    print("=" * 70)
    
    # 여러 검색어 시도
    test_addresses = [
        "인천 신광교회",
        "인천광역시 신광교회",
        "인천시 신광교회",
    ]
    
    for test_address in test_addresses:
        print(f"\n[검색 시도] {test_address}")
        print("-" * 70)
        
        # 1단계: 주소 -> 좌표 변환
        try:
            from src.server import _address_to_coordinates
            
            lat, lng = _address_to_coordinates(test_address)
            
            if lat and lng:
                print(f"[OK] 좌표 변환 성공")
                print(f"  위도: {lat}")
                print(f"  경도: {lng}")
                
                # 2단계: 주변 주차장 검색
                print(f"\n[주변 주차장 검색]")
                print("-" * 70)
                
                from src.api_clients import KakaoLocalClient
                from src.server import _parse_kakao_parking_response, _get_region
                
                kakao_client = KakaoLocalClient()
                response = kakao_client.search_parking_nearby(
                    latitude=lat,
                    longitude=lng,
                    radius=500,
                    size=15
                )
                
                if response.get("status") == "success":
                    kakao_data = response.get("data", {})
                    parking_list = _parse_kakao_parking_response(kakao_data)
                    
                    print(f"[OK] 주차장 {len(parking_list)}개 발견")
                    
                    # 신광교회 관련 주차장 찾기
                    church_parkings = [p for p in parking_list if "신광" in p.get("name", "") or "교회" in p.get("name", "")]
                    
                    if church_parkings:
                        print(f"\n[신광교회 관련 주차장 발견!]")
                        for parking in church_parkings:
                            print(f"\n  {parking.get('name', 'N/A')}")
                            print(f"    주소: {parking.get('address', 'N/A')}")
                            print(f"    도로명주소: {parking.get('road_address', 'N/A')}")
                            
                            # 지역 확인
                            address = parking.get("address", "") or parking.get("road_address", "")
                            region = _get_region(address)
                            print(f"    지역: {region}")
                            
                            if region == "other":
                                print(f"    [답변] 인천 지역은 실시간 주차 정보를 제공할 수 없습니다.")
                                print(f"            기본 주차장 정보만 제공됩니다.")
                            elif region == "seoul":
                                print(f"    [답변] 서울 지역이므로 실시간 주차 가능 대수를 확인할 수 있습니다.")
                            elif region == "gyeonggi":
                                print(f"    [답변] 경기 지역이므로 요금/운영시간 정보만 제공됩니다.")
                                print(f"            실시간 주차 가능 대수는 제공되지 않습니다.")
                        
                        return  # 성공했으므로 종료
                    else:
                        print(f"\n[근처 주차장 목록]")
                        for i, parking in enumerate(parking_list[:5], 1):
                            print(f"  {i}. {parking.get('name', 'N/A')} - {parking.get('address', 'N/A')}")
                else:
                    print(f"[X] 주차장 검색 실패")
            else:
                print(f"[X] 좌표 변환 실패")
        except Exception as e:
            print(f"[X] 오류: {str(e)}")
            continue
    
    # 모든 검색어 실패 시
    print("\n" + "=" * 70)
    print("[최종 답변]")
    print("=" * 70)
    print("\n'인천 신광교회' 주차장을 찾을 수 없습니다.")
    print("\n[안내]")
    print("- 인천 지역은 서울/경기 지역이 아니므로 실시간 주차 정보를 제공할 수 없습니다.")
    print("- 더 구체적인 주소(예: '인천광역시 남동구...')를 입력하시면 근처 주차장을 찾아드릴 수 있습니다.")
    print("- 실시간 주차 가능 대수는 서울 지역에서만 제공됩니다.")

if __name__ == "__main__":
    test_incheon_church_detailed()

