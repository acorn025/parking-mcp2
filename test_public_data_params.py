"""
공공데이터포털 API 파라미터 테스트
다양한 파라미터 조합으로 테스트
"""

import sys
import os
import requests
from urllib.parse import quote
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_various_params():
    """다양한 파라미터 조합 테스트"""
    print("=" * 70)
    print("공공데이터포털 API 파라미터 테스트")
    print("=" * 70)
    
    api_key = os.getenv("PUBLIC_DATA_API_KEY")
    base_url = "http://apis.data.go.kr"
    service_name = "B552895"
    
    # 테스트 1: 기본 파라미터 (현재 사용 중)
    print("\n[테스트 1] 현재 사용 중인 파라미터")
    print("-" * 70)
    endpoint1 = f"/{service_name}/ParkingInfoService/getParkingInfo"
    params1 = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows": 10,
        "lat": 37.566370776634,
        "lng": 126.977918351844,
        "radius": 1000,
    }
    test_request(base_url + endpoint1, params1, "테스트 1")
    
    # 테스트 2: serviceKey를 URL 인코딩
    print("\n[테스트 2] serviceKey URL 인코딩")
    print("-" * 70)
    params2 = {
        "serviceKey": quote(api_key, safe=''),
        "pageNo": 1,
        "numOfRows": 10,
        "lat": 37.566370776634,
        "lng": 126.977918351844,
        "radius": 1000,
    }
    test_request(base_url + endpoint1, params2, "테스트 2")
    
    # 테스트 3: 파라미터 이름 변경 (latitude, longitude)
    print("\n[테스트 3] 파라미터 이름 변경 (latitude, longitude)")
    print("-" * 70)
    params3 = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows": 10,
        "latitude": 37.566370776634,
        "longitude": 126.977918351844,
        "radius": 1000,
    }
    test_request(base_url + endpoint1, params3, "테스트 3")
    
    # 테스트 4: 필수 파라미터만 (좌표 제외)
    print("\n[테스트 4] 필수 파라미터만 (좌표 제외)")
    print("-" * 70)
    params4 = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows": 10,
    }
    test_request(base_url + endpoint1, params4, "테스트 4")
    
    # 테스트 5: 다른 엔드포인트 (getParkingInfoList)
    print("\n[테스트 5] 다른 엔드포인트 (getParkingInfoList)")
    print("-" * 70)
    endpoint5 = f"/{service_name}/ParkingInfoService/getParkingInfoList"
    params5 = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows": 10,
    }
    test_request(base_url + endpoint5, params5, "테스트 5")
    
    # 테스트 6: 좌표를 문자열로 변환
    print("\n[테스트 6] 좌표를 문자열로 변환")
    print("-" * 70)
    params6 = {
        "serviceKey": api_key,
        "pageNo": "1",
        "numOfRows": "10",
        "lat": "37.566370776634",
        "lng": "126.977918351844",
        "radius": "1000",
    }
    test_request(base_url + endpoint1, params6, "테스트 6")
    
    # 테스트 7: 반경 단위 변경 (미터 -> 킬로미터)
    print("\n[테스트 7] 반경 단위 변경 (미터 -> 킬로미터)")
    print("-" * 70)
    params7 = {
        "serviceKey": api_key,
        "pageNo": 1,
        "numOfRows": 10,
        "lat": 37.566370776634,
        "lng": 126.977918351844,
        "radius": 1,  # 1km
    }
    test_request(base_url + endpoint1, params7, "테스트 7")
    
    print("\n" + "=" * 70)
    print("모든 테스트 완료")
    print("=" * 70)

def test_request(url, params, test_name):
    """단일 API 요청 테스트"""
    try:
        response = requests.get(url, params=params, timeout=10)
        
        print(f"상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            print(f"[OK] {test_name} 성공!")
            print(f"응답 (처음 300자): {response.text[:300]}")
            
            # XML 파싱 시도
            try:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.text)
                print(f"XML 루트 태그: {root.tag}")
                
                # 에러 체크
                result_code = root.find(".//resultCode")
                result_msg = root.find(".//resultMsg")
                if result_code is not None:
                    code = result_code.text
                    msg = result_msg.text if result_msg is not None else ""
                    print(f"결과 코드: {code}")
                    if msg:
                        print(f"결과 메시지: {msg}")
                    
                    if code != "00":
                        print(f"[경고] API 에러 코드: {code}")
            except:
                pass
        else:
            print(f"[X] {test_name} 실패")
            print(f"응답: {response.text[:200]}")
            
    except Exception as e:
        print(f"[X] {test_name} 예외 발생: {str(e)}")

if __name__ == "__main__":
    test_various_params()

