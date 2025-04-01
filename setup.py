from setuptools import setup, find_packages

setup(
    name="portfolio_tracker",
    version="0.1.0",
    packages=find_packages(),  # This finds "app" if it has __init__.py
    install_requires=[
        "streamlit",
        "pandas",
        # etc...
    ],
)