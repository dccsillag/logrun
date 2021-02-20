from setuptools import setup


setup(
    name="microlog",
    version="0.1.0",
    description="A convenient experiment logging package for Python",
    url="https://github.com/dccsillag/microlog",
    author="Daniel Csillag",
    license="WTFPL",
    packages=['microlog'],
    install_requires=['dill', 'gitpython'],

    # TODO: classifiers
)
