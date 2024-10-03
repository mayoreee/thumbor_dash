from setuptools import setup, find_packages

# Read the contents of the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="thumbor_dash",
    version="0.0.21",
    author="mayoreee",
    description="A thumbor server extension for DASH",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mayoreee/thumbor_dash",
    project_urls={
        "Source Code": "https://github.com/mayoreee/thumbor_dash",
        "Bug Tracker": "https://github.com/mayoreee/thumbor_dash/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.11",
    install_requires=[
        "thumbor >= 7.7.4",
        "grpcio >= 1.38.1",
        "protobuf >= 3.17.3",
        "dapiclient @ git+https://github.com/mayoreee/dapi-client-py.git@d0520b7#egg=dapiclient",
    ],
    entry_points={
        "console_scripts": [
            "thumbor_dash = thumbor_dash.server:main",
            "thumbor_dash-url = thumbor_dash.url_composer:main",
        ],
    },
)
