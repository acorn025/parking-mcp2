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
├── venv/                 # 가상환경 (gitignore됨)
├── .env                  # 환경 변수 (gitignore됨)
├── .env.example          # 환경 변수 예시
├── .gitignore
├── requirements.txt      # Python 의존성
├── README.md
└── src/                  # 소스 코드 (추가 예정)
```

## 사용 방법

개발 환경 설정이 완료되면 MCP 서버 코드를 작성할 수 있습니다.

## 의존성

- fastmcp: MCP 서버 프레임워크
- requests: HTTP API 호출
- python-dotenv: 환경 변수 관리

