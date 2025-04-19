import os
from setuptools import setup, find_packages

__authors__ = "Damian Guenzing\nAlpha T. N'Diaye"

__version__ = None
with open(os.path.join("xaspy", "_version.py"), "r") as version_file:
    lines = version_file.readlines()
    for line in lines:
        line = line[:-1]
        if line.startswith("__version__"):
            key, vers = [w.strip() for w in line.split("=")]
            __version__ = vers.replace("'", "").replace('"', "").strip()

setup(
    name="xaspy",
    packages=find_packages(),
    version=__version__,
    license="MIT",
    description="package for analysis of experimental xray absorption spectroscopy data",
    author=__authors__,
    author_email="hi@gnzng.me",
    url="https://github.com/gnzng/xaspy",
    keywords=["xray absorption spectroscopy", "xmcd", "synchrotron"],
    install_requires=[
        "numpy",
        "pandas",
        "scipy",
        "matplotlib",
        "pytest",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
)
