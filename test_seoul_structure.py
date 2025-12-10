"""
서울 API 응답 구조 상세 확인
"""

import sys
import os
import requests
import json
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_seoul_structure():
    """서울 API 응답 구조 상세 확인"""
    api_key = os.getenv("SEOUL_DATA_API_KEY")
    base_url = "http://openapi.seoul.go.kr:8088"
    endpoint = f"/{api_key}/json/GetParkingInfo/1/5"
    url = base_url + endpoint
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        print("=" * 70)
        print("서울 API 응답 구조")
        print("=" * 70)
        
        parking_info = data.get("GetParkingInfo", {})
        print(f"\n[GetParkingInfo 키] {list(parking_info.keys())}")
        
        row = parking_info.get("row", [])
        print(f"\n[주차장 개수] {len(row)}개")
        
        if row:
            first = row[0]
            print(f"\n[첫 번째 주차장 필드]")
            for key, value in first.items():
                print(f"  {key}: {value}")
            
            print(f"\n[주요 필드 매핑]")
            print(f"  주차장명: PKLT_NM = {first.get('PKLT_NM')}")
            print(f"  주소: ADDR = {first.get('ADDR')}")
            print(f"  총 주차 대수: TPKCT = {first.get('TPKCT')}")
            print(f"  현재 주차 대수: NOW_PRK_VHCL_CNT = {first.get('NOW_PRK_VHCL_CNT')}")
            print(f"  주차 가능 대수: {first.get('TPKCT', 0) - first.get('NOW_PRK_VHCL_CNT', 0)}")
            
    except Exception as e:
        print(f"오류: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_seoul_structure()

