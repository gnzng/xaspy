
from distutils.core import setup
setup(
  name = 'xaspy',         # How you named your package folder (MyLib)
  packages = ['xaspy'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'package for analysis of experimental xray absorption spectroscopy data',   # Give a short description about your library
  author = 'YOUR NAME',                   # Type in your name
  author_email = 'damian@guenzing.de',      # Type in your E-Mail
  url = 'https://github.com/gnzng/xaspy',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/gnzng/xaspy/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['xray absorption spectroscopy', 'xmcd', 'synchrotron'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',
          'beautifulsoup4',
          'numpy',
          'pandas',
          'scipy',
          'matplotlib',
          'pickle'

      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',
  ],
)