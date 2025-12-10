# FastMCP 배포 가이드

## Entry Point 설정 방법

### 현재 구조

현재 프로젝트는 다음과 같이 구성되어 있습니다:

```
src/
  └── server.py  # FastMCP 앱 인스턴스 (app)와 app.run() 포함
```

### Entry Point 옵션

#### 1. 모듈로 실행 (현재 방식) ✅

**장점**: 간단하고 즉시 사용 가능

**사용 방법**:
```bash
python -m src.server
```

**MCP 클라이언트 설정**:
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

#### 2. setup.py를 통한 Entry Point 설정 (권장)

**장점**: 패키지 설치 후 명령어로 직접 실행 가능

**setup.py 생성**:
```python
from setuptools import setup, find_packages

setup(
    name="parking-mcp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastmcp>=0.1.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "parking-mcp=src.server:main",
        ],
    },
)
```

**설치 및 사용**:
```bash
# 개발 모드로 설치
pip install -e .

# 실행
parking-mcp
```

**MCP 클라이언트 설정**:
```json
{
  "mcpServers": {
    "parking-mcp": {
      "command": "parking-mcp"
    }
  }
}
```

#### 3. 직접 실행 스크립트 생성

**장점**: 가장 명확하고 제어 가능

**src/server.py 수정** (이미 구현됨):
```python
if __name__ == "__main__":
    app.run()
```

**실행 스크립트 생성** (예: `run_server.py`):
```python
#!/usr/bin/env python
"""주차장 정보 조회 MCP 서버 실행 스크립트"""
import sys
import os

# src 디렉터리를 Python 경로에 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.server import app

if __name__ == "__main__":
    app.run()
```

**MCP 클라이언트 설정**:
```json
{
  "mcpServers": {
    "parking-mcp": {
      "command": "python",
      "args": ["run_server.py"],
      "cwd": "/path/to/parking-mcp2"
    }
  }
}
```

## 현재 프로젝트 Entry Point

### 현재 사용 중인 방식

**Entry Point**: `src.server:main` (함수)

**실행 명령어**:
```bash
python -m src.server
```

또는:
```bash
$env:PYTHONPATH="src"; python -m src.server
```

### MCP 클라이언트 설정 (현재)

```json
{
  "mcpServers": {
    "parking-mcp": {
      "command": "python",
      "args": ["-m", "src.server"],
      "env": {
        "PYTHONPATH": "src"
      },
      "cwd": "C:/AIproject/parking-mcp2"
    }
  }
}
```

## 배포 환경별 설정

### 로컬 개발 환경

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

### 가상환경 사용 시

```json
{
  "mcpServers": {
    "parking-mcp": {
      "command": "venv/Scripts/python.exe",
      "args": ["-m", "src.server"],
      "env": {
        "PYTHONPATH": "src"
      }
    }
  }
}
```

### 패키지 설치 후 (setup.py 사용 시)

```json
{
  "mcpServers": {
    "parking-mcp": {
      "command": "parking-mcp"
    }
  }
}
```

## 주의사항

1. **PYTHONPATH 설정**: `src` 디렉터리를 Python 경로에 포함해야 합니다.
2. **환경 변수**: `.env` 파일이 있는 디렉터리에서 실행해야 합니다.
3. **상대 경로**: `cwd` 설정 시 프로젝트 루트 디렉터리를 지정하세요.

## 추천 방식

**개발 환경**: 모듈로 실행 (현재 방식)
```bash
python -m src.server
```

**프로덕션 환경**: setup.py를 통한 entry point 설정
- 패키지로 설치하여 명령어로 실행
- 더 명확하고 관리하기 쉬움

