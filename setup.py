from setuptools import setup

setup(name='pyPly',
      version='0.0.1',
      description='A set of Python classes designed for composite materials CLT calculations',
      url='http://github.com/Rlee13/pyPLY',
      author='Liviu Armeanu',
      author_email='-',
      license='GPL 2.0',
      packages=['pyPLY'],
      install_requires=[
            'numpy',
      ],
      zip_safe=False)