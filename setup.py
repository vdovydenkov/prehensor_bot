from setuptools import setup, find_packages

setup(
    name="prehensor_bot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-telegram-bot>=20.0,<21.0",
        "pydantic>=2.0,<3.0",
        "PyYAML>=6.0,<7.0",
        "python-dotenv>=1.0,<2.0",
        "yt-dlp>=2023.5.1,<2024.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0,<8.0",
            "pytest-asyncio>=0.20,<1.0",
            "pytest-mock>=3.0,<4.0",
            "flake8>=6.0,<7.0",
            "mypy>=1.0,<2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "prehensor_bot = bot.__main__:main",
        ],
    },
)
