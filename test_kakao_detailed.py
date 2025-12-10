"""
카카오 API 상세 테스트 (에러 디버깅)
"""

import sys
import os
import requests
sys.path.insert(0, 'src')

from dotenv import load_dotenv

load_dotenv()

def test_kakao_api_directly():
    """카카오 API를 직접 호출하여 상세 정보 확인"""
    print("=" * 60)
    print("카카오 API 직접 호출 테스트")
    print("=" * 60)
    
    api_key = os.getenv("KAKAO_REST_API_KEY")
    test_address = "서울시 중구 세종대로 110"
    
    print(f"\n[API 키 확인]")
    if api_key:
        print(f"[OK] API 키 존재: {api_key[:10]}...{api_key[-4:]}")
    else:
        print("[X] API 키가 없습니다!")
        return
    
    print(f"\n[테스트 주소] {test_address}")
    print("-" * 60)
    
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {
        "Authorization": f"KakaoAK {api_key}"
    }
    params = {
        "query": test_address
    }
    
    print(f"\n[요청 정보]")
    print(f"URL: {url}")
    print(f"Headers: Authorization: KakaoAK {api_key[:10]}...")
    print(f"Params: query={test_address}")
    print("-" * 60)
    
    try:
        print(f"\n[API 호출 중...]")
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        print(f"\n[응답 정보]")
        print(f"상태 코드: {response.status_code}")
        print(f"응답 헤더: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n[성공] API 호출 성공!")
            print(f"응답 데이터: {data}")
            
            documents = data.get("documents", [])
            if documents:
                print(f"\n[결과] {len(documents)}개의 결과를 찾았습니다.")
                for i, doc in enumerate(documents, 1):
                    print(f"\n--- 결과 {i} ---")
                    print(f"주소명: {doc.get('address_name', 'N/A')}")
                    print(f"위도: {doc.get('y', 'N/A')}")
                    print(f"경도: {doc.get('x', 'N/A')}")
            else:
                print("\n[결과] 검색 결과가 없습니다.")
        else:
            print(f"\n[에러] HTTP {response.status_code}")
            print(f"응답 본문: {response.text}")
            
            if response.status_code == 401:
                print("\n[원인 분석] 인증 실패")
                print("- API 키가 잘못되었거나 만료되었습니다.")
                print("- Authorization 헤더 형식을 확인하세요.")
            elif response.status_code == 403:
                print("\n[원인 분석] 접근 거부")
                print("- API 키는 유효하지만 권한이 없습니다.")
                print("- 카카오 개발자 콘솔에서 '로컬 API' 서비스를 활성화해야 합니다.")
                print("- https://developers.kakao.com/console/app 에서 확인하세요.")
            elif response.status_code == 400:
                print("\n[원인 분석] 잘못된 요청")
                print("- 요청 파라미터를 확인하세요.")
            
    except requests.exceptions.RequestException as e:
        print(f"\n[X] 네트워크 오류: {str(e)}")
    except Exception as e:
        print(f"\n[X] 예상치 못한 오류: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n" + "=" * 60)

if __name__ == "__main__":
    test_kakao_api_directly()


