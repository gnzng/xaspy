import os
from distutils.core import setup
__authors__ = 'Damian Guenzing  \n Alpha T. N\'Diaye'


_version__ = None
with open(os.path.join('xaspy', '_version.py'), 'r') as version_file:
    lines = version_file.readlines()
    for line in lines:
        line = line[:-1]
        if line.startswith('__version__'):
            key, vers = [w.strip() for w in line.split('=')]
            __version__ = vers.replace("'",  "").replace('"',  "").strip()


setup(
  name='xaspy',
  packages=['xaspy',
            'xaspy.utils',
            'xaspy.xas',
            'xaspy.readin',
            'xaspy.beamlines'],
  version=__version__,
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description='package for analysis of experimental xray absorption spectroscopy data',
  author=__authors__,
  author_email='hi@gnzng.me',
  url='https://github.com/gnzng/xaspy',
  keywords=['xray absorption spectroscopy', 'xmcd', 'synchrotron'],
  install_requires=[
          'numpy',
          'pandas',
          'scipy',
          'matplotlib',
          'python-telegram-bot',
          'xraydb'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',
  ],
)
