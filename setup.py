from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    author='Noah Weinthal',
    author_email='nweinthal@gmail.com',
    description='An event-driven, pub sub webframework',
    license='MIT',
    long_description=long_description,
    name='latch',
    url='https://github.com/nweinthal/latch',
    version='0.0.1-alpha',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        "aiohttp==2.0.5",
        "aioredis==0.3.0",
        "appdirs==1.4.3",
        "appnope==0.1.0",
        "async-timeout==1.2.0",
        "chardet==2.3.0",
        "decorator==4.0.11",
        "hiredis==0.2.0",
        "ipython==6.0.0",
        "ipython-genutils==0.2.0",
        "jedi==0.10.2",
        "Jinja2==2.9.6",
        "jsonschema==2.6.0",
        "MarkupSafe==1.0",
        "multidict==2.1.4",
        "packaging==16.8",
        "pexpect==4.2.1",
        "pickleshare==0.7.4",
        "prompt-toolkit==1.0.14",
        "protobuf==3.2.0",
        "ptyprocess==0.5.1",
        "Pygments==2.2.0",
        "pyparsing==2.2.0",
        "PyYAML==3.12",
        "redis==2.10.5",
        "simplegeneric==0.8.1",
        "six==1.10.0",
        "swagger-parser==0.1.11",
        "swagger-spec-validator==2.1.0",
        "traitlets==4.3.2",
        "wcwidth==0.1.7",
        "yarl==0.10.0"
    ],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'sample=sample:main',
        ],
    },

    keywords='web framework async redis pubsub',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    package_data={
        '': ['*.proto'],
    }
)
