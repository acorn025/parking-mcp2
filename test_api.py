"""
API 클라이언트 테스트 스크립트
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_api_clients():
    """각 API 클라이언트 초기화 테스트"""
    print("=" * 50)
    print("API 클라이언트 초기화 테스트")
    print("=" * 50)
    
    # 환경변수 확인
    print("\n[환경변수 확인]")
    keys = {
        "PUBLIC_DATA_API_KEY": os.getenv("PUBLIC_DATA_API_KEY"),
        "SEOUL_DATA_API_KEY": os.getenv("SEOUL_DATA_API_KEY"),
        "GYEONGGI_DATA_API_KEY": os.getenv("GYEONGGI_DATA_API_KEY"),
        "KAKAO_REST_API_KEY": os.getenv("KAKAO_REST_API_KEY"),
    }
    
    for key, value in keys.items():
        if value and value != f"your_{key.lower()}_here":
            print(f"[OK] {key}: 설정됨 ({value[:10]}...)")
        else:
            print(f"[X] {key}: 설정되지 않음")
    
    # 클라이언트 초기화 테스트
    print("\n[클라이언트 초기화 테스트]")
    
    try:
        from api_clients import PublicDataClient
        client = PublicDataClient()
        print("[OK] PublicDataClient: 초기화 성공")
    except Exception as e:
        print(f"[X] PublicDataClient: {str(e)}")
    
    try:
        from api_clients import SeoulDataClient
        client = SeoulDataClient()
        print("[OK] SeoulDataClient: 초기화 성공")
    except Exception as e:
        print(f"[X] SeoulDataClient: {str(e)}")
    
    try:
        from api_clients import GyeonggiDataClient
        client = GyeonggiDataClient()
        print("[OK] GyeonggiDataClient: 초기화 성공")
    except Exception as e:
        print(f"[X] GyeonggiDataClient: {str(e)}")
    
    try:
        from api_clients import KakaoLocalClient
        client = KakaoLocalClient()
        print("[OK] KakaoLocalClient: 초기화 성공")
    except Exception as e:
        print(f"[X] KakaoLocalClient: {str(e)}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_api_clients()

