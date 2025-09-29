from setuptools import setup, find_packages

setup(
    name="python_voltage_monitor",
    version="1.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # 加上必要的依賴，例如：
        # "numpy",
    ],
    python_requires=">=3.8",
)
