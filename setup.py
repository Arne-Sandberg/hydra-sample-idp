from setuptools import setup, find_packages

setup(
    name='sample-hydra-idp',
    version='0.0.1',
    description='',
    long_description='',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-login',
        'requests',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'run-hydra-sample-idp=hydra_sample_idp.idp:cli',
        ]
    },
    tests_require=['nose'],
    test_suite='nose.collector'
)
