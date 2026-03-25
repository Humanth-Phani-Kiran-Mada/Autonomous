"""
Setup configuration for Autonomous AI System package distribution
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README content
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = (
    requirements_path.read_text(encoding="utf-8").splitlines()
    if requirements_path.exists()
    else []
)

setup(
    name="autonomous-ai-system",
    version="1.0.0",
    author="Mada-Humanth-Phani-Kiran",
    author_email="humanathphanikiran@gmail.com",
    description="A sophisticated, autonomous AI system for continuous self-improvement and knowledge acquisition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Humanth-Phani-Kiran-Mada/Autonomous",
    project_urls={
        "Bug Tracker": "https://github.com/Humanth-Phani-Kiran-Mada/Autonomous/issues",
        "Documentation": "https://github.com/Humanth-Phani-Kiran-Mada/Autonomous",
        "Source Code": "https://github.com/Humanth-Phani-Kiran-Mada/Autonomous",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
            "pylint>=2.0",
            "radon>=5.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "autonomous=main:main",
            "autonomous-cli=run_autonomous_system:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
