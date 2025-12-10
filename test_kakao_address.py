"""
카카오 API 주소 -> 좌표 변환 테스트
"""

import sys
import os
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_address_to_coordinates():
    """주소를 좌표로 변환하는 테스트"""
    print("=" * 60)
    print("카카오 API 주소 -> 좌표 변환 테스트")
    print("=" * 60)
    
    test_address = "서울시 중구 세종대로 110"
    print(f"\n[테스트 주소] {test_address}")
    print("-" * 60)
    
    try:
        from api_clients import KakaoLocalClient
        client = KakaoLocalClient()
        print("[OK] KakaoLocalClient 초기화 성공")
        
        print(f"\n[API 호출 중...]")
        response = client.address_to_coordinates(test_address)
        
        print(f"\n[응답 상태] {response.get('status')}")
        
        if response.get("status") == "success":
            data = response.get("data", {})
            documents = data.get("documents", [])
            
            if documents:
                print(f"\n[결과] {len(documents)}개의 결과를 찾았습니다.\n")
                
                for i, doc in enumerate(documents, 1):
                    print(f"--- 결과 {i} ---")
                    print(f"주소명: {doc.get('address_name', 'N/A')}")
                    print(f"위도 (y): {doc.get('y', 'N/A')}")
                    print(f"경도 (x): {doc.get('x', 'N/A')}")
                    
                    address = doc.get('address', {})
                    if address:
                        print(f"시도: {address.get('region_1depth_name', 'N/A')}")
                        print(f"시군구: {address.get('region_2depth_name', 'N/A')}")
                        print(f"읍면동: {address.get('region_3depth_name', 'N/A')}")
                        print(f"도로명: {address.get('road_name', 'N/A')}")
                    
                    road_address = doc.get('road_address', {})
                    if road_address:
                        print(f"도로명 주소: {road_address.get('address_name', 'N/A')}")
                    
                    print()
                
                # 첫 번째 결과의 좌표 반환
                first_result = documents[0]
                lat = first_result.get('y')
                lng = first_result.get('x')
                
                if lat and lng:
                    print(f"[최종 좌표]")
                    print(f"위도: {lat}")
                    print(f"경도: {lng}")
                    return lat, lng
                else:
                    print("[X] 좌표 정보를 찾을 수 없습니다.")
                    return None, None
            else:
                print("[X] 검색 결과가 없습니다.")
                print(f"\n[전체 응답 데이터]")
                print(data)
                return None, None
        else:
            print(f"[X] API 호출 실패")
            print(f"응답: {response}")
            return None, None
            
    except ValueError as e:
        print(f"\n[X] 오류 발생: {str(e)}")
        print("\n[가능한 원인]")
        print("1. API 키가 유효하지 않습니다.")
        print("2. 카카오 개발자 콘솔에서 '로컬 API' 서비스가 활성화되지 않았습니다.")
        print("3. API 키의 권한이 부족합니다.")
        return None, None
    except Exception as e:
        print(f"\n[X] 예상치 못한 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None
    
    finally:
        print("\n" + "=" * 60)

if __name__ == "__main__":
    lat, lng = test_address_to_coordinates()
    
    if lat and lng:
        print(f"\n[테스트 성공]")
        print(f"주소 '{test_address}'가 성공적으로 좌표로 변환되었습니다.")
        print(f"위도: {lat}, 경도: {lng}")
    else:
        print(f"\n[테스트 실패]")
        print("좌표 변환에 실패했습니다. 위의 오류 메시지를 확인하세요.")


