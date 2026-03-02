"""
Setup script for Morse Decoder Package
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取 README 文件
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

# 读取版本号
version = "1.0.0"

setup(
    name="morse-decoder",
    version=version,
    author="Morse Decoder Team",
    author_email="contact@morsedecoder.dev",
    description="高性能摩尔斯电码解码器，支持多种解码算法",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/morse-decoder",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "scikit-learn>=0.24.0",
        "sounddevice>=0.4.5",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
            "mypy>=0.900",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "morse-decode=morse_decoder.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
