from setuptools import setup, find_packages

setup(
    name="arch-universal-toolbox",
    version="0.1.0",
    description="Universal GUI toolbox for Arch Linux package management",
    author="Mig Saito",
    packages=find_packages(),
    install_requires=[
        "PyQt5>=5.15.0",
    ],
    entry_points={
        "console_scripts": [
            "arch-toolbox=src.main:main",
        ],
    },
    python_requires=">=3.8",
)
