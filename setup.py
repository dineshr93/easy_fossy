import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easy_fossy",
    version="1.0.9",
    author="dinesh_ravi",
    author_email="dineshr93@gmail.com",
    description="fossology API wrapper in python 3.10",
    long_description=long_description,
    long_description_content_type="text/markdown", install_requires=[
        'certifi==2021.10.8',
        'charset-normalizer==2.0.7',
        'idna==3.3',
        'pydantic==1.8.2',
        'requests==2.26.0',
        'requests-toolbelt==0.9.1',
        'typing-extensions==3.10.0.2',
        'urllib3==1.26.7',
    ],
    url="https://github.com/dineshr93/easy_fossy",
    project_urls={
        "Bug Tracker": "https://github.com/dineshr93/easy_fossy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
)
