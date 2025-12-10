"""
공공데이터포털 다양한 서비스 코드 테스트
"""

import sys
import os
import requests
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_different_services():
    """다양한 서비스 코드 테스트"""
    print("=" * 70)
    print("공공데이터포털 다양한 서비스 코드 테스트")
    print("=" * 70)
    
    api_key = os.getenv("PUBLIC_DATA_API_KEY")
    base_url = "http://apis.data.go.kr"
    
    # 다양한 서비스 코드 시도
    service_codes = [
        "B552895",  # 현재 사용 중
        "1613000",  # 일반적인 공공데이터 서비스 코드 형식
        "15000000",  # 다른 형식
    ]
    
    endpoints = [
        "/ParkingInfoService/getParkingInfo",
        "/ParkingInfoService/getParkingInfoList",
        "/getParkingInfo",
        "/getParkingInfoList",
    ]
    
    # 간단한 파라미터로 테스트
    simple_params = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows": 5,
    }
    
    for service_code in service_codes:
        print(f"\n[서비스 코드: {service_code}]")
        print("-" * 70)
        
        for endpoint in endpoints:
            full_endpoint = f"/{service_code}{endpoint}"
            url = base_url + full_endpoint
            
            try:
                response = requests.get(url, params=simple_params, timeout=5)
                
                if response.status_code == 200:
                    print(f"[OK] {full_endpoint} - 성공!")
                    print(f"응답 (처음 200자): {response.text[:200]}")
                    
                    # XML 파싱
                    try:
                        import xml.etree.ElementTree as ET
                        root = ET.fromstring(response.text)
                        result_code = root.find(".//resultCode")
                        if result_code is not None:
                            print(f"결과 코드: {result_code.text}")
                    except:
                        pass
                    break
                elif response.status_code == 404:
                    print(f"[404] {full_endpoint} - 엔드포인트 없음")
                elif response.status_code == 500:
                    print(f"[500] {full_endpoint} - 서버 에러")
                else:
                    print(f"[{response.status_code}] {full_endpoint} - {response.text[:100]}")
            except Exception as e:
                print(f"[X] {full_endpoint} - 예외: {str(e)[:50]}")
    
    # 공공데이터포털에서 실제 제공하는 API 확인
    print(f"\n[추가 정보]")
    print("-" * 70)
    print("공공데이터포털(data.go.kr)에서 제공하는 주차장 정보 API는")
    print("다양한 기관에서 제공할 수 있으며, 각각 다른 서비스 코드를 사용합니다.")
    print("\n확인 방법:")
    print("1. https://www.data.go.kr 접속")
    print("2. '주차장' 검색")
    print("3. 원하는 API 선택 후 서비스 코드 확인")
    print("4. 해당 API의 실제 엔드포인트와 파라미터 확인")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_different_services()

