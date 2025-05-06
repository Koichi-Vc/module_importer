from setuptools import setup, find_packages

setup(
    name = 'module_importer',
    version='1.0.2',
    packages = find_packages(where='src'),
    package_dir = {'':'src'}
)
