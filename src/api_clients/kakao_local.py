"""
카카오 로컬 API 클라이언트
주소 → 좌표 변환 및 장소 검색
"""

import os
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class KakaoLocalClient:
    """카카오 로컬 API 클라이언트"""
    
    BASE_URL = "https://dapi.kakao.com"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Args:
            api_key: 카카오 REST API 키 (없으면 환경변수에서 로드)
        """
        self.api_key = api_key or os.getenv("KAKAO_REST_API_KEY")
        if not self.api_key:
            raise ValueError(
                "KAKAO_REST_API_KEY가 설정되지 않았습니다. "
                ".env 파일에 KAKAO_REST_API_KEY를 추가하세요."
            )
        self.headers = {
            "Authorization": f"KakaoAK {self.api_key}"
        }
    
    def _make_request(
        self,
        endpoint: str,
        params: Dict,
        timeout: int = 10
    ) -> Dict:
        """
        API 요청 실행 (에러 핸들링 포함)
        
        Args:
            endpoint: API 엔드포인트
            params: 요청 파라미터
            timeout: 타임아웃 (초)
        
        Returns:
            API 응답 데이터
        
        Raises:
            ValueError: API 키가 없거나 잘못된 경우
            requests.exceptions.RequestException: HTTP 에러
            TimeoutError: 타임아웃 발생
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=timeout
            )
            response.raise_for_status()
            
            # 빈 응답 체크
            if not response.content:
                raise ValueError("API 응답이 비어있습니다.")
            
            # JSON 응답 파싱
            data = response.json()
            
            # 카카오 API 에러 체크
            if isinstance(data, dict) and "error" in data:
                error = data["error"]
                error_type = error.get("error_type", "Unknown")
                error_msg = error.get("message", "알 수 없는 오류")
                raise ValueError(f"카카오 API 오류 ({error_type}): {error_msg}")
            
            return {"status": "success", "data": data}
            
        except requests.exceptions.Timeout:
            raise TimeoutError(f"API 요청 타임아웃 (>{timeout}초)")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise ValueError("API 키가 유효하지 않습니다.")
            elif e.response.status_code == 403:
                raise ValueError("API 접근이 거부되었습니다. API 키 권한을 확인하세요.")
            elif e.response.status_code == 404:
                raise ValueError("요청한 API 엔드포인트를 찾을 수 없습니다.")
            elif e.response.status_code == 429:
                raise ValueError("API 호출 한도를 초과했습니다. 잠시 후 다시 시도하세요.")
            elif 400 <= e.response.status_code < 500:
                raise ValueError(f"클라이언트 에러 ({e.response.status_code}): {e.response.text}")
            elif 500 <= e.response.status_code < 600:
                raise ConnectionError(f"서버 에러 ({e.response.status_code}): 서버에 문제가 있습니다.")
            else:
                raise ConnectionError(f"HTTP 에러 ({e.response.status_code}): {e.response.text}")
        except requests.exceptions.ConnectionError:
            raise ConnectionError("API 서버에 연결할 수 없습니다. 네트워크를 확인하세요.")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API 요청 중 오류 발생: {str(e)}")
        except ValueError as e:
            # JSON 파싱 에러 등
            raise ValueError(f"응답 파싱 오류: {str(e)}")
    
    def address_to_coordinates(
        self,
        address: str
    ) -> Dict:
        """
        주소를 좌표로 변환
        
        Args:
            address: 검색할 주소
        
        Returns:
            좌표 정보 (위도, 경도)
        """
        endpoint = "/v2/local/search/address.json"
        params = {
            "query": address,
        }
        
        return self._make_request(endpoint, params)
    
    def search_place(
        self,
        query: str,
        category_group_code: Optional[str] = None,
        x: Optional[float] = None,
        y: Optional[float] = None,
        radius: Optional[int] = None,
        page: int = 1,
        size: int = 15
    ) -> Dict:
        """
        장소 검색
        
        Args:
            query: 검색어
            category_group_code: 카테고리 그룹 코드 (예: "PK6" - 주차장)
            x: 경도 (중심 좌표)
            y: 위도 (중심 좌표)
            radius: 반경 (미터 단위, 0~20000)
            page: 페이지 번호
            size: 페이지당 결과 수 (1~15)
        
        Returns:
            장소 검색 결과
        """
        endpoint = "/v2/local/search/keyword.json"
        params = {
            "query": query,
            "page": page,
            "size": size,
        }
        
        if category_group_code:
            params["category_group_code"] = category_group_code
        
        if x is not None and y is not None:
            params["x"] = x
            params["y"] = y
        
        if radius is not None:
            params["radius"] = radius
        
        return self._make_request(endpoint, params)
    
    def search_parking_nearby(
        self,
        latitude: float,
        longitude: float,
        radius: int = 2000,
        page: int = 1,
        size: int = 15
    ) -> Dict:
        """
        주변 주차장 검색 (편의 메서드)
        
        Args:
            latitude: 위도
            longitude: 경도
            radius: 검색 반경 (미터 단위)
            page: 페이지 번호
            size: 페이지당 결과 수
        
        Returns:
            주변 주차장 목록
        """
        return self.search_place(
            query="주차장",
            category_group_code="PK6",
            x=longitude,
            y=latitude,
            radius=radius,
            page=page,
            size=size
        )


