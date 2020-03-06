WibblyWobbly
============

Python library to create equivalence dictionaries between a set of texts and a catalog using FuzzyWuzzy.

It is a common nightmare for data scientist, your human users captured the data according to a catalog but it is full of mistakes. WibblyWobbly automates the task of automatically matching the data to a catalog while allowing for manual review of suspicious cases and rejecting bad matches.

Requirements
------------

-  Python 3 or higher
-  fuzzywuzzy
-  python-Levenshtein (optional)
-  unidecode
-  pandas

Instalation
-----------

Using PIP via PyPI

.. code:: sh

   pip install wibblywobbly

WibblyWobbly extends fuzzywuzzy, it is recomended to install python-Levenshtein too

.. code:: sh

   pip install fuzzywuzzy[speedup]

Manually via GIT

.. code:: sh

   git clone git://github.com/mar-esther23/wibblywobbly.git wibblywobbly
   cd fuzzywuzzy
   python setup.py install

Usage
-----

Match data to a catalog
~~~~~~~~~~~~~~~~~~~~~~~

Import wibblywobbly and load your data and catalog as list. If you are using pandas use *.to_list()*.

.. code:: python3

    import wibblywobbly as ww
    
    catalog = ["Mouse", "Cat", "Dog", "Human"]
    data = ["mice",  "CAT ", "doggo", "PERSON", 999]



WibblyWobbly compares the data to the catalog and returns the most likely options and a similarity score. If it cannot find a good match it will return the original data.

It automaticaly accepts the catalog options that have a higher similarity score than ``thr_accept`` and rejects those that have a lower score than ``thr_reject``. This treshold values can be adjusted depending in the data quality. It ignores non-string values.

By default it returns a pandas dataframe that can be saved as a csv or excel file *.to_excel()*.



.. code:: python3

    ww.map_list_to_catalog(data, catalog, thr_accept=95, thr_reject=40)

.. raw:: html

    <div>
    <table border="0" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th> <th>Data</th> <th>Option1</th> <th>Score1</th> <th>Option2</th> <th>Score2</th> <th>Option3</th> <th>Score3</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>0</td> <td>CAT</td> <td>Cat</td> <td>100</td> <td>None</td> <td>NaN</td> <td>None</td> <td>NaN</td>
        </tr>
        <tr>
          <td>1</td> <td>doggo</td> <td>Dog</td> <td>90</td> <td>Mouse</td> <td>20.0</td> <td>Human</td> <td>0.0</td>
        </tr>
        <tr>
          <td>2</td> <td>mice</td> <td>Mouse</td> <td>44</td> <td>Cat</td> <td>29.0</td> <td>Human</td> <td>22.0</td>
        </tr>
        <tr>
          <td>3</td> <td>PERSON</td> <td>PERSON</td> <td>0</td> <td>None</td> <td>NaN</td> <td>None</td> <td>NaN</td>
        </tr>
        <tr>
          <td>4</td> <td>999</td> <td>999</td> <td>0</td> <td>None</td> <td>NaN</td> <td>None</td> <td>NaN</td>
        </tr>
      </tbody>
    </table>
    </div>



WibblyWobbly can also return a dictionary with the best options. This dictionary can be used to clean a pandas dataframe with *.replace()* and *.map()*.

.. code:: python3

    ww.map_list_to_catalog(data, catalog, output_format="dictionary")




.. parsed-literal::

    {'mice': 'mice', 999: 999, 'doggo': 'Dog', 'PERSON': 'PERSON', 'CAT ': 'Cat'}



It is possible set a ``reject_value``.

.. code:: python3

    ww.map_list_to_catalog(data, catalog, output_format="dictionary", reject_value='Other')




.. parsed-literal::

    {'mice': 'Other', 999: 999, 'doggo': 'Dog', 'PERSON': 'Other', 'CAT ': 'Cat'}



WibblyWobbly can also raise warnings of the suspicious values to facilitate visual inspection.

.. code:: python3

    ww.map_list_to_catalog(data, catalog, output_format="dictionary", 
                           thr_accept=95, thr_reject=40,  warnings=True)


.. parsed-literal::

    WOBBLY: mice
    	Options: Mouse (44), Cat (29), Human (22)
    WOBBLY: doggo
    	Options: Dog (90), Mouse (20), Human (0)




.. parsed-literal::

    {'mice': 'Mouse', 999: 999, 'doggo': 'Dog', 'PERSON': 'PERSON', 'CAT ': 'Cat'}



Versions
--------

-  0.1.0

   -  We are online!
   -  Basic operations to match list to catalogs

Thanks
------

The `FuzzyWuzzy <https://github.com/seatgeek/fuzzywuzzy>`__ team, you are amazing!

`Syats <https://github.com/syats/>`__ for helping with the hierarchical code.

.. 

        You see, most people think that time is a strict progression of cause to effect, but actually, from a non-linear, non-subjective point of view, it’s more like a big ball of…Wibbly-Wobbly…Timey-Wimey…stuff.
        (The Doctor)
