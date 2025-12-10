"""
경기 API 응답 구조 상세 확인
"""

import sys
import os
import requests
import json
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_gyeonggi_structure():
    """경기 API 응답 구조 상세 확인"""
    api_key = "bd5042fb07784ab0abb07a021a4488d5"
    base_url = "https://openapi.gg.go.kr"
    endpoint = "/ParkingPlace"
    url = base_url + endpoint
    params = {
        "KEY": api_key,
        "Type": "json",
        "pIndex": 1,
        "pSize": 3,
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        print("=" * 70)
        print("경기 API 응답 구조 상세 확인")
        print("=" * 70)
        
        parking_place = data.get("ParkingPlace", [])
        
        if isinstance(parking_place, list) and len(parking_place) > 1:
            row_data = parking_place[1].get("row", [])
            
            if row_data:
                first = row_data[0]
                
                print(f"\n[주차장 정보]")
                print(f"이름: {first.get('PARKPLC_NM', 'N/A')}")
                print(f"주소: {first.get('LOCPLC_ROADNM_ADDR', 'N/A')}")
                
                print(f"\n[전체 필드 목록]")
                for key, value in first.items():
                    if value and value != "":
                        print(f"  {key}: {value}")
                
                print(f"\n[운영정보 필드]")
                operating_fields = {
                    "WKDAY_OPERT_BEGIN_TM": "평일 운영 시작",
                    "WKDAY_OPERT_END_TM": "평일 운영 종료",
                    "SAT_OPERT_BEGIN_TM": "토요일 운영 시작",
                    "SAT_OPERT_END_TM": "토요일 운영 종료",
                    "HOLIDAY_OPERT_BEGIN_TM": "공휴일 운영 시작",
                    "HOLIDAY_OPERT_END_TM": "공휴일 운영 종료",
                }
                for field, desc in operating_fields.items():
                    print(f"  {desc} ({field}): {first.get(field, 'N/A')}")
                
                print(f"\n[요금정보 필드]")
                fee_fields = {
                    "PAY_NM": "요금제",
                    "UNPAY_NM": "무료",
                    "WKDAY_PAY_NM": "평일 요금",
                    "SAT_PAY_NM": "토요일 요금",
                    "HOLIDAY_PAY_NM": "공휴일 요금",
                    "FULLTIME_MONTHLY_PAY_NM": "월정기 요금",
                    "GRP_PARKNG_FEE": "단체 주차 요금",
                }
                for field, desc in fee_fields.items():
                    value = first.get(field, 'N/A')
                    if value and value != "":
                        print(f"  {desc} ({field}): {value}")
                
                print(f"\n[기타 정보]")
                print(f"  총 주차 대수: {first.get('PARKNG_COMPRT_PLANE_CNT', 'N/A')}")
                print(f"  주차장 구분: {first.get('PARKPLC_DIV_NM', 'N/A')}")
                print(f"  주차장 유형: {first.get('PARKPLC_TYPE', 'N/A')}")
                
    except Exception as e:
        print(f"오류: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gyeonggi_structure()

