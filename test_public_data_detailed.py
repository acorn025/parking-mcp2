"""
공공데이터포털 API 상세 테스트 및 디버깅
"""

import sys
import os
import requests
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_public_data_api():
    """공공데이터포털 API 상세 테스트"""
    print("=" * 70)
    print("공공데이터포털 API 상세 테스트")
    print("=" * 70)
    
    api_key = os.getenv("PUBLIC_DATA_API_KEY")
    
    print(f"\n[1. API 키 확인]")
    print("-" * 70)
    if api_key:
        print(f"[OK] API 키 존재: {api_key[:10]}...{api_key[-4:]}")
        print(f"[INFO] API 키 길이: {len(api_key)}자")
    else:
        print("[X] API 키가 없습니다!")
        return
    
    # 현재 코드에서 사용하는 엔드포인트 확인
    print(f"\n[2. 엔드포인트 및 파라미터 확인]")
    print("-" * 70)
    
    base_url = "http://apis.data.go.kr"
    service_name = "B552895"
    endpoint = f"/{service_name}/ParkingInfoService/getParkingInfo"
    
    print(f"Base URL: {base_url}")
    print(f"Service Name: {service_name}")
    print(f"Endpoint: {endpoint}")
    print(f"Full URL: {base_url}{endpoint}")
    
    # 테스트 파라미터
    test_lat = 37.566370776634
    test_lng = 126.977918351844
    test_radius = 1000
    
    params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows": 10,
        "lat": test_lat,
        "lng": test_lng,
        "radius": test_radius,
    }
    
    print(f"\n[요청 파라미터]")
    for key, value in params.items():
        if key == "serviceKey":
            print(f"  {key}: {value[:10]}...{value[-4:]} (길이: {len(value)})")
        else:
            print(f"  {key}: {value}")
    
    print(f"\n[3. 실제 API 호출 테스트]")
    print("-" * 70)
    
    url = f"{base_url}{endpoint}"
    
    try:
        print(f"요청 URL: {url}")
        print(f"요청 중...")
        
        response = requests.get(url, params=params, timeout=10)
        
        print(f"\n[응답 정보]")
        print(f"상태 코드: {response.status_code}")
        print(f"응답 헤더: {dict(response.headers)}")
        print(f"응답 본문 길이: {len(response.content)} bytes")
        
        if response.status_code == 200:
            print(f"\n[성공] API 호출 성공!")
            print(f"응답 내용 (처음 500자):")
            print(response.text[:500])
        else:
            print(f"\n[에러] HTTP {response.status_code}")
            print(f"응답 본문:")
            print(response.text)
            
            # XML 파싱 시도
            try:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.text)
                print(f"\n[XML 파싱 결과]")
                print(f"루트 태그: {root.tag}")
                for child in root:
                    print(f"  - {child.tag}: {child.text}")
            except:
                pass
        
    except requests.exceptions.RequestException as e:
        print(f"\n[X] 네트워크 오류: {str(e)}")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\n[X] 예상치 못한 오류: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # 다른 엔드포인트 시도
    print(f"\n[4. 대체 엔드포인트 테스트]")
    print("-" * 70)
    
    alternative_endpoints = [
        f"/{service_name}/ParkingInfoService/getParkingInfoList",
        f"/{service_name}/ParkingInfoService/getParkingInfoNearby",
        f"/{service_name}/ParkingInfoService/getParkingInfoByLocation",
    ]
    
    for alt_endpoint in alternative_endpoints:
        print(f"\n테스트: {alt_endpoint}")
        alt_url = f"{base_url}{alt_endpoint}"
        try:
            alt_response = requests.get(alt_url, params=params, timeout=5)
            print(f"  상태 코드: {alt_response.status_code}")
            if alt_response.status_code == 200:
                print(f"  [OK] 이 엔드포인트가 작동합니다!")
                print(f"  응답 (처음 200자): {alt_response.text[:200]}")
                break
        except:
            print(f"  [X] 호출 실패")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_public_data_api()

