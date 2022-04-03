# WibblyWobbly

## Overview

Oerview
When working with machine learning pipelines, a common issue is having data matched to a catalog where the classification is full of mistakes. 

WibblyWobbly is a Python 3 library that finds equivalence between a set of data strings and a strings catalog using fuzzy string matching [FuzzyWuzzy](https://pypi.org/project/fuzzywuzzy/). WibblyWobbly automates matching the data to a catalog while allowing for manual review of suspicious cases and rejecting bad matches. If WibblyWobbly cannot find a good match, it will return the original data.

WibblyWobbly automatically accepts the catalog options with a higher similarity score than a given acceptance threshold (`thr_accept`) and rejects those with a lower score than a given rejection threshold (`thr_reject`). These threshold values can be adjusted depending on the data quality. WibblyWobbly ignores non-string values.

The default output of WibblyWobbly is a pandas data frame that you can save as a CSV or excel file using `dataframe_name.to_excel()`.

## Requirements

-  [Python 3](https://www.python.org/downloads/) or higher
-  [`unidecode`](https://pypi.org/project/Unidecode/): Python package
-  [`pandas`](https://pandas.pydata.org/): Python set of data analysis and manipulation tools 
-  [theFuzz](https://github.com/seatgeek/thefuzz/): Python package

Additionally, you may want to get the [python-Levenshtein](https://github.com/ztane/python-Levenshtein/) package for Python. It consists of a set of fast computation functions that may improve the performance time of theFuzz (and therefore of WibblyWobbly).

## Installation

### Using PIP via PyPI

1. As WibblyWobbly is an extension of Thefuzz, you must download Thefuzz first. To improve performance, install `python-Levenshtein` too. Consider that `python-Levenshtein` has its own dependencies. 
   ```python
   pip install thefuzz
   pip install python-Levenshtein #optional
   ```
2. Install WibblyWobbly.
   ```python
   pip install wibblywobbly
   ```

## Usage

### Match Data to a Catalog

To match data to a catalog:

1. Import `wibblywobbly`.
   ```python
   import wibblywobbly as ww
   ```
2. Load your data and catalog as lists (if you are using pandas use `.to_list()`.)
   ```python
   catalog = ["Mouse", "Cat", "Dog", "Human"]
   data = ["mice",  "CAT ", "doggo", "PERSON", 999]
   ```
3. Use the method `map_list_to_catalog` in your WibblyWobbly instance to match the data with the catalog in a pandas dataframe.
   ```python
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

### Return a Dictionary

To get a dictionary with the best options:

1. Run steps one and two from the section [Match Data to a Catalog](#Match-Data-to-a-Catalog).
2. Use the method `map_list_to_catalog` in your WibblyWobbly instance to match the data with the catalog. Set `output_format="dictionary"`.
   ```python
   ww.map_list_to_catalog(data, catalog, output_format="dictionary")
   >> {'mice': 'mice', 999: 999, 'doggo': 'Dog', 'PERSON': 'PERSON', 'CAT ': 'Cat'}
   ```
   

 This dictionary can be used to clean a pandas dataframe with `.replace()` and `.map()`.

### Set a `reject_value`.

You can assign a reject value to any word that did not match the dictionary with WibblyWobbly. To set a reject value:

1. 1. Run steps one and two from the section [Match Data to a Catalog](#Match-Data-to-a-Catalog).
2. Use the method `map_list_to_catalog` in your WibblyWobbly instance to match the data with the catalog. Set `output_format="dictionary"` and `reject_value='Other'`.
   ```python
   ww.map_list_to_catalog(data, catalog, output_format="dictionary", reject_value='Other')
   >> {'mice': 'Other', 999: 999, 'doggo': 'Dog', 'PERSON': 'Other', 'CAT ': 'Cat'}
   ```

### Raise Warnings
WibblyWobbly can also raise warnings of the suspicious values to facilitate visual inspection.

```python
ww.map_list_to_catalog(data, catalog, output_format="dictionary", 
                           thr_accept=95, thr_reject=40,  warnings=True)
>> WOBBLY: mice
     	Options: Mouse (44), Cat (29), Human (22)
     WOBBLY: doggo
     	Options: Dog (90), Mouse (20), Human (0)
 
 {'mice': 'Mouse', 999: 999, 'doggo': 'Dog', 'PERSON': 'PERSON', 'CAT ': 'Cat'}
```

## Versions
--------

-  0.2.0
   - Uses theFuzz
   - Includes a rough clustering algorithm
   - Includes hierarchical dictionaries

- 0.1.0
   - We are online!
   - Includes basic operations to match list to catalogs

## Acknowledgements
------

Thank you [theFuzz](https://github.com/seatgeek/thefuzz/) team. You are amazing!

Thank you [Syats](https://github.com/syats/) for helping with the hierarchical code.



--------------------------------------------

>You see, most people think that time is a strict progression of cause to effect, but actually, from a non-linear, non-subjective point of view, it’s more like a big ball of... Wibbly-Wobbly... Timey-Wimey... stuff. </p>
<p align="right">The Doctor</p>
