"""
인천 신광교회 - 친절한 안내 메시지 테스트
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_friendly_message():
    """친절한 안내 메시지 테스트"""
    print("=" * 70)
    print("인천 신광교회 - 친절한 안내 메시지 테스트")
    print("=" * 70)
    
    test_address = "인천 신광교회"
    
    print(f"\n[테스트 주소] {test_address}")
    print("-" * 70)
    
    try:
        from src.server import _address_to_coordinates, _get_region
        
        # 주소 변환 시도
        lat, lng = _address_to_coordinates(test_address)
        
        if lat is None or lng is None:
            # 지역 확인
            region = _get_region(test_address)
            print(f"\n[지역 감지] {region}")
            
            # 안내 메시지 생성
            if region == "other":
                message = (
                    f"주소 '{test_address}'를 찾을 수 없습니다.\n\n"
                    "인천 지역은 서울/경기 지역이 아니어서 실시간 주차 가능 대수 정보를 제공할 수 없습니다.\n\n"
                    "근처 주차장을 검색해드릴까요? 더 구체적인 주소(예: \"인천광역시 남동구...\")를 알려주시면 "
                    "근처 주차장 위치와 기본 정보를 찾아드릴 수 있습니다."
                )
            else:
                message = f"주소 '{test_address}'를 찾을 수 없습니다. 주소를 확인해주세요."
            
            print("\n[응답 메시지]")
            print("=" * 70)
            print(message)
            print("=" * 70)
        else:
            print(f"[OK] 좌표 변환 성공: {lat}, {lng}")
            
    except Exception as e:
        print(f"[X] 오류: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_friendly_message()

