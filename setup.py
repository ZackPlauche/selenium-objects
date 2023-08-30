from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='selenium-objects',
    version='0.1.0',
    description='A package for creating Selenium objects.',
    author='Zack Plauché',
    author_email='zackknowspython@gmail.com',
    packages=find_packages(),
    install_requires=requirements,
)

