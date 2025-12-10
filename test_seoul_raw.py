"""
서울 API 원시 응답 확인
"""

import sys
import os
import requests
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_seoul_raw():
    """서울 API 원시 응답 확인"""
    api_key = os.getenv("SEOUL_DATA_API_KEY")
    base_url = "http://openapi.seoul.go.kr:8088"
    
    # 서울 열린데이터 주차장 정보 API 엔드포인트 확인
    # 일반적인 형식: /{인증키}/json/서비스명/시작인덱스/종료인덱스
    endpoint = f"/{api_key}/json/GetParkingInfo/1/10"
    url = base_url + endpoint
    
    print(f"URL: {url}")
    print(f"요청 중...")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"상태 코드: {response.status_code}")
        print(f"응답 헤더: {dict(response.headers)}")
        print(f"\n응답 본문 (처음 1000자):")
        print(response.text[:1000])
        
        # Content-Type 확인
        content_type = response.headers.get('Content-Type', '')
        print(f"\nContent-Type: {content_type}")
        
        if 'xml' in content_type.lower():
            print("\n[결과] XML 형식입니다.")
        elif 'json' in content_type.lower():
            print("\n[결과] JSON 형식입니다.")
            try:
                data = response.json()
                print(f"JSON 파싱 성공!")
                print(f"키: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
            except:
                print("JSON 파싱 실패")
        else:
            print(f"\n[결과] 알 수 없는 형식: {content_type}")
            
    except Exception as e:
        print(f"오류: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_seoul_raw()

