from distutils.core import setup
setup(
  name = 'wibblywobbly',
  packages = ['wibblywobbly'],
  version = '0.1',
  license='MIT',
  description = 'Python library to create equivalence dictionaries between a set of texts and a catalog using FuzzyWuzzy. ',
  author = 'ME Martinez-Sanchez',
  author_email = 'mar.esther23@gmail.com',
  url = 'https://github.com/mar-esther23/WibblyWobbly',
  download_url = 'https://github.com/mar-esther23/WibblyWobbly/archive/v_01.tar.gz',
  keywords = ['fuzzy matching', 'catalog', 'data cleaning', 'fuzzywuzzy'],
  install_requires=[
          'fuzzywuzzy',
          'unidecode',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Beta',
    'Intended Audience :: DataScientists',
    'Topic :: Data Science :: Data cleaning',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)