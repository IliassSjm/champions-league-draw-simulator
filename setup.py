"""
Setup script for Champions League Draw Simulator
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="champions-league-draw",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies - uses only standard library
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    py_modules=[
        "champions_league_draw",
        "statistics",
        "export_json",
        "demo",
    ],
    entry_points={
        "console_scripts": [
            "ucl-draw=champions_league_draw:main",
            "ucl-stats=statistics:main",
            "ucl-demo=demo:main",
        ],
    },
    include_package_data=True,
    keywords="champions-league uefa draw simulator constraint-satisfaction algorithm",
)

