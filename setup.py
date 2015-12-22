from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pylend',
      version='0.0.4',
      description='A Python library for interacting with the LendingClub REST API',
      long_description=readme(),
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.3',
        'Topic :: Office/Business :: Financial :: Investment'
      ],
      url='https://github.com/Webs961/pylend',
      author='William Barr III',
      author_email='will.barr@outlook.com',
      license='MIT',
      packages=['pylend'],
      install_requires=[
        'requests',
        'arrow'
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],)
