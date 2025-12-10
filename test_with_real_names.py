"""
실제 서울/경기 API 주차장명으로 테스트
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_seoul_with_real_name():
    """서울 API에서 실제 주차장명 가져와서 테스트"""
    print("=" * 80)
    print("서울 지역 테스트 (실제 주차장명 사용)")
    print("=" * 80)
    
    try:
        from api_clients import SeoulDataClient, KakaoLocalClient
        from src.server import _get_realtime_info_seoul, _format_parking_info
        
        # 서울 API에서 실제 주차장명 가져오기
        seoul_client = SeoulDataClient()
        seoul_response = seoul_client.get_realtime_parking_info(1, 10)
        
        if seoul_response.get("status") != "success":
            print("[X] 서울 API 호출 실패")
            return
        
        seoul_data = seoul_response.get("data", {})
        seoul_parkings = seoul_data.get("GetParkingInfo", {}).get("row", [])
        
        if not seoul_parkings:
            print("[X] 서울 주차장 데이터 없음")
            return
        
        # 첫 번째 주차장 정보
        real_parking = seoul_parkings[0]
        parking_name = real_parking.get("PKLT_NM", "")
        parking_addr = real_parking.get("ADDR", "")
        
        print(f"\n[서울 API 주차장]")
        print(f"이름: {parking_name}")
        print(f"주소: {parking_addr}")
        print(f"총 주차 대수: {real_parking.get('TPKCT', 'N/A')}")
        print(f"현재 주차 대수: {real_parking.get('NOW_PRK_VHCL_CNT', 'N/A')}")
        print("-" * 80)
        
        # 실시간 정보 조회 테스트
        print(f"\n[실시간 정보 조회 테스트]")
        realtime_info = _get_realtime_info_seoul(parking_name, parking_addr)
        
        if realtime_info:
            print(f"[OK] 실시간 정보 조회 성공!\n")
            
            standard_parking = {
                "name": parking_name,
                "address": parking_addr,
                "total_spots": None,
                "fee": "",
                "distance": 0,
            }
            
            formatted = _format_parking_info(standard_parking, "seoul", realtime_info)
            
            print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"주차장: {formatted.get('name')}")
            print(f"주소: {formatted.get('address')}")
            print(f"\n[실시간 정보]")
            print(f"  총 주차 대수: {formatted.get('total_spots')}대")
            print(f"  주차 가능 대수: {formatted.get('available_spots')}대")
            
            if formatted.get('operating_info'):
                op = formatted.get('operating_info')
                print(f"\n[운영 시간]")
                print(f"  운영 구분: {op.get('operating_type', 'N/A')}")
                print(f"  평일: {op.get('weekday_start', 'N/A')} ~ {op.get('weekday_end', 'N/A')}")
                print(f"  주말: {op.get('weekend_start', 'N/A')} ~ {op.get('weekend_end', 'N/A')}")
                print(f"  공휴일: {op.get('holiday_start', 'N/A')} ~ {op.get('holiday_end', 'N/A')}")
            
            if formatted.get('fee_info'):
                fee = formatted.get('fee_info')
                print(f"\n[요금 정보]")
                print(f"  유료 여부: {fee.get('is_paid', 'N/A')}")
                print(f"  기본 요금: {fee.get('basic_fee', 0)}원 / {fee.get('basic_hours', 0)}분")
                print(f"  추가 요금: {fee.get('additional_fee', 0)}원 / {fee.get('additional_hours', 0)}분")
                if fee.get('daily_max_fee'):
                    print(f"  일일 최대 요금: {fee.get('daily_max_fee')}원")
        else:
            print(f"[X] 실시간 정보 조회 실패")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n[X] 오류: {str(e)}")
        import traceback
        traceback.print_exc()

def test_gyeonggi_with_real_name():
    """경기 API에서 실제 주차장명 가져와서 테스트"""
    print("\n" + "=" * 80)
    print("경기 지역 테스트 (실제 주차장명 사용)")
    print("=" * 80)
    
    try:
        from api_clients import GyeonggiDataClient
        from src.server import _get_realtime_info_gyeonggi, _format_parking_info
        
        # 경기 API에서 실제 주차장명 가져오기
        gyeonggi_client = GyeonggiDataClient()
        gyeonggi_response = gyeonggi_client.get_realtime_parking_info(1, 10)
        
        if gyeonggi_response.get("status") != "success":
            print("[X] 경기 API 호출 실패")
            return
        
        gyeonggi_data = gyeonggi_response.get("data", {})
        gyeonggi_place = gyeonggi_data.get("ParkingPlace", [])
        
        if isinstance(gyeonggi_place, list) and len(gyeonggi_place) > 1:
            gyeonggi_parkings = gyeonggi_place[1].get("row", [])
        else:
            gyeonggi_parkings = []
        
        if not gyeonggi_parkings:
            print("[X] 경기 주차장 데이터 없음")
            return
        
        # 첫 번째 주차장 정보
        real_parking = gyeonggi_parkings[0]
        parking_name = real_parking.get("PARKPLC_NM", "")
        parking_addr = real_parking.get("LOCPLC_ROADNM_ADDR", "") or real_parking.get("LOCPLC_LOTNO_ADDR", "")
        
        print(f"\n[경기 API 주차장]")
        print(f"이름: {parking_name}")
        print(f"주소: {parking_addr}")
        print(f"총 주차 대수: {real_parking.get('PARKNG_COMPRT_PLANE_CNT', 'N/A')}")
        print("-" * 80)
        
        # 정보 조회 테스트
        print(f"\n[요금 및 운영시간 정보 조회 테스트]")
        realtime_info = _get_realtime_info_gyeonggi(parking_name, parking_addr)
        
        if realtime_info:
            print(f"[OK] 정보 조회 성공!\n")
            
            standard_parking = {
                "name": parking_name,
                "address": parking_addr,
                "total_spots": None,
                "fee": "",
                "distance": 0,
            }
            
            formatted = _format_parking_info(standard_parking, "gyeonggi", realtime_info)
            
            print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"주차장: {formatted.get('name')}")
            print(f"주소: {formatted.get('address')}")
            
            if formatted.get('total_spots'):
                print(f"\n[주차장 정보]")
                print(f"  총 주차 대수: {formatted.get('total_spots')}대")
            
            if formatted.get('operating_info'):
                op = formatted.get('operating_info')
                print(f"\n[운영 시간]")
                print(f"  평일: {op.get('weekday_start', 'N/A')} ~ {op.get('weekday_end', 'N/A')}")
                print(f"  토요일: {op.get('saturday_start', 'N/A')} ~ {op.get('saturday_end', 'N/A')}")
                print(f"  공휴일: {op.get('holiday_start', 'N/A')} ~ {op.get('holiday_end', 'N/A')}")
            
            if formatted.get('fee_info'):
                fee = formatted.get('fee_info')
                print(f"\n[요금 정보]")
                print(f"  유료 여부: {fee.get('is_paid', 'N/A')}")
                print(f"  기본 요금: {fee.get('basic_fee', 0)}원 / {fee.get('basic_time', 0)}분")
                print(f"  추가 요금: {fee.get('additional_fee', 0)}원 / {fee.get('additional_time', 0)}분")
                if fee.get('payment_method'):
                    print(f"  결제 방법: {fee.get('payment_method')}")
        else:
            print(f"[X] 정보 조회 실패")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n[X] 오류: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_seoul_with_real_name()
    test_gyeonggi_with_real_name()

