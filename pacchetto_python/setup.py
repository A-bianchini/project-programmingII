from setuptools import setup, find_packages

setup(
    name="traffico_ticino",
    version="0.1.1",
    description="A Python package to analyze traffic and air pollution in Ticino",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Arianna Bianchini, Giacomo Lugana, Roberto Stoian, Philip Peter",
    author_email="philip.peter@usi.ch",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas",
        "matplotlib",
        "seaborn",
        "statsmodels",
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    license_files=(),        
    python_requires=">=3.8",
)
