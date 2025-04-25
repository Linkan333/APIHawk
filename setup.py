from setuptools import setup, find_packages

setup(
    name="apihawk",
    version="0.1.0",
    packages=find_packages(where=".", exclude=["tests*"]),
    include_package_data=True,
    install_requires=[
        "httpx[http2]>=0.28.1",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "pytest>=8.3.5",
        "pytest-asyncio>=0.26.0",
        "anyio>=4.2.0",
        "urllib3>=2.0.0"
    ],
    entry_points={
        "console_scripts": [
            "apihawk=apihawk.cli:main",
        ],
    },
)