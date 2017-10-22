#! /usr/bin/env python
#! -*- encoding: utf-8 -*-

import codecs
import os

from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    description = f.readline()
    long_description = f.read()

if __name__ == '__main__':
    setup(
        name = 'glossarist',
        version = '1.0.0',
        description = description,
        long_description = long_description,
        license = 'MIT',

        url = 'https://github.com/kshitij10496/glossarist',
        download_url ='https://github.com/kshitij10496/glossarist/releases/tag/v1.0.0',

        author = 'Kshitij Saraogi',
        author_email = 'kshitijsaraogi@gmail.com',

        classifiers=[
                    'Development Status :: 3 - Alpha',
                    'Intended Audience :: Developers',
                    'Topic :: Software Development :: Build Tools',
                    'License :: OSI Approved :: MIT License',
                    'Programming Language :: Python :: 3.5',
                    ],
        keywords='vocabulary command-line',

        packages = ['glossarist'],
        include_package_data = True,
        install_requires = [
            'Click',
            'arrow',
            'python-dateutil',
            'requests',
            'tabulate',
            'wordnik-py3'
        ],
        entry_points = {
            'console_scripts': [
                'glossarist=glossarist.cli:glossarist'
            ]
        }
    )
