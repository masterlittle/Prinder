from setuptools import setup
from setuptools import find_packages

with open('README.MD', 'rb') as f:
    readme = f.read().decode('utf-8')

setup(
    name='prinder',
    version='1.1.1',
    url='http://github.com/masterlittle/Prinder',
    author='Shitij Goyal',
    author_email='goyalshitij@gmail.com',
    description='Posts a list of open pull requests for an organization',
    long_description=readme,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'asn1crypto==0.24.0',
        'certifi==2018.4.16',
        'cffi==1.11.5',
        'chardet==3.0.4',
        'click==6.7',
        'cryptography==2.2.2',
        'enum34==1.1.6',
        'github3.py==1.1.0',
        'idna==2.7',
        'ipaddress==1.0.22',
        'ndg-httpsclient==0.5.0',
        'pyasn1==0.4.3',
        'pycparser==2.18',
        'pyOpenSSL==18.0.0',
        'python-dateutil==2.7.3',
        'PyYAML==3.13',
        'requests==2.19.1',
        'six==1.11.0',
        'slacker==0.9.65',
        'uritemplate==3.0.0',
        'urllib3==1.23'
        ],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License'
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points='''
        [console_scripts]
        prinder=prinder.prinder:run
    '''
)
