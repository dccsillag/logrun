from setuptools import setup


setup(
    name="exlog",
    version="0.1.0",
    description="A convenient experiment logging package for Python",
    url="https://github.com/dccsillag/exlog",
    author="Daniel Csillag",
    author_email="dccsillag@gmail.com",
    license="MIT",
    packages=['exlog', 'exlog.utils'],
    install_requires=['dill',
                      'psutil',
                      'xxhash',
                      'gitpython'],

    # TODO: classifiers
)
