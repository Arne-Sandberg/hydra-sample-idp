from setuptools import setup, find_packages

setup(
    name='sample-hydra-idp',
    version='0.0.1',
    description='',
    long_description='',
    packages=find_packages(),
    zip_safe=False,
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
    include_package_data=True,
    tests_require=['nose'],
    test_suite='nose.collector'
)
