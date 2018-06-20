from setuptools import setup

with open('README.rst', 'rb') as f:
    readme = f.read().decode('utf-8')

setup(
    name='prinder',
    version='0.1.0',
    url='http://github.com/masterlittle/prinder',
    author='Shitij Goyal',
    author_email='goyalshitij@gmail.com',
    description='Posts a list of open pull requests for an organization',
    long_description=readme,
    py_modules=['prinder'],
    license='MIT',
    install_requires=[
        'requests==2.18.3',
        'github3.py==1.0.0a4', 'click'
    ],
    entry_points='''
        [console_scripts]
        prinder=prinder:cli
    '''
)
