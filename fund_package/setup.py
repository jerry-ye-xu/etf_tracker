import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="fund_package", # Replace with your own username
    version="0.0.1",
    author="Jerry Xu",
    author_email="jerryxu2500@gmail.com",
    description="Modules used for extracing stock prices using Alpha Vantage",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)