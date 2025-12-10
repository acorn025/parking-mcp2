# 주차장 정보 조회 MCP 서버

fastMCP를 사용하여 전국 주차장 정보를 조회하는 MCP (Model Context Protocol) 서버입니다.

## 주요 특징

- **전국 주차장 검색**: 카카오 로컬 API를 통한 전국 주차장 검색
- **지역별 정보 제공**: 서울/경기 지역은 실시간 정보 및 상세 정보 제공
- **실시간 주차 정보**: 서울 지역 실시간 주차 가능 대수 제공
- **운영 시간 및 요금 정보**: 서울/경기 지역 운영 시간 및 요금 정보 제공
- **사용자 친화적 에러 메시지**: 기술적 용어 없이 명확한 안내 메시지

## 개발 환경 설정 (Windows)

### 1. Python 가상환경 생성

PowerShell에서 다음 명령어를 실행하세요:

```powershell
# Python 3.8 이상이 설치되어 있어야 합니다
python --version

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
.\venv\Scripts\Activate.ps1
```

**참고**: PowerShell 실행 정책 오류가 발생하는 경우:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

또는 Command Prompt(cmd)를 사용하는 경우:
```cmd
venv\Scripts\activate.bat
```

### 2. 필요한 라이브러리 설치

가상환경이 활성화된 상태에서:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env.example` 파일을 참고하여 `.env` 파일을 생성하세요:

```powershell
copy .env.example .env
```

그리고 `.env` 파일을 열어서 실제 API 키를 입력하세요.

**참고**: `.env.example` 파일이 없는 경우 `env.example` 파일을 참고하세요.

## 프로젝트 구조

```
parking-mcp2/
├── venv/                      # 가상환경 (gitignore됨)
├── .env                       # 환경 변수 (gitignore됨)
├── env.example                # 환경 변수 예시
├── .gitignore
├── requirements.txt           # Python 의존성
├── README.md
├── test_api.py                # API 클라이언트 테스트
├── test_api_call.py           # 실제 API 호출 테스트
├── test_server.py             # 서버 구조 테스트
└── src/                       # 소스 코드
    ├── __init__.py
    ├── server.py              # MCP 서버 메인 파일
    └── api_clients/           # API 클라이언트 모듈
        ├── __init__.py
        ├── kakao_local.py     # 카카오 로컬 API (주요 검색 API)
        ├── seoul_data.py      # 서울 열린데이터 (서울 실시간 정보)
        └── gyeonggi_data.py   # 경기데이터드림 (경기 실시간 정보)
```

## API 키 발급 방법

### 1. 카카오 로컬 API 키

1. [카카오 개발자 콘솔](https://developers.kakao.com/) 접속
2. 애플리케이션 생성
3. **앱 설정 > 앱 키**에서 **REST API 키** 복사
4. **제품 설정 > 카카오 로그인** 활성화 (필수)
5. **제품 설정 > 로컬** 활성화 (필수)
6. `.env` 파일에 `KAKAO_REST_API_KEY`에 입력

**주의**: "OPEN_MAP_AND_LOCAL" 서비스가 활성화되어 있어야 합니다.

### 2. 서울 열린데이터 API 키

1. [서울 열린데이터 광장](https://data.seoul.go.kr/) 접속
2. 회원가입 및 로그인
3. **마이페이지 > 인증키 관리**에서 인증키 발급
4. `.env` 파일에 `SEOUL_DATA_API_KEY`에 입력

**사용 API**: 
- `GetParkingInfo`: 서울시 공영주차장 실시간 정보

### 3. 경기데이터드림 API 키

1. [경기데이터드림](https://data.gg.go.kr/) 접속
2. 회원가입 및 로그인
3. **마이페이지 > 인증키 관리**에서 인증키 발급
4. `.env` 파일에 `GYEONGGI_DATA_API_KEY`에 입력

**사용 API**: 
- `ParkingPlace`: 경기도 공영주차장 정보

## 사용 방법

### 서버 실행

```powershell
# 가상환경 활성화
.\venv\Scripts\Activate.ps1

# 서버 실행 (모듈로 실행)
$env:PYTHONPATH="src"; python -m src.server
```

### MCP 서버 연결

MCP 클라이언트에서 다음과 같이 연결하세요:

```json
{
  "mcpServers": {
    "parking-mcp": {
      "command": "python",
      "args": ["-m", "src.server"],
      "env": {
        "PYTHONPATH": "src"
      }
    }
  }
}
```

### 테스트

```powershell
# API 클라이언트 초기화 테스트
python test_api.py

# 실제 API 호출 테스트 (카카오 API)
python test_api_call.py

# 서버 구조 테스트
python test_server.py
```

## 주요 기능

### 제공하는 Tool 함수

1. **search_nearby_parking**
   - 주변 주차장 검색 (카카오 로컬 API 사용)
   - 좌표 기반 검색 (위도, 경도, 반경)
   - 지역별 정보 자동 추가 (서울/경기/기타)
   
   **파라미터:**
   - `latitude`: 위도 (필수)
   - `longitude`: 경도 (필수)
   - `radius`: 검색 반경 미터 (기본값: 1000)

2. **get_parking_info**
   - 특정 주차장 상세 정보 조회
   - 주차장 이름 또는 주소로 검색
   - 지역별 실시간 정보 자동 추가
   
   **파라미터:**
   - `parking_id`: 주차장 이름 또는 주소 (필수)

### 지역별 제공 정보

| 정보 | 서울 | 경기 | 기타 |
|------|------|------|------|
| 기본 정보 (이름, 주소) | ✅ | ✅ | ✅ |
| 총 주차 대수 | ✅ | ✅ | ❌ |
| 실시간 주차 가능 대수 | ✅ | ❌ | ❌ |
| 운영 시간 | ✅ | ✅ | ❌ |
| 요금 정보 | ✅ | ✅ | ❌ |
| 업데이트 시간 | ✅ | ❌ | ❌ |

**서울 지역:**
- 실시간 주차 가능 대수 제공
- 상세 운영 시간 (평일/주말/공휴일)
- 상세 요금 정보 (기본 요금, 추가 요금, 일일 최대 요금 등)
- 실시간 정보 업데이트 시간

**경기 지역:**
- 총 주차 대수 제공
- 운영 시간 (평일/토요일/공휴일)
- 요금 정보 (기본 요금, 추가 요금, 결제 방법)

**기타 지역:**
- 기본 주차장 정보만 제공 (이름, 주소, 카테고리)
- 안내 메시지 표시

### 지원하는 API

- **카카오 로컬 API**: 전국 주차장 검색 및 주소 변환 (주요 검색 API)
- **서울 열린데이터**: 서울시 실시간 주차 정보 (서울 지역 실시간 정보 추가)
- **경기데이터드림**: 경기도 실시간 주차 정보 (경기 지역 실시간 정보 추가)

## 사용 예시

### 예시 1: 서울 지역 주차장 검색

```python
# search_nearby_parking 호출
{
  "latitude": 37.5665,
  "longitude": 126.9780,
  "radius": 1000
}

# 응답 예시
{
  "parkings": [
    {
      "name": "서울시청 주차장",
      "address": "서울 중구 세종대로 110",
      "total_spots": 1260,
      "available_spots": 507,
      "fee": "교통,지하철 > 지하철역 > 주차장",
      "distance": 62,
      "operating_info": {
        "operating_type": "시간제 운영",
        "weekday_start": "0000",
        "weekday_end": "2400",
        ...
      },
      "fee_info": {
        "is_paid": "유료",
        "basic_fee": 430.0,
        "basic_hours": 5.0,
        ...
      },
      "update_time": "2025-12-10 10:24:30"
    }
  ],
  "count": 1
}
```

### 예시 2: 경기 지역 주차장 검색

```python
# search_nearby_parking 호출
{
  "latitude": 37.2892,
  "longitude": 127.0086,
  "radius": 1000
}

# 응답 예시
{
  "parkings": [
    {
      "name": "화성행궁",
      "address": "경기도 수원시 팔달구 화성행궁 159",
      "total_spots": 62,
      "available_spots": null,
      "fee": "교통,지하철 > 지하철역 > 주차장",
      "distance": 0,
      "operating_info": {
        "weekday_start": "00:00",
        "weekday_end": "23:59",
        ...
      },
      "fee_info": {
        "is_paid": "유료",
        "basic_time": 90,
        "basic_fee": 400,
        ...
      }
    }
  ],
  "count": 1
}
```

### 예시 3: 기타 지역 주차장 검색

```python
# search_nearby_parking 호출
{
  "latitude": 35.1631,
  "longitude": 129.1636,
  "radius": 1000
}

# 응답 예시
{
  "notice": "해당 지역은 기본 주차장 정보만 제공됩니다. 실시간 정보는 서울 지역에서, 요금 및 운영시간 정보는 서울/경기 지역에서 이용 가능합니다.",
  "parkings": [
    {
      "name": "해운대역 주차장",
      "address": "부산 해운대구 우동 1378-95",
      "total_spots": null,
      "available_spots": null,
      "fee": "교통,지하철 > 지하철역 > 주차장",
      "distance": 0
    }
  ],
  "count": 1
}
```

### 에러 응답 예시

```json
{
  "error": "주차장 정보를 불러오는 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.",
  "parkings": []
}
```

상세한 응답 형식은 [MCP_RESPONSE_FORMAT.md](MCP_RESPONSE_FORMAT.md)를 참고하세요.

## 의존성

- fastmcp: MCP 서버 프레임워크
- requests: HTTP API 호출
- python-dotenv: 환경 변수 관리

