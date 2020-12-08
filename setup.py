
from setuptools import setup, find_packages
from mylibrary.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='mylibrary',
    version=VERSION,
    description='MyLibrary server side',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Vitaly Zarubin',
    author_email='keygenqt@gmail.com',
    url='https://github.com/keygenqt/MyLibrary-server',
    license='Apache License 2.0',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'mylibrary': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        mylibrary = mylibrary.main:main
    """,
)
