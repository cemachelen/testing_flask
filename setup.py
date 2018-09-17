'''
build a distribution file and install that in another environment, just like
you installed Flask in your project’s environment. This makes deploying your
project the same as installing any other library, so you’re using all the
standard Python tools to manage everything.

Requires MANIFEST.in file
'''
from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
