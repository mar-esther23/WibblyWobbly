import logging
import pandas as pd
from fuzzywuzzy import process

from unidecode import unidecode
from re import sub as resub
import warnings

def map_list_to_catalog(data, catalog, 
    thr_warn=90, max_options=3, thr_reject=50, reject_value=None):
    """
    Create an equivalence dictionary between data and a catalog.

    Take a 'data' list of dirty strings that will be mapped to a 'catalog' and return the equivalence dictionary with that mapping. It generates warnings if the data has low similarity to the catalog. Uses fuzzywuzzy.process.extract ().
    
    Parameters
    ----------
    data: list of str
        List of strings with the data to be mapped to the catalog
    catalog: list of str
        Catalog
    thr_warn: int, default '90'
        Treshold value for manual revision. If the similarity between the item and the best match of the catalog is lower than this value a warning with the best options will be shown.
    max_options: int, default 2
        Number of options to display if low similarity
    thr_reject: int, default '50'
        Treshold value for rejection. If the similarity between the item and the best match of the catalog is lower than this value no equivalence to the catalog will be created and the equivalence will be replaced by reject_value.
    reject_value: str, default 'None'
        A value that is returned if there is no minimum similarity between the string and the catalog. If 'None' the original string value is returned.


    Returns
    -------
    dictionary
        Dictionary that allows mapping options to the catalog

    Examples
    --------
    """

    #Format
    data_ = list(set(data))
    data_ ={simplify_string(s):s for s in data_}
    catalog_ = list(set(catalog))
    catalog_ ={simplify_string(s):s for s in catalog_}
    warnings.formatwarning = warn_review

    s_dic = {}
    ignorados = {}
    #verify if reject_value exists in catalog
    if reject_value!=None:
        catalog_[reject_value]=reject_value
    for i in data_.keys():
        # ignore if not a string
        if type(i)!=str: 
            if reject_value==None: s_dic[i]=i
            else: s_dic[i]=reject_value
        else:
            # compare with catalog using fuzzywuzzy
            val = process.extract(i, catalog_.keys())
            top_option, top_value = val[0]
            # Reject
            if top_value <= thr_reject: 
                warning.warn(val, 'REJECT', max_options=max_options)
                catalog_[i] = data_[i] #save item
                if reject_value==None: s_dic[i]=i
                else: s_dic[i]=reject_value
            else: 
                # low similarity
                if thr_reject < top_value <= thr_warn:
                    warning.warn(val, 'WOBBLY', max_options=max_options)
                s_dic[i] = top_option

    # Return to original string format
    s_dic = {data_[k]:catalog_[v] for k,v in s_dic.items() }
    return s_dic

def simplify_string(text):
    """Simplify a string to remove special characters, double spaces and use lower case."""
    text = text.lower()
    text = ' '.join([t for t in text.split()])
    text = unidecode.unidecode(text)
    text = resub(r"[^a-zA-Z0-9]+", ' ', text)
    text = ' '.join([t for t in text.split()]) #paranoia
    return text

def warn_review(message, category, 
                filename='', lineno='', line='',
                max_options=3):
    max_options = min(len(message), max_options)
    message = message[0:max_options]
    options = ', '.join(["{} ({})".format(*i) for i in message])
    warn_message = "{}: {}\n\tOptions: {}".format( category, i, options )
    return warn_message
