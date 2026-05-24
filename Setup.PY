"""
setup.py — ClinicEase package configuration
Used by the CI/CD pipeline to build a Python wheel artifact.
"""
from setuptools import setup, find_packages

setup(
    name="clinicease",
    version="1.0.0",
    description="ClinicEase Online Doctor Appointment Booking System",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="[Your Full Name]",
    python_requires=">=3.12",
    packages=find_packages(exclude=["tests*", "screenshort*", "docs*"]),
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn>=0.23.0",
        "bcrypt>=4.0.0",
        "httpx>=0.24.0",
    ],
    extras_require={
        "dev": [
            "pytest>=9.0.0",
            "pytest-cov>=4.0.0",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "Framework :: FastAPI",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
    ],
)