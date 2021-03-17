import os
import pathlib

from setuptools import setup, find_packages

current_path = pathlib.Path(__file__).parent

with open(os.path.join(current_path, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = f.read().split('\n')

"""
print(install_requires)
print(open('PYPI_DESCRIPTION.md', 'r', encoding='utf-8').read())
"""
setup(
    name='quick-mail',
    description='A simple commandline application for sending mails quickly',
    version='1.0.1',
    install_requires=install_requires,
    author='Avi Kumar Singh',
    author_email='avikumar.singh1508@gmail.com',
    python_requires='>=3.0',
    long_description_content_type="text/markdown",
    long_description=open('PYPI_DESCRIPTION.md', 'r', encoding='utf-8').read(),
    packages=find_packages(),
    #    package_dir={'': 'quickmail'},
    entry_points={'console_scripts': ['quickmail=quickmail.cli:execute']},
    url='https://github.com/avikumar15/quick-email-cli',
    license="MIT",
    keywords=['CLI', 'gmail', 'email'],
    # platforms='any',
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        'Topic :: Education',
        'Topic :: Communications',
        'Topic :: Communications :: Email',
        'Topic :: Internet',
        'Topic :: Terminals',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Education',
        'Intended Audience :: Other Audience',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
