from setuptools import setup

setup(name='pylend',
      version='0.0.1',
      description='A Python library for interacting with the LendingClub REST API',
      url='https://github.com/Webs961/pylend',
      author='William Barr III',
      author_email='will.barr@outlook.com',
      license='MIT',
      packages=['pylend'],
      install_requires=[
        'requests'
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],)
