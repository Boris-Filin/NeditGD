import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='neditgd',
    python_requires='>=3.12.0',
    version='0.3.1',    
    description='Lightweight Geometry Dash level scripting tool',
    url='https://github.com/Boris-Filin/NeditGD',
    author='Nemo2510 (Boris Filin)',
    author_email='oonemoo2510@gmail.com',
    license='MIT',
    install_requires=['websocket-client'],
    long_description_content_type="text/markdown",
    long_description=read('README.md')
)