from setuptools import setup, find_packages

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
    version="0.0.1",
    zip_safe=False,
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=requirements
)
