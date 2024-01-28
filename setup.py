import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="h5viewer",
    version="24.01.28",
    author="Cong Wang",
    author_email="wangimagine@gmail.com",
    description="A HDF5 viewer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carbonscott/h5viewer",
    keywords = ['h5viewer'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts' : [
            'h5viewer=h5viewer.serve:main',
        ],
    },
    python_requires='>=3.6',
    include_package_data=True,
)
