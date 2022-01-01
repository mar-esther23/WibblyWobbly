# WibblyWobbly

Python library to create equivalence dictionaries between a set of texts and a catalog using FuzzyWuzzy.

It is a common nightmare for data scientist, your human users captured the data according to a "catalog" but it is full of mistakes. WibblyWobbly automates the task of automatically matching the data to a catalog while allowing for manual review of suspicious cases and rejecting bad matches.

## Requirements

-  Python 3 or higher
-  the fuzz
-  python-Levenshtein (optional)
-  unidecode
-  pandas

#Instalation

Using PIP via PyPI

´´´
pip install wibblywobbly
´´´

WibblyWobbly extends hefuzz, it is recomended to install python-Levenshtein too

´´´
pip install thefuzz
pip install python-Levenshtein
´´´

## Usage

### Match data to a catalog

Import wibblywobbly and load your data and catalog as list. If you are using pandas use *.to_list()*.

´´´
import wibblywobbly as ww

catalog = ["Mouse", "Cat", "Dog", "Human"]
data = ["mice",  "CAT ", "doggo", "PERSON", 999]
´´´


WibblyWobbly compares the data to the catalog and returns the most likely options and a similarity score. If it cannot find a good match it will return the original data.

It automaticaly accepts the catalog options that have a higher similarity score than `thr_accept` and rejects those that have a lower score than `thr_reject`. This treshold values can be adjusted depending in the data quality. It ignores non-string values.

By default it returns a pandas dataframe that can be saved as a csv or excel file *.to_excel()*.



´´´
ww.map_list_to_catalog(data, catalog, thr_accept=95, thr_reject=40)
´´´

|   | Data  | Option1 | Score1 | Option2 | Score2 | Option3 | Score3 |
|---|-------|---------|--------|---------|--------|---------|--------|
| 0 | CAT   | Cat     | 100    | None    | NaN    | None    | NaN    |
| 1 | doggo | Dog     | 90     | Mouse   | 20.0   | Human   | 0.0    |
| 2 | mice  | Mouse   | 44     | Cat     | 29.0   | Human   | 22.0   |
| 3 | PERSON | PERSON | 0      | None    | NaN    | None    | NaN    |
| 4 | 999   | 999     | 0      | None    | NaN    | None    | NaN    |



WibblyWobbly can also return a dictionary with the best options. This dictionary can be used to clean a pandas dataframe with *.replace()* and *.map()*.

´´´
ww.map_list_to_catalog(data, catalog, output_format="dictionary")
´´´
´´´
{'mice': 'mice', 999: 999, 'doggo': 'Dog', 'PERSON': 'PERSON', 'CAT ': 'Cat'}
´´´


It is possible set a `reject_value`.

´´´
ww.map_list_to_catalog(data, catalog, output_format="dictionary", reject_value='Other')
´´´
´´´
{'mice': 'Other', 999: 999, 'doggo': 'Dog', 'PERSON': 'Other', 'CAT ': 'Cat'}
´´´


WibblyWobbly can also raise warnings of the suspicious values to facilitate visual inspection.

´´´
ww.map_list_to_catalog(data, catalog, output_format="dictionary", 
                           thr_accept=95, thr_reject=40,  warnings=True)
´´´

´´´
WOBBLY: mice
    	Options: Mouse (44), Cat (29), Human (22)
    WOBBLY: doggo
    	Options: Dog (90), Mouse (20), Human (0)

{'mice': 'Mouse', 999: 999, 'doggo': 'Dog', 'PERSON': 'PERSON', 'CAT ': 'Cat'}
´´´


## Versions
--------

-  0.2.0
   - Now uses thefuzz
   - Rough clustering algorithm
   - Hierarchical dictionaries
   - Happy New Year!

-  0.1.0
   -  We are online!
   -  Basic operations to match list to catalogs

Thanks
------

The [thefuzz](https://github.com/seatgeek/thefuzz` team, you are amazing!

[Syats](https://github.com/syats/) for helping with the hierarchical code.



--------------------------------------------

<p align="right"> You see, most people think that time is a strict progression of cause to effect, but actually, from a non-linear, non-subjective point of view, it’s more like a big ball of... Wibbly-Wobbly... Timey-Wimey... stuff. </p>
<p align="right">The Doctor</p>
<p align="right">The Doctor)
