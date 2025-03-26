from setuptools import setup, find_packages

setup(
    name='scxml4py',
    version='0.2.0',
    author='Robert Karban, Luigi Andolfato',
    author_email='karbanite.engineering@gmail.com',
    description='SCXML library for Python',
    long_description = open("README.md", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/openmbee/scxml4py',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
