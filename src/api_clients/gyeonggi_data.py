"""
경기데이터드림 API 클라이언트
경기도 실시간 주차 정보
"""

import os
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()


class GyeonggiDataClient:
    """경기데이터드림 주차장 정보 API 클라이언트"""
    
    BASE_URL = "https://openapi.gg.go.kr"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Args:
            api_key: 경기데이터드림 API 키 (없으면 환경변수에서 로드)
        """
        self.api_key = api_key or os.getenv("GYEONGGI_DATA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GYEONGGI_DATA_API_KEY가 설정되지 않았습니다. "
                ".env 파일에 GYEONGGI_DATA_API_KEY를 추가하세요."
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
        params["KEY"] = self.api_key
        
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            
            # 빈 응답 체크
            if not response.content:
                raise ValueError("API 응답이 비어있습니다.")
            
            # JSON 응답 파싱
            data = response.json()
            
            # 경기데이터드림 에러 체크
            if isinstance(data, dict):
                # 에러 응답 형식 확인 (실제 API 문서에 따라 조정 필요)
                if "RESULT" in data:
                    result = data["RESULT"]
                    if result.get("CODE") and result.get("CODE") != "INFO-000":
                        error_msg = result.get("MESSAGE", "알 수 없는 오류")
                        raise ValueError(f"API 오류: {error_msg}")
            
            return {"status": "success", "data": data}
            
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
        except ValueError as e:
            # JSON 파싱 에러 등
            raise ValueError(f"응답 파싱 오류: {str(e)}")
    
    def get_realtime_parking_info(
        self,
        page: int = 1,
        size: int = 100
    ) -> Dict:
        """
        경기도 실시간 주차 정보 조회
        
        Args:
            page: 페이지 번호
            size: 페이지당 결과 수
        
        Returns:
            실시간 주차 정보
        """
        endpoint = "/Parking"
        params = {
            "Type": "json",
            "pIndex": page,
            "pSize": size,
        }
        
        return self._make_request(endpoint, params)
    
    def get_parking_availability(
        self,
        parking_id: Optional[str] = None,
        page: int = 1,
        size: int = 100
    ) -> Dict:
        """
        주차 가능 대수 조회
        
        Args:
            parking_id: 주차장 ID (None이면 전체)
            page: 페이지 번호
            size: 페이지당 결과 수
        
        Returns:
            주차 가능 대수 정보
        """
        endpoint = "/ParkingAvailability"
        params = {
            "Type": "json",
            "pIndex": page,
            "pSize": size,
        }
        
        if parking_id:
            params["PARKING_ID"] = parking_id
        
        return self._make_request(endpoint, params)

