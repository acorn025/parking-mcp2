"""
주차장 정보 조회 MCP 서버 패키지 설정
"""

from setuptools import setup, find_packages

setup(
    name="parking-mcp",
    version="0.1.0",
    description="전국 주차장 정보 조회 MCP 서버",
    packages=find_packages(include=["src", "src.*"]),
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
    python_requires=">=3.8",
)

