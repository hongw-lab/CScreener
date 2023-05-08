from setuptools import setup, find_packages

import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name="cscreener",
    version="0.1.0",
    author="Xingjian Zhang",
    description="A GUI to assist cell picking for CNMFE outputs",
    packages=find_packages(),
    project_urls={"Source Code": "https://github.com/hsingchien/CScreener"},
    entry_points={"console_scripts": ["screen-cell=cscreener.app:main"]},
    python_requires="==3.9",
)
