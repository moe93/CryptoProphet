#!/usr/bin/env python3
"""
CryptoProphet is a python crypto trading bot with forecasting
abilities to determine buy and sell orders.

A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""
DOCLINES = (__doc__ or '').split("\n")

from setuptools import setup, find_packages
import pathlib
import sys

# Python supported version checks. Keep right after stdlib imports to ensure we
# get a sensible error for older Python versions
if sys.version_info[:2] < (3, 8):
    raise RuntimeError("Python version >= 3.8 required.")

here = pathlib.Path(__file__).parent.resolve()
with (here/"README.md").open(mode='r', encoding="utf-8") as fh:
    long_description = fh.read()


setup(
        name='cryptoprophet',
        version=".".join(("0", "0", "1")),
        description='Crypto trader with forecasting capabilities',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://gitlab.com/moe93/cryptoprophet',
        author='Mohammad Odeh',
        author_email='m.odeh93@gmail.com',
        keywords=["technical analysis", "trading", "python3"],
        classifiers=[  # Optional
                # Check: http://pypi.python.org/pypi?%3Aaction=list_classifiers
                # How mature is this project? Common values are
                "Development Status :: 1 - Planning",
                # "Development Status :: 2 - Pre - Alpha",
                # "Development Status :: 3 - Alpha",
                # "Development Status :: 4 - Beta",
                # "Development Status :: 5 - Production / Stable",
                # "Development Status :: 6 - Mature",
                # "Development Status :: 7 - Inactive",
                # Indicate who your project is intended for
                "Intended Audience :: Developers",
                "Intended Audience :: Education",
                "Intended Audience :: Other Audience",
                # Pick your license as you wish
                "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                # Compatible operating systems
                "Operating System :: MacOS",
                # Specify the Python versions you support here. In particular, ensure
                # that you indicate you support Python 3. These classifiers are *not*
                # checked by 'pip install'. See instead 'python_requires' below.
                "Programming Language :: Python :: 3",
                "Programming Language :: Python :: 3.8",
                "Programming Language :: Python :: 3.9",
                "Programming Language :: Python :: 3.10",
                "Programming Language :: Python :: 3 :: Only",
                # Topic of project
                "Topic :: Scientific/Engineering :: Artificial Intelligence",
                "Topic :: Scientific/Engineering :: Information Analysis",
                ],
        package_dir={"": "cryptoprophet"},
        packages=find_packages( where="cryptoprophet",
                                include=[ 'crypto_bot', 'telegram_bot', '*_bot' ] ),
        package_data={
                "data": ["data/*.csv"],
            },
        include_package_data=True,
        python_requires=">=3.8, <4",
        install_requires=[
                'matplotlib==3.5.2',
                'numpy==1.23.1',
                'orjson==3.7.11',
                'pandas==1.4.3',
                'pandas-ta==0.3.14b0',
                'python-dotenv==0.20.0',
                'python-telegram-bot==13.13',
                # 'python-telegram-bot==20.0a1',
                'readchar==3.1.0',
                'requests==2.28.1',
                'statsmodels==0.13.2',
                'websockets==10.3.0'
                ],
        )
