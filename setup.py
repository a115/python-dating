import os
from codecs import open
from setuptools import setup, find_packages

from dating import VERSION

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

try:
    import pypandoc
    long_description = pypandoc.convert(os.path.join(here, 'README.md'), 'rst')
except (ImportError, IOError):
    pass

setup(
        name='dating',
        version=VERSION,
        description='Library for handling date ranges and time periods in a business context',
        long_description=long_description,
        url='https://github.com/a115/python-dating',
        author='Jordan Dimov',
        author_email='jdimov@mlke.net',
        license='MIT',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            ],
        keywords='datetime date range ISO8601',
        packages=['dating',],
        install_requires=[
            'iso8601>=0.1.12',
            'pytz>=2017.2',
            ],
        python_requires='>=3'
)
