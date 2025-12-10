"""
실제 API 호출 테스트
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_kakao_api():
    """카카오 로컬 API 테스트"""
    print("=" * 50)
    print("카카오 로컬 API 테스트")
    print("=" * 50)
    
    try:
        from api_clients import KakaoLocalClient
        client = KakaoLocalClient()
        
        # 주소 -> 좌표 변환 테스트
        print("\n[테스트 1] 주소 -> 좌표 변환")
        print("주소: '서울시청'")
        response = client.address_to_coordinates("서울시청")
        
        if response.get("status") == "success":
            data = response.get("data", {})
            documents = data.get("documents", [])
            if documents:
                doc = documents[0]
                print(f"[OK] 위도: {doc.get('y')}, 경도: {doc.get('x')}")
                print(f"[OK] 주소: {doc.get('address', {}).get('address_name', '')}")
                return doc.get('y'), doc.get('x')
            else:
                print("[X] 결과를 찾을 수 없습니다.")
        else:
            print(f"[X] API 호출 실패: {response}")
            
    except Exception as e:
        print(f"[X] 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return None, None

def test_kakao_parking_search(lat, lng):
    """카카오 주차장 검색 테스트"""
    if not lat or not lng:
        print("\n[테스트 2] 주차장 검색 - 좌표 없음으로 스킵")
        return
    
    print("\n[테스트 2] 주변 주차장 검색")
    print(f"위치: 위도 {lat}, 경도 {lng}")
    
    try:
        from api_clients import KakaoLocalClient
        client = KakaoLocalClient()
        
        response = client.search_parking_nearby(
            latitude=float(lat),
            longitude=float(lng),
            radius=1000
        )
        
        if response.get("status") == "success":
            data = response.get("data", {})
            documents = data.get("documents", [])
            print(f"[OK] 주변 주차장 {len(documents)}개 발견")
            
            for i, doc in enumerate(documents[:3], 1):  # 최대 3개만 출력
                print(f"\n  {i}. {doc.get('place_name', '')}")
                print(f"     주소: {doc.get('address_name', '')}")
                print(f"     거리: {doc.get('distance', '')}m")
        else:
            print(f"[X] API 호출 실패: {response}")
            
    except Exception as e:
        print(f"[X] 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    lat, lng = test_kakao_api()
    test_kakao_parking_search(lat, lng)
    print("\n" + "=" * 50)


