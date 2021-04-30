from setuptools import setup, find_packages

setup(
    name='webspiderv2',
    version='19.6.13',
    packages=find_packages(),
    url='',
    license='',
    author='maxwellchen, Erdi Fan',
    author_email='',
    description='',

    install_requires=[
        'beautifulsoup4==4.7.1',
        'bs4==0.0.1',
        'certifi==2019.3.9',
        'chardet==3.0.4',
        'idna==2.8',
        'lxml==4.3.4',
        'requests==2.22.0',
        'selenium==3.141.0',
        'soupsieve==1.9.1',
        'urllib3==1.25.8',
        'setuptools==40.8.0',
    ],
    entry_points = {
        'console_scripts':[
            'go = src.webspider:main'
        ]
    }
)
