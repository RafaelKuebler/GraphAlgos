from distutils.core import setup

setup(
    name='GraphAlgos',
    version='0.1dev',
    packages=['graphalgos',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    install_requires=[
            "pygame == 1.9.2",
            "Pygcurse == 0.10.3",
    ],
)
