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
    "emoji"
]

setup(
    name="joji",
    version="1.0.0",
    description="convert a word to corresponding emoji",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/GopikrishnanSasikumar/joji",
    author="Gopikrishnan Sasikumar",
    author_email="gopikrishnans1996@gmail.com",
    license="MIT",
    zip_safe=False,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=requirements
)
