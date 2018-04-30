from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'ex3',
  ext_modules = cythonize("ex3.pyx"),
)