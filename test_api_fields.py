"""
서울/경기 API 필드 상세 확인
운영정보 및 요금 정보 확인
"""

import sys
import os
import requests
import json
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_seoul_fields():
    """서울 API 필드 상세 확인"""
    print("=" * 70)
    print("서울 열린데이터 API 필드 확인")
    print("=" * 70)
    
    api_key = os.getenv("SEOUL_DATA_API_KEY")
    base_url = "http://openapi.seoul.go.kr:8088"
    endpoint = f"/{api_key}/json/GetParkingInfo/1/3"
    url = base_url + endpoint
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        parking_info = data.get("GetParkingInfo", {})
        row = parking_info.get("row", [])
        
        if row:
            first = row[0]
            
            print(f"\n[주차장 정보]")
            print(f"이름: {first.get('PKLT_NM')}")
            print(f"주소: {first.get('ADDR')}")
            
            print(f"\n[운영 정보]")
            print(f"운영 상태: {first.get('PRK_STTS_NM', 'N/A')}")
            print(f"운영 구분: {first.get('OPER_SE_NM', 'N/A')}")
            print(f"평일 운영 시작: {first.get('WD_OPER_BGNG_TM', 'N/A')}")
            print(f"평일 운영 종료: {first.get('WD_OPER_END_TM', 'N/A')}")
            print(f"주말 운영 시작: {first.get('WE_OPER_BGNG_TM', 'N/A')}")
            print(f"주말 운영 종료: {first.get('WE_OPER_END_TM', 'N/A')}")
            print(f"공휴일 운영 시작: {first.get('LHLDY_OPER_BGNG_TM', 'N/A')}")
            print(f"공휴일 운영 종료: {first.get('LHLDY_OPER_END_TM', 'N/A')}")
            
            print(f"\n[요금 정보]")
            print(f"유료 여부: {first.get('PAY_YN_NM', 'N/A')}")
            print(f"야간 유료 여부: {first.get('NGHT_PAY_YN_NM', 'N/A')}")
            print(f"기본 주차 요금: {first.get('BSC_PRK_CRG', 'N/A')}원")
            print(f"기본 주차 시간: {first.get('BSC_PRK_HR', 'N/A')}분")
            print(f"추가 주차 요금: {first.get('ADD_PRK_CRG', 'N/A')}원")
            print(f"추가 주차 시간: {first.get('ADD_PRK_HR', 'N/A')}분")
            print(f"일일 최대 요금: {first.get('DAY_MAX_CRG', 'N/A')}원")
            print(f"기간 요금: {first.get('PRD_AMT', 'N/A')}원")
            
            print(f"\n[전체 필드 목록]")
            for key, value in first.items():
                if value and value != "*" and value != "":
                    print(f"  {key}: {value}")
                    
    except Exception as e:
        print(f"오류: {str(e)}")
        import traceback
        traceback.print_exc()

def test_gyeonggi_fields():
    """경기 API 필드 상세 확인"""
    print("\n" + "=" * 70)
    print("경기데이터드림 API 필드 확인")
    print("=" * 70)
    
    api_key = os.getenv("GYEONGGI_DATA_API_KEY")
    base_url = "https://openapi.gg.go.kr"
    endpoint = "/Parking"
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
        
        print(f"\n[응답 구조]")
        print(f"키: {list(data.keys())}")
        
        result = data.get("RESULT", {})
        if result.get("CODE") != "INFO-000":
            print(f"\n[에러] {result.get('MESSAGE', 'N/A')}")
            print(f"서비스를 찾을 수 없습니다. 다른 엔드포인트를 시도합니다...")
            
            # 다른 엔드포인트 시도
            alternative_endpoints = [
                "/ParkingLot",
                "/ParkingInfo",
                "/ParkingFacility",
            ]
            
            for alt_endpoint in alternative_endpoints:
                alt_url = base_url + alt_endpoint
                alt_response = requests.get(alt_url, params=params, timeout=5)
                alt_data = alt_response.json()
                alt_result = alt_data.get("RESULT", {})
                
                if alt_result.get("CODE") == "INFO-000":
                    print(f"\n[성공] {alt_endpoint} 엔드포인트가 작동합니다!")
                    data = alt_data
                    break
                else:
                    print(f"[실패] {alt_endpoint}: {alt_result.get('MESSAGE', 'N/A')}")
        else:
            parking = data.get("Parking", {})
            if parking:
                row = parking.get("row", [])
                if row:
                    first = row[0]
                    print(f"\n[주차장 정보]")
                    print(f"전체 필드:")
                    for key, value in first.items():
                        if value:
                            print(f"  {key}: {value}")
                            
    except Exception as e:
        print(f"오류: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_seoul_fields()
    test_gyeonggi_fields()
    print("\n" + "=" * 70)

