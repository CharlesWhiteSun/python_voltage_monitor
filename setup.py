from setuptools import setup, find_packages

setup(
    name="python_voltage_monitor",
    version="1.0.0",  # 請根據實際版本進行更新
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",  # 假設有這個依賴，請根據實際情況調整
        # 其他必要的依賴套件
    ],
    description="Python application for retrieving voltage data from PLC devices and uploading it to the cloud for real-time energy monitoring.",
    long_description=open("README.md").read(),
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
