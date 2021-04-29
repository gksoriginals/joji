import pathlib
from setuptools import setup, find_packages


HERE = pathlib.Path(__file__).parent


README = (HERE / "README.md").read_text()


requirements = [
    "ipython",
    "ipdb",
    "pytest",
    "requests",
    "flask",
    "gunicorn",
    "sqlalchemy",
    "mysql-connector-python",
    "unidecode",
    "spacy",
    "emoji",
    "numba"
]

setup(
    name="joji",
    version="1.1.9",
    description="convert a word to corresponding emoji",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/GopikrishnanSasikumar/joji",
    author="Gopikrishnan Sasikumar",
    author_email="gopikrishnans1996@gmail.com",
    zip_safe=False,
    packages=["joji"],
    package_data={"joji": ["data/emoji_dict1.p"]},
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="text to emoji"
)
