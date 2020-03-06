# WibblyWobbly

WibblyWobbly is a library to match a list of strings to a catalog using FuzzyWuzzy.

It is a common nightmare for data scientist, your human users captured the data according to a catalog but it is full of mistakes. WibblyWobbly automates the task of automatically matching the data to a catalog while allowing for manual review of suspicious cases and rejecting bad matches.


## Requirements

* Python 3 or higher
* fuzzywuzzy
* python-Levenshtein (optional)
* unidecode
* pandas


## Instalation

Using PIP via PyPI
```sh
pip install wibblywobbly
```

WibblyWobbly extends fuzzywuzzy, it is recomended to install python-Levenshtein too
```sh
pip install fuzzywuzzy[speedup]
```

Manually via GIT
```sh
git clone git://github.com/mar-esther23/wibblywobbly.git wibblywobbly
cd fuzzywuzzy
python setup.py install
```

## Usage


## Historial de versiones

* 0.1.0
    * We are online!
    * Basic operations to match list to catalogs

## Thanks
The [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy) team, you are amazing!

[Syats](https://github.com/syats/) for helping with the hierarchical code.

<p align="right"> You see, most people think that time is a strict progression of cause to effect, but actually, from a non-linear, non-subjective point of view, it’s more like a big ball of...Wibbly-Wobbly...Timey-Wimey...stuff. </p>
<p align="right"> - The Doctor </p>
