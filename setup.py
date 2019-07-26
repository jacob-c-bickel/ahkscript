from setuptools import setup

def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name='ahkscript',
    version='0.9.0',
    description='AHK Script generator with helpful functionality for interacting with a Python script.',
    url='https://github.com/jacob-c-bickel/ahkscript',
    author='Jacob Bickel',
    author_email='jacob.c.bickel@gmail.com',
    license='MIT',
    include_package_data=True,
    packages=['ahkscript'],
    install_requires=[],
    zip_safe=False
)