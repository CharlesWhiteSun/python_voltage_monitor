from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="python_voltage_monitor",
    version="1.1.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        # 其他必要的依賴套件
    ],
    description="Python application for retrieving voltage data from PLC devices and uploading it to the cloud for real-time energy monitoring.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CharlesWhiteSun/python_voltage_monitor",
    author="Charles",
    author_email="charleswhitesun@gmail.com",
    license="Apache License 2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
