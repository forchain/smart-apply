from setuptools import setup, find_packages

setup(
    name="smart-apply",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "openai>=1.3.0",
        "streamlit>=1.28.0",
        "python-dotenv>=1.0.0",
        "PyYAML>=6.0.1",
        "requests>=2.31.0",
    ],
    author="forchain",
    description="Streamline Your Job Application Process With LLM",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/forchain/smart-apply",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
) 