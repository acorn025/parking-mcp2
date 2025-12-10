"""
서울/경기 API 실제 응답 형식 확인 테스트
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_seoul_api():
    """서울 API 응답 형식 확인"""
    print("=" * 70)
    print("서울 열린데이터 API 응답 형식 확인")
    print("=" * 70)
    
    try:
        from api_clients import SeoulDataClient
        client = SeoulDataClient()
        
        print("\n[API 호출 중...]")
        response = client.get_realtime_parking_info(
            start_index=1,
            end_index=10  # 처음 10개만
        )
        
        print(f"\n[응답 상태] {response.get('status')}")
        
        if response.get("status") == "success":
            data = response.get("data", {})
            
            print(f"\n[응답 데이터 타입] {type(data)}")
            print(f"[응답 데이터 키] {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
            
            # JSON 응답인 경우
            if isinstance(data, dict):
                print(f"\n[응답 구조]")
                print(f"전체 데이터 (처음 500자):")
                import json
                print(json.dumps(data, ensure_ascii=False, indent=2)[:500])
                
                # GetParkingInfo 확인
                parking_info = data.get("GetParkingInfo", {})
                if parking_info:
                    print(f"\n[GetParkingInfo 구조]")
                    print(f"키: {list(parking_info.keys())}")
                    
                    row = parking_info.get("row", [])
                    if row and len(row) > 0:
                        print(f"\n[첫 번째 주차장 데이터]")
                        first_parking = row[0]
                        print(f"키: {list(first_parking.keys())}")
                        print(f"데이터:")
                        for key, value in list(first_parking.items())[:10]:
                            print(f"  {key}: {value}")
            else:
                print(f"\n[응답 내용] {str(data)[:500]}")
        else:
            print(f"[X] API 호출 실패: {response}")
            
    except Exception as e:
        print(f"\n[X] 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

def test_gyeonggi_api():
    """경기 API 응답 형식 확인"""
    print("\n" + "=" * 70)
    print("경기데이터드림 API 응답 형식 확인")
    print("=" * 70)
    
    try:
        from api_clients import GyeonggiDataClient
        client = GyeonggiDataClient()
        
        print("\n[API 호출 중...]")
        response = client.get_realtime_parking_info(
            page=1,
            size=10  # 처음 10개만
        )
        
        print(f"\n[응답 상태] {response.get('status')}")
        
        if response.get("status") == "success":
            data = response.get("data", {})
            
            print(f"\n[응답 데이터 타입] {type(data)}")
            print(f"[응답 데이터 키] {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
            
            # JSON 응답인 경우
            if isinstance(data, dict):
                print(f"\n[응답 구조]")
                print(f"전체 데이터 (처음 500자):")
                import json
                print(json.dumps(data, ensure_ascii=False, indent=2)[:500])
                
                # Parking 확인
                parking_info = data.get("Parking", {})
                if parking_info:
                    print(f"\n[Parking 구조]")
                    print(f"키: {list(parking_info.keys())}")
                    
                    row = parking_info.get("row", [])
                    if row and len(row) > 0:
                        print(f"\n[첫 번째 주차장 데이터]")
                        first_parking = row[0]
                        print(f"키: {list(first_parking.keys())}")
                        print(f"데이터:")
                        for key, value in list(first_parking.items())[:10]:
                            print(f"  {key}: {value}")
            else:
                print(f"\n[응답 내용] {str(data)[:500]}")
        else:
            print(f"[X] API 호출 실패: {response}")
            
    except Exception as e:
        print(f"\n[X] 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_seoul_api()
    test_gyeonggi_api()
    print("\n" + "=" * 70)

