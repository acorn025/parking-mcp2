"""
공공데이터포털 API 클라이언트
전국 공영주차장 기본 정보 조회
"""

import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


class PublicDataClient:
    """공공데이터포털 주차장 정보 API 클라이언트"""
    
    BASE_URL = "http://apis.data.go.kr"
    SERVICE_NAME = "B552895"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Args:
            api_key: 공공데이터포털 API 키 (없으면 환경변수에서 로드)
        """
        self.api_key = api_key or os.getenv("PUBLIC_DATA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "PUBLIC_DATA_API_KEY가 설정되지 않았습니다. "
                ".env 파일에 PUBLIC_DATA_API_KEY를 추가하세요."
            )
    
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
        params["serviceKey"] = self.api_key
        
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            
            # 빈 응답 체크
            if not response.content:
                raise ValueError("API 응답이 비어있습니다.")
            
            # XML 응답 파싱 (일반적으로 공공데이터포털은 XML 사용)
            # 실제 구현 시 xml.etree.ElementTree 또는 lxml 사용
            return {"status": "success", "data": response.text}
            
        except requests.exceptions.Timeout:
            raise TimeoutError(f"API 요청 타임아웃 (>{timeout}초)")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise ValueError("API 키가 유효하지 않습니다.")
            elif e.response.status_code == 403:
                raise ValueError("API 접근이 거부되었습니다.")
            elif e.response.status_code == 404:
                raise ValueError("요청한 API 엔드포인트를 찾을 수 없습니다.")
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
    
    def search_nearby_parking(
        self,
        latitude: float,
        longitude: float,
        radius: float = 1000.0,
        page: int = 1,
        num_of_rows: int = 10
    ) -> Dict:
        """
        좌표 기반 주변 주차장 검색
        
        Args:
            latitude: 위도
            longitude: 경도
            radius: 검색 반경 (미터 단위)
            page: 페이지 번호
            num_of_rows: 페이지당 결과 수
        
        Returns:
            주변 주차장 목록
        """
        endpoint = f"/{self.SERVICE_NAME}/ParkingInfoService/getParkingInfo"
        params = {
            "pageNo": page,
            "numOfRows": num_of_rows,
            "lat": latitude,
            "lng": longitude,
            "radius": radius,
        }
        
        return self._make_request(endpoint, params)
    
    def get_parking_list(
        self,
        page: int = 1,
        num_of_rows: int = 10
    ) -> Dict:
        """
        전국 공영주차장 기본 정보 조회
        
        Args:
            page: 페이지 번호
            num_of_rows: 페이지당 결과 수
        
        Returns:
            주차장 목록
        """
        endpoint = f"/{self.SERVICE_NAME}/ParkingInfoService/getParkingInfo"
        params = {
            "pageNo": page,
            "numOfRows": num_of_rows,
        }
        
        return self._make_request(endpoint, params)

