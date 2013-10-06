import os
from setuptools import setup, find_packages
import github as app

install_requires = [
    'django',
    'django-celery',
    'requests>1.0.0'
]

tests_requires = [
    'django-discover-runner',
    'factory-boy',
    'mock',
    'httmock'
]


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name="django-octocat",
    version=app.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='django, app, reusable, github, git',
    author='Kit Sunde',
    author_email='kitsunde.com',
    url="https://github.com/Celc/django-octocat",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'tests': tests_requires
    },
)
