"""
경기 API 원시 응답 확인
"""

import sys
import os
import requests
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_gyeonggi_raw():
    """경기 API 원시 응답 확인"""
    api_key = os.getenv("GYEONGGI_DATA_API_KEY")
    base_url = "https://openapi.gg.go.kr"
    
    # 경기데이터드림 API 엔드포인트 확인
    # 일반적인 형식: /서비스명?KEY=인증키&Type=json&pIndex=1&pSize=10
    endpoint = "/Parking"
    url = base_url + endpoint
    params = {
        "KEY": api_key,
        "Type": "json",
        "pIndex": 1,
        "pSize": 5,
    }
    
    print(f"URL: {url}")
    print(f"Params: {params}")
    print(f"요청 중...")
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"상태 코드: {response.status_code}")
        print(f"응답 헤더: {dict(response.headers)}")
        print(f"\n응답 본문 (처음 1000자):")
        print(response.text[:1000])
        
        # Content-Type 확인
        content_type = response.headers.get('Content-Type', '')
        print(f"\nContent-Type: {content_type}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"\nJSON 파싱 성공!")
                print(f"키: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
                
                if isinstance(data, dict):
                    parking = data.get("Parking", {})
                    if parking:
                        print(f"\n[Parking 구조]")
                        print(f"키: {list(parking.keys())}")
                        
                        row = parking.get("row", [])
                        if row and len(row) > 0:
                            print(f"\n[첫 번째 주차장 데이터]")
                            first = row[0]
                            print(f"키: {list(first.keys())}")
                            for key, value in list(first.items())[:15]:
                                print(f"  {key}: {value}")
            except:
                print("JSON 파싱 실패")
            
    except Exception as e:
        print(f"오류: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gyeonggi_raw()

