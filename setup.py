from setuptools import setup, find_packages

with open('README.md', mode='r', encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name             = 'python201',
    version          = '0.0.1',
    author           = 'Geoffrey Lentner',
    author_email     = 'glentner@purdue.edu',
    description      = 'A Python package for numerical algorithms.',
    license          = 'Apache Software License',
    keywords         = 'tutorial packaging example',
    url              = 'https://github.com/glentner/python201',
    packages         = find_packages(),
    include_package_data = True,
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    classifiers      = ['Development Status :: 4 - Beta',
                        'Programming Language :: Python :: 3.7',
                        'Programming Language :: Python :: 3.8',
                        'Operating System :: POSIX :: Linux',
                        'Operating System :: MacOS',
                        'Operating System :: Microsoft :: Windows',
                        'License :: OSI Approved :: Apache Software License', ],
    install_requires = ['numpy', 'numba', ],
    extras_require   = {
        'dev': ['ipython', 'pytest', 'hypothesis', 'pylint', 'sphinx',
                'pydata_sphinx_theme'],
    },
    entry_points = {
        'console_scripts': ['cumprod=python201.algorithms:main']
    },
    data_files = [
        ('share/man/man1', ['man/man1/cumprod.1', ]),
    ],
)
