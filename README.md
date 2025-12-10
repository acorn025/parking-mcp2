# 주차장 정보 조회 MCP 서버

fastMCP를 사용하여 주차장 정보를 조회하는 MCP 서버입니다.

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

## 프로젝트 구조

```
parking-mcp2/
├── venv/                      # 가상환경 (gitignore됨)
├── .env                       # 환경 변수 (gitignore됨)
├── .env.example               # 환경 변수 예시
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

## 사용 방법

### 서버 실행

```powershell
# 가상환경 활성화
.\venv\Scripts\Activate.ps1

# 서버 실행 (모듈로 실행)
$env:PYTHONPATH="src"; python -m src.server
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
   - 서울/경기 지역은 실시간 주차 가능 대수 추가 제공
   - 기타 지역은 기본 주차장 정보 제공

2. **get_parking_info**
   - 특정 주차장 상세 정보 조회
   - 주차장 ID로 조회
   - 지역별 실시간 정보 자동 추가

### 지원하는 API

- **카카오 로컬 API**: 전국 주차장 검색 및 주소 변환 (주요 검색 API)
- **서울 열린데이터**: 서울시 실시간 주차 정보 (서울 지역 실시간 정보 추가)
- **경기데이터드림**: 경기도 실시간 주차 정보 (경기 지역 실시간 정보 추가)

## 의존성

- fastmcp: MCP 서버 프레임워크
- requests: HTTP API 호출
- python-dotenv: 환경 변수 관리

