from distutils.core import setup

import setuptools

with open("README.md", "r", encoding="utf-8") as fh :
    long_description = fh.read()


setuptools.setup(
    name='selenium_page_extension',
    packages=setuptools.find_packages(),
    version='v0.2',
    license='GNU GPLv3',
    description='Selenium simple POM extension',
    author='Antonio Giangrande',
    author_email='antoniogiangrandex@gmail.com',
    url='https://github.com/Daemos87/gian-selenium',
    download_url='https://github.com/Daemos87/gian-selenium/archive/v0.1.tar.gz',
    keywords=['SELENIUM', 'Page object model', 'No boilerplate'],
    install_requires=[
        "pytest",
        "selenium"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.9',
    ],

    entry_points={
        'pytest11' : [
            'selenium_page_extension = selenium_page_extension.hooks.web_test_gen',
        ]}
)
