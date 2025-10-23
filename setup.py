"""
Setup script for Champions League Draw Simulator
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="champions-league-draw",
    version="1.0.0",
    author="Iliass Sijelmassi",
    author_email="iliass.sij@icloud.com",
    description="UEFA Champions League Draw Simulator with constraint satisfaction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iliassSjm/champions-league-draw",
    project_urls={
        "Bug Tracker": "https://github.com/iliassSjm/champions-league-draw/issues",
        "Documentation": "https://github.com/iliassSjm/champions-league-draw/blob/main/ARCHITECTURE.md",
        "Source Code": "https://github.com/iliassSjm/champions-league-draw",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Games/Entertainment",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        # No external dependencies - uses only standard library
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    packages=["src", "tests"],
    package_dir={"src": "src", "tests": "tests"},
    entry_points={
        "console_scripts": [
            "ucl-draw=src.champions_league_draw:main",
            "ucl-stats=src.statistics:main",
            "ucl-demo=src.demo:main",
        ],
    },
    include_package_data=True,
    keywords="champions-league uefa draw simulator constraint-satisfaction algorithm",
)

