# WibblyWobbly

## Table of Contents
  - [Overview](#overview)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [Using PIP via PyPI](#using-pip-via-pypi)
  - [Usage](#usage)
    - [Match Data to a Catalog](#match-data-to-a-catalog)
    - [Return a Dictionary](#return-a-dictionary)
    - [Set a `reject_value`.](#set-a-reject_value)
    - [Raise Warnings](#raise-warnings)
    - [Clean a Data Frame Using a Dictionary](#clean-a-data-frame-using-a-dictionary)
    - [Cluster Strings and Create a Rough Catalog](#cluster-strings-and-create-a-rough-catalog)
  - [Versions](#versions)
  - [Acknowledgments](#acknowledgments)

## Overview

A common issue When working with machine learning pipelines is to have data where names and descriptions are full of typos. 

WibblyWobbly is a Python 3 library that finds equivalence between a set of data strings and a strings catalog using fuzzy string matching [FuzzyWuzzy](https://pypi.org/project/fuzzywuzzy/). WibblyWobbly automates matching the data to a catalog while allowing for manual review of suspicious cases and rejecting bad matches. If WibblyWobbly cannot find a good match, it will return the original data.

WibblyWobbly automatically accepts the catalog options with a higher similarity score than a given acceptance threshold (`thr_accept`) and rejects those with a lower score than a given rejection threshold (`thr_reject`). You can adjust these threshold values according to the data quality. WibblyWobbly ignores non-string values.

The default output of WibblyWobbly is a [`pandas`]((https://pandas.pydata.org/)) data frame that you can save as a CSV or Excel file using `dataframe_name.to_excel()`.

## Requirements

-  [Python 3](https://www.python.org/downloads/) or higher
-  [`unidecode`](https://pypi.org/project/Unidecode/): Python package to interpret Unicode.
-  [`pandas`](https://pandas.pydata.org/): Python set of data analysis and manipulation tools.
-  [TheFuzz](https://github.com/seatgeek/thefuzz/): Python package to add fuzzy logic string matching.

An optional dependence is the [python-Levenshtein](https://github.com/ztane/python-Levenshtein/) package for Python. It consists of a set of fast computation functions that may improve the performance time of TheFuzz (and therefore of WibblyWobbly).

## Installation

### Using PIP via PyPI

1. As WibblyWobbly is an extension of TheFuzz, you must download TheFuzz first. To improve performance, install `python-Levenshtein` too. 
   >**Note:** Consider that `python-Levenshtein` has its own dependencies. 
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
        Data Option1  Score1 Option2  Score2 Option3  Score3
   0    CAT      Cat     100    None     NaN    None     NaN
   1   doggo     Dog      90   Mouse    20.0   Human     0.0
   2    mice   Mouse      44     Cat    29.0   Human    22.0
   3  PERSON  PERSON       0    None     NaN    None     NaN
   4     999     999       0    None     NaN    None     NaN
   ```

### Return a Dictionary

To get a dictionary with the best matching options:

1. Run steps 1 and 2 from the section [Match Data to a Catalog](#Match-Data-to-a-Catalog).
2. Use the method `map_list_to_catalog` in your WibblyWobbly instance to match the data with the catalog. Set `output_format="dictionary"`.
   ```python
   ww.map_list_to_catalog(data, catalog, output_format="dictionary")
   {'mice': 'mice', 999: 999, 'doggo': 'Dog', 'PERSON': 'PERSON', 'CAT ': 'Cat'}
   ```
### Set a `reject_value`.

You can assign a reject value to any word that did not match the dictionary with WibblyWobbly by assignining a string value to `reject_value`. You can use the `reject_value` parameter anytime you implement `map_list_to_catalog`. To set a reject value in a dictionary:

1. Run steps 1 and 2 from the section [Match Data to a Catalog](#Match-Data-to-a-Catalog).
2. Use the method `map_list_to_catalog` in your WibblyWobbly instance to match the data with the catalog. Set `output_format="dictionary"` and `reject_value='Other'`.
   ```python
   ww.map_list_to_catalog(data, catalog, output_format="dictionary", reject_value='Other')
   {'mice': 'Other', 999: 999, 'doggo': 'Dog', 'PERSON': 'Other', 'CAT ': 'Cat'}
   ```

### Raise Warnings 
Raising warnings of potential misclassified values facilitate visual inspection. To raise warnings using WibblyWobbly:

1. Run steps 1 and 2 from the section [Match Data to a Catalog](#Match-Data-to-a-Catalog).
2. Use the method `map_list_to_catalog` in your WibblyWobbly instance to match the data with the catalog. Set `output_format="dictionary"` and `warnings=True`.
```python
ww.map_list_to_catalog(data, catalog, output_format="dictionary", 
                           thr_accept=95, thr_reject=40,  warnings=True)
WOBBLY: mice
     	Options: Mouse (44), Cat (29), Human (22)
     WOBBLY: doggo
     	Options: Dog (90), Mouse (20), Human (0)
 
 {'mice': 'Mouse', 999: 999, 'doggo': 'Dog', 'PERSON': 'PERSON', 'CAT ': 'Cat'}
```

### Clean a Data Frame Using a Dictionary 
To use WibblyWobbly to a clean a `pandas` dataframe using a dictionary as reference and the methods `_.replace()` and `_.map()`:
1. Import `wibblywobbly`.
   ```python
   import wibblywobbly as ww
   ```
2. Import `pandas`. Then, load the catalog with `_.read_csv()_` or `_.read_excel()_`.
   ```python
   import pandas as pd
   df_catalog = pd.read_csv("./tests/example_taxa.csv")
   df_catalog
   Common name      Order           Family    Genus      Species
   0      Guinea pig   Rodentia         Caviidae    Cavia    porcellus
   1           Mouse   Rodentia          Muridae      Mus     musculus
   2             Rat   Rodentia          Muridae   Rattus   norvegicus
   3             Cat  Carnivora          Felidae    Felis        catus
   4             Dog  Carnivora          Canidae    Canis        lupus
   5  Rhesus macaque   Primates  Cercopithecidae   Macaca      mulatta
   6      Chimpanzee   Primates        Hominidae      Pan  troglodytes
   7         Gorilla   Primates        Hominidae  Gorilla      gorilla
   8       Orangutan   Primates        Hominidae    Pongo    pygmaeus
   9           Human   Primates        Hominidae     Homo      sapiens
   ```
3. Load the data table with `_.read_csv()_` or `_.read_excel()_`.
   ```python
   df_data = pd.read_csv("./tests/example_dirty_name.csv")
   df_data
           Animal  Count
   0         mice      3
   1         CAT       1
   2        doggo      5
   3       PERSON      0
   4   guinea pig      1
   5          pig      2
   6      Gorilla      3
   7   Chimpanzee      0
   8    orangután      1
   9    chinpanze      7
   10      gorila      3
   11         NaN      6
   12        dogs      2
   13        rats     12
   14       mouse      1
   15       kitty      3
   16         Cat      2
   17      macaco      1
   ```
4. Create two lists. One with the columns you want to use as catalog and another with the data using `_.to_list()_`.
   ```python
   catalog = df_catalog["Common name"].to_list()
   print('Catalog: ', catalog)
   Catalog:  ['Guinea pig', 'Mouse', 'Rat', 'Cat', 'Dog', 'Rhesus macaque', 'Chimpanzee', 'Gorilla', 'Orangutan', 'Human']

   data = df_data["Animal"].to_list()
   print('Data: ', data)
   Data:  ['mice', 'CAT ', 'doggo', 'PERSON', 'guinea pig', 'pig', 'Gorilla', 'Chimpanzee', 'orangután', 'chinpanze', 'gorila', nan, 'dogs', 'rats', 'mouse', 'kitty', 'Cat', 'macaco']
   ```
5. Create an equivalence dictionary using `map_list_to_catalog`. Set `output_format="dictionary"`, to get a dictionary and `warnings=True` to check the results.
   >**Note:**
   You may need to adjust `thr_accept` and `thr_reject` to get better results.
   ```python
   equivalence = ww.map_list_to_catalog(data, catalog, output_format="dictionary", thr_accept=80, thr_reject=50, warnings=True)
   REJECT: PERSON
        Options: Rhesus macaque (43), Rat (30), Chimpanzee (30)
   REJECT: kitty
        Options: Rat (30), Cat (30), Guinea pig (18)
   REJECT: mice
        Options: Guinea pig (45), Rhesus macaque (45), Mouse (44)
   WOBBLY: macaco
        Options: Cat (60), Rhesus macaque (60), Mouse (36)
   
   equivalence
   {'Gorilla': 'Gorilla', 'pig': 'Guinea pig', 'guinea pig': 'Guinea pig', 'PERSON': 'PERSON', 'orangután': 'Orangutan', 'doggo': 'Dog', 'mouse': 'Mouse', 'Cat': 'Cat', 'dogs': 'Dog', 'Chimpanzee': 'Chimpanzee', 'chinpanze': 'Chimpanzee', 'kitty': 'kitty', 'mice': 'mice', 'macaco': 'Cat', 'rats': 'Rat', 'CAT ': 'Cat', nan: nan, 'gorila': 'Gorilla'}
   ```
6. Correct the `equivalence` dictionary by changing manually the values assigned by WibblyWobbly.
   ```python
   equivalence['macaco'] = 'Rhesus macaque'
   equivalence['kitty']  = 'Cat'
   equivalence['PERSON'] = 'Human'
   equivalence['mice']   = 'Mouse'
   equivalence
   {'Gorilla': 'Gorilla', 'pig': 'Guinea pig', 'guinea pig': 'Guinea pig', 'PERSON': 'Human', 'orangután': 'Orangutan', 'doggo': 'Dog', 'mouse': 'Mouse', 'Cat': 'Cat', 'dogs': 'Dog', 'Chimpanzee': 'Chimpanzee', 'chinpanze': 'Chimpanzee', 'kitty': 'Cat', 'mice': 'Mouse', 'macaco': 'Rhesus macaque', 'rats': 'Rat', 'CAT ': 'Cat', nan: nan, 'gorila': 'Gorilla'}
   ```
7. Clean de data using the equivalence dictionary in the function `_.map()_`. Overwrite the values.
   ```python
   df_data['Animal'] = df_data['Animal'].map(equivalence)
   df_data
               Animal  Count
   0            Mouse      3
   1              Cat      1
   2              Dog      5
   3            Human      0
   4       Guinea pig      1
   5       Guinea pig      2
   6          Gorilla      3
   7       Chimpanzee      0
   8        Orangutan      1
   9       Chimpanzee      7
   10         Gorilla      3
   11             NaN      6
   12             Dog      2
   13             Rat     12
   14           Mouse      1
   15             Cat      3
   16             Cat      2
   17  Rhesus macaque      1
   ```
8. Save the clean table as a new file using either `_.to_csv()_` or `_.to_excel()_`.
   ```python
   df_data.to_csv("./tests/example_clean_name.csv")
   ```

### Cluster Strings and Create a Rough Catalog

To use WibblyWobbly as a rough clustering algorithm:
1. Import `wibblywobbly`.
   ```python
   import wibblywobbly as ww
   ```
2. Load the data table using either `_.read_csv()_` or `_.read_excel()_` method.
   ```python
   df_data = pd.read_csv("./tests/example_dirty_name.csv")
   df_data
           Animal  Count
   0         mice      3
   1         CAT       1
   2        doggo      5
   3       PERSON      0
   4   guinea pig      1
   5          pig      2
   6      Gorilla      3
   7   Chimpanzee      0
   8    orangután      1
   9    chinpanze      7
   10      gorila      3
   11         NaN      6
   12        dogs      2
   13        rats     12
   14       mouse      1
   15       kitty      3
   16         Cat      2
   17      macaco      1
   ```
3. Convert the data frame to list.
   ```python
   df_data['Animal'].to_list()
   ['mice', 'CAT ', 'doggo', 'PERSON', 'guinea pig', 'pig', 'Gorilla', 'Chimpanzee', 'orangután', 'chinpanze', 'gorila', nan, 'dogs', 'rats', 'mouse', 'kitty', 'Cat', 'macaco']
   ```
4. Set a random seed for the clustering algorithm.
   ```python
   import random
   random.seed(10)
   ```
5. Group the strings whose Levenshtein distance is higher than `thr_accept` using `_.cluster_strings()`.  
   >**Note:**
   This is a rough algorithm. Once a cluster forms, none of its elements will belong to another cluster.
   ```python
   ww.cluster_strings(df_data['Animal'])
   [['pig', 'guinea pig'], ['mouse'], ['Cat', 'CAT '], ['Chimpanzee'], ['Gorilla', 'gorila'], ['PERSON'], ['macaco'], ['mice'], ['orangután'], ['doggo'], ['kitty'], ['chinpanze'], ['rats']]
   ```
6. To change the number maximum number of elements (x) in the cluster set `max_options=x`:
   ```python
   ww.cluster_strings(df_data['Animal'], thr_accept=75, max_options=1)
   ['Cat', 'kitty', 'doggo', 'Gorilla', 'mouse', 'guinea pig', 'Chimpanzee', 'macaco', 'rats', 'PERSON', 'dogs', 'mice']
   ```
   > **Note:** This can be used as a very rough method to infer a catalog.

## Versions
- 0.3.0
  - Includes performance improvements. 
- 0.2.0
  - Uses theFuzz.
  - Includes a rough clustering algorithm.
  - Includes hierarchical dictionaries.

- 0.1.0
  - This is the first WibblyWobbly version online!
  - Includes basic operations to match list to catalogs.

## Acknowledgments
Thank you, [TheFuzz](https://github.com/seatgeek/thefuzz/) team. You are amazing!

Thank you, [Syats](https://github.com/syats/) for helping with the hierarchical code.

---
>People assume that time is a strict progression of cause to effect, but actually from a non-linear, non-subjective point of view, it’s more like a big ball of wibbly-wobbly, timey-wimey stuff. </p>
<p align="right">The Doctor</p>
