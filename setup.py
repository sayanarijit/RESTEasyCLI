from os import path
from codecs import open
from setuptools import setup, find_packages

PROJECT = 'RESTEasyCLI'
VERSION = '0.1.2'  # Also resteasycli.config.Config, README.md


here = path.abspath(path.dirname(__file__))

# Get requirements from requirements.txt file
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read().splitlines()

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=PROJECT,
    version=VERSION,

    # Also change resteasycli.config.Config, README.md
    description='Handy REST API client on your terminal',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/rapidstack/RESTEasyCLI',
    download_url='https://github.com/rapidstack/RESTEasyCLI/archive/%s.tar.gz' % VERSION,
    author='Arijit Basu',
    author_email='sayanarijit@gmail.com',
    license='MIT',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
        'Topic :: Utilities',
        'Topic :: Software Development',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft'
    ],
    platforms=['Any'],

    install_requires=requirements,

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'recli = resteasycli.cmd.main:main'
        ],
        'cliff.recli': [
            'init = resteasycli.cmd.initialize:Init',
            'get = resteasycli.cmd.methods:GET',
            'post = resteasycli.cmd.methods:POST',
            'put = resteasycli.cmd.methods:PUT',
            'patch = resteasycli.cmd.methods:PATCH',
            'delete = resteasycli.cmd.methods:DELETE',
            'list = resteasycli.cmd.methods:LIST',
            'show = resteasycli.cmd.methods:SHOW'
        ]
    },
    keywords='REST API client CLI tool'
)
