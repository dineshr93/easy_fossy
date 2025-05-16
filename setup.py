from setuptools import setup, find_packages

setup(
    name="easy-fossy-mcp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "requests-toolbelt>=1.0.0",
        "pydantic>=2.7.2,<3.0.0",
        "mcp[cli]>=1.2.0",
    ],
    python_requires=">=3.9",
) 