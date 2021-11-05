import os

from setuptools import find_packages
from setuptools import setup

name = "async_nbgrader"
here = os.path.abspath(os.path.dirname(__file__))
version_ns = {}
with open(os.path.join(here, name, "_version.py")) as f:
    exec(f.read(), {}, version_ns)

setup_args = dict(
    name=name,
    version=version_ns["__version__"],
    packages=find_packages(),
    entry_points={
        "console_scripts": ["ild=async_nbgrader.apps.async_nbgraderapp:main"]
    },
    install_requires=[
        "nbgrader>=0.6.2",
        "apscheduler>=3.7.0",
    ],
    include_package_data=True,
)

if __name__ == "__main__":
    setup(**setup_args)
