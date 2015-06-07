import os
from setuptools import setup, find_packages

try:
    f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
    long_description = f.read().strip()
    f.close()
except IOError:
    long_description = None

setup(
    name='django-static-lor',
    version='1.0',
    url="",
    description="",
    long_description=long_description,
    author='ZuluPro (Anthony MONTHE)',
    author_email='anthony.monthe@gmail.com',
    license='BSD',
    platforms='any',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
    packages=find_packages(exclude=['lor.tests']),
    include_package_data=True,
    test_suite='lor.tests',
    install_requires=['Django>=1.6']
)