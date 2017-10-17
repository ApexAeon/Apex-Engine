from cx_Freeze import setup, Executable

setup(name='Cataclysm',
      version='pre-alpha1.0',
      executables = [Executable('frame.py')])
