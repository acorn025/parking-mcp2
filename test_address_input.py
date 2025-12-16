"""
주소 입력 기능 테스트
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_address_to_coordinates():
    """주소를 좌표로 변환 테스트"""
    print("=" * 70)
    print("주소 → 좌표 변환 테스트")
    print("=" * 70)
    
    test_address = "서울시 중구 세종대로 110"
    print(f"\n[테스트 주소] {test_address}")
    print("-" * 70)
    
    try:
        from src.server import _address_to_coordinates
        
        lat, lng = _address_to_coordinates(test_address)
        
        if lat and lng:
            print(f"\n[성공] 좌표 변환 완료")
            print(f"  위도: {lat}")
            print(f"  경도: {lng}")
        else:
            print(f"\n[실패] 좌표 변환 실패")
            
    except Exception as e:
        print(f"\n[오류] {str(e)}")
        import traceback
        traceback.print_exc()


def test_address_input():
    """주소로 주차장 검색 테스트 (MCP 서버 실행 필요)"""
    print("\n" + "=" * 70)
    print("주소 입력 기능 테스트 (MCP 서버 실행 필요)")
    print("=" * 70)
    print("\n[안내] 이 테스트는 MCP 서버가 실행 중일 때만 작동합니다.")
    print("MCP 클라이언트를 통해 tool을 호출해야 합니다.")

if __name__ == "__main__":
    test_address_to_coordinates()
    test_address_input()

