"""
경기 API 새 엔드포인트 테스트
"""

import sys
import os
import requests
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_gyeonggi_new():
    """경기 API 새 엔드포인트 테스트"""
    print("=" * 70)
    print("경기 API 새 엔드포인트 테스트")
    print("=" * 70)
    
    api_key = "bd5042fb07784ab0abb07a021a4488d5"
    base_url = "https://openapi.gg.go.kr"
    endpoint = "/ParkingPlace"
    url = base_url + endpoint
    params = {
        "KEY": api_key,
        "Type": "json",
        "pIndex": 1,
        "pSize": 5,
    }
    
    print(f"\n[요청 정보]")
    print(f"URL: {url}")
    print(f"Params: {params}")
    print("-" * 70)
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n[응답 구조]")
            print(f"키: {list(data.keys())}")
            
            result = data.get("RESULT", {})
            if result.get("CODE") == "INFO-000":
                print(f"[OK] API 호출 성공!")
                
                parking_place = data.get("ParkingPlace", {})
                if parking_place:
                    print(f"\n[ParkingPlace 구조]")
                    print(f"키: {list(parking_place.keys())}")
                    
                    row = parking_place.get("row", [])
                    if row and len(row) > 0:
                        print(f"\n[주차장 개수] {len(row)}개")
                        print(f"\n[첫 번째 주차장 필드]")
                        first = row[0]
                        
                        # 모든 필드 출력
                        for key, value in first.items():
                            if value and value != "":
                                print(f"  {key}: {value}")
                        
                        # 운영정보 및 요금정보 필드 확인
                        print(f"\n[운영정보 필드 확인]")
                        operating_fields = [k for k in first.keys() if any(x in k.upper() for x in ['OPER', 'TIME', 'OPEN', 'CLOSE', '운영', '시간'])]
                        for field in operating_fields:
                            print(f"  {field}: {first.get(field, 'N/A')}")
                        
                        print(f"\n[요금정보 필드 확인]")
                        fee_fields = [k for k in first.keys() if any(x in k.upper() for x in ['FEE', 'CHARGE', 'CRG', 'PAY', '요금', '비용'])]
                        for field in fee_fields:
                            print(f"  {field}: {first.get(field, 'N/A')}")
                    else:
                        print("[경고] row 데이터가 없습니다.")
                else:
                    print("[경고] ParkingPlace 데이터가 없습니다.")
            else:
                print(f"[에러] {result.get('MESSAGE', 'N/A')}")
                print(f"응답: {response.text[:500]}")
        else:
            print(f"[에러] HTTP {response.status_code}")
            print(f"응답: {response.text[:500]}")
            
    except Exception as e:
        print(f"\n[X] 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gyeonggi_new()

