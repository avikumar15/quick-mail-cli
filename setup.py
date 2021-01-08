import os
import pathlib

from setuptools import setup, find_packages

current_path = pathlib.Path(__file__).parent

with open(os.path.join(current_path, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = f.read().split('\n')

# print(install_requires)

setup(
    name='quickmailcli',
    description='A simple commandline application for sending mails quickly',
    version='1.0.0',
    install_requires=install_requires,
    author='Avi Kumar',
    author_email='avikumar.singh1508@gmail.com',
    python_requires='>=3.6',
    package_dir={'': 'src'},
    entry_points={'console_scripts': ['quickmailcli=src.quickmailcli.cli:execute']},
    url='https://github.com/avikumar15/quick-email-cli',
    keywords=['CLI', 'gmail', 'email']
)
