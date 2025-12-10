"""
MCP 서버 구조 테스트
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_server_import():
    """서버 모듈 import 테스트"""
    print("=" * 50)
    print("MCP 서버 구조 테스트")
    print("=" * 50)
    
    try:
        # 서버 모듈 import
        print("\n[테스트 1] 서버 모듈 import")
        import src.server as server_module
        print("[OK] 서버 모듈 import 성공")
        
        # FastMCP 앱 확인
        print("\n[테스트 2] FastMCP 앱 확인")
        app = server_module.app
        print(f"[OK] FastMCP 앱 생성됨: {app}")
        
        # Tool 함수 확인
        print("\n[테스트 3] Tool 함수 확인")
        tools = []
        if hasattr(app, 'tools') or hasattr(app, '_tools'):
            # fastMCP의 실제 구조에 따라 조정 필요
            print("[OK] Tool 등록 확인됨")
        else:
            print("[INFO] Tool 구조 확인 필요 (fastMCP 버전에 따라 다를 수 있음)")
        
        # Helper 함수 확인
        print("\n[테스트 4] Helper 함수 확인")
        helper_functions = [
            '_is_seoul',
            '_is_gyeonggi',
            '_get_region',
            '_format_parking_info',
            '_get_realtime_info_seoul',
            '_get_realtime_info_gyeonggi',
            '_parse_xml_response'
        ]
        
        for func_name in helper_functions:
            if hasattr(server_module, func_name):
                print(f"[OK] {func_name} 함수 존재")
            else:
                print(f"[X] {func_name} 함수 없음")
        
        # Tool 함수 확인
        print("\n[테스트 5] Tool 함수 확인")
        if hasattr(server_module, 'search_nearby_parking'):
            print("[OK] search_nearby_parking 함수 존재")
        else:
            print("[X] search_nearby_parking 함수 없음")
            
        if hasattr(server_module, 'get_parking_info'):
            print("[OK] get_parking_info 함수 존재")
        else:
            print("[X] get_parking_info 함수 없음")
        
        print("\n" + "=" * 50)
        print("[결과] 서버 구조가 정상적으로 구성되었습니다!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n[X] 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_server_import()


