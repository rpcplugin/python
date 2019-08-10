import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rpcplugin",
    version="0.0.1",
    author="Martin Atkins",
    author_email="mart@degeneration.co.uk",
    description="gRPC-based plugin system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rpcplugin/python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
