from setuptools import setup, find_packages

setup(
    name="smart_apply",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.3.0",
        "PyYAML>=6.0.1",
        "streamlit>=1.28.0",
        "python-dotenv>=1.0.0",
    ],
) 