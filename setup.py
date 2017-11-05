#! /usr/bin/env python
#! -*- encoding: utf-8 -*-

import codecs
import os

from setuptools import setup, find_packages

if __name__ == '__main__':
    setup(
        name = 'lexico',
        version = '0.0.1',
        description = 'Assistant to write your personalised glossary',
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

        packages = ['lexico'],
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
                'lexico=lexico.cli:lexico'
            ]
        }
    )
