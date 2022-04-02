# WibblyWobbly

## Overview

WibblyWobbly is a Python 3 library that creates equivalence dictionaries between a set of texts and a strings catalog using the fuzzy string matching [FuzzyWuzzy](https://pypi.org/project/fuzzywuzzy/). WibblyWobbly automates the matching of the data to a catalog while allowing for manual review of suspicious cases and rejecting bad matches. If it WibblyWobbly cannot find a good match it will return the original data.

WibblyWobbly automaticaly accepts the catalog options that have a higher similarity score than a given acceptance threshold (`thr_accept`) and rejects those that have a lower score than agiven rejection threshold (`thr_reject`). This treshold values can be adjusted depending in the data quality. WibblyWobbly ignores non-string values.

The default output of WibblyWobbly is a pandas dataframe that can be saved as a csv or excel file using `dataframe_name.to_excel()`.

## Requirements

-  [Python 3](https://www.python.org/downloads/) or higher
-  [unidecode](https://pypi.org/project/Unidecode/): Python package
-  [pandas](https://pandas.pydata.org/): Python set of data analysis and manipulation tools 
-  [TheFuzz](https://github.com/seatgeek/thefuzz/): Python package


Additionally, you may want to get the [python-Levenshtein](https://github.com/ztane/python-Levenshtein/) package for python. It consists on a set of fast computation functions that may improve the performance time of WibblyWobbly.

## Installation

### Using PIP via PyPI

1. As WibblyWobbly is an extension of Thefuzz you must download Thefuzz first. It is recomended to install `python-Levenshtein` too. Consider that `python-Levenshtein` has its own dependencies. 
   ```
   pip install thefuzz
   pip install python-Levenshtein #optional
   ```
2. Install WibblyWobbly.
   ```
   pip install wibblywobbly
   ```

## Usage

### Match Data to a Catalog

1. Import `wibblywobbly`.
   ```
   import wibblywobbly as ww
   ```
2. Load your data and catalog as lists (if you are using pandas use `.to_list()`.)
   ```
   catalog = ["Mouse", "Cat", "Dog", "Human"]
   data = ["mice",  "CAT ", "doggo", "PERSON", 999]
   ```
3. Use the method `map_list_to_catalog` in your WibblyWobbly instance to match the data with the catalog in a pandas dataframe.
   ```
   ww.map_list_to_catalog(data, catalog, thr_accept=95, thr_reject=40)
   ```
   The following table shows an output table example for the catalog and data in two.
   |   | Data  | Option1 | Score1 | Option2 | Score2 | Option3 | Score3 |
   |---|-------|---------|--------|---------|--------|---------|--------|
   | 0 | CAT   | Cat     | 100    | None    | NaN    | None    | NaN    |
   | 1 | doggo | Dog     | 90     | Mouse   | 20.0   | Human   | 0.0    |
   | 2 | mice  | Mouse   | 44     | Cat     | 29.0   | Human   | 22.0   |
   | 3 | PERSON | PERSON | 0      | None    | NaN    | None    | NaN    |
   | 4 | 999   | 999     | 0      | None    | NaN    | None    | NaN    |



WibblyWobbly can also return a dictionary with the best options. This dictionary can be used to clean a pandas dataframe with `.replace()` and `.map()`.

``
ww.map_list_to_catalog(data, catalog, output_format="dictionary")
``
> {'mice': 'mice', 999: 999, 'doggo': 'Dog', 'PERSON': 'PERSON', 'CAT ': 'Cat'}



It is possible set a `reject_value`.

``
ww.map_list_to_catalog(data, catalog, output_format="dictionary", reject_value='Other')
``
> {'mice': 'Other', 999: 999, 'doggo': 'Dog', 'PERSON': 'Other', 'CAT ': 'Cat'}



WibblyWobbly can also raise warnings of the suspicious values to facilitate visual inspection.

``
ww.map_list_to_catalog(data, catalog, output_format="dictionary", 
                           thr_accept=95, thr_reject=40,  warnings=True)
``

> WOBBLY: mice
>     	Options: Mouse (44), Cat (29), Human (22)
>     WOBBLY: doggo
>     	Options: Dog (90), Mouse (20), Human (0)
> 
> {'mice': 'Mouse', 999: 999, 'doggo': 'Dog', 'PERSON': 'PERSON', 'CAT ': 'Cat'}


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

The [thefuzz](https://github.com/seatgeek/thefuzz/) team, you are amazing!

[Syats](https://github.com/syats/) for helping with the hierarchical code.



--------------------------------------------

<p align="right"> You see, most people think that time is a strict progression of cause to effect, but actually, from a non-linear, non-subjective point of view, it’s more like a big ball of... Wibbly-Wobbly... Timey-Wimey... stuff. </p>
<p align="right">The Doctor</p>
<p align="right">The Doctor)
