from cx_Freeze import setup, Executable

setup(name='Carpenter World Builder',
      version='pre-alpha1.0',
      executables = [Executable('carpenter.py')])
