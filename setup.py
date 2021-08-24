import os
from setuptools import setup, find_packages

name = 'async_nbgrader'
here = os.path.abspath(os.path.dirname(__file__))
version_ns = {}
with open(os.path.join(here, name, '_version.py')) as f:
    exec(f.read(), {}, version_ns)

setup_args = dict(
    name=name,
    version=version_ns['__version__'],
    packages=find_packages(),
    install_requires=[
        "jupyter_core==4.7.1",
        "notebook==6.4.2",
        "nbgrader==0.6.2",
        "apscheduler==3.7.0",
    ],
    include_package_data=True
)

if __name__ == "__main__":
    setup(**setup_args)
