import warnings
import logging

from pandas import DataFrame
from thefuzz import process
from unidecode import unidecode
from random import shuffle
from re import sub as resub

def unnest(l):
        return [i for sub in l for i in sub]


def simplify_string(text):
    """Simplify a string to remove special characters, double spaces and use lower case.

    Parameters
    ----------
    text: str
        string to clean

    Returns
    -------
    str

    Examples
    --------
    >>> text = ' (S . cerevisiáe  )'
    >>> simplify_string(text)
    's cerevisiae'

    """
    text = text.lower()
    text = ' '.join([t for t in text.split()])
    text = unidecode(text)
    text = resub(r"[^a-zA-Z0-9]+", ' ', text)
    text = ' '.join([t for t in text.split()]) #paranoia
    return text


def warn_review(category, item, options):
    """
    Overwrite formatwarning to simplify options evaluation.
    """
    def warn_text(message, category='', filename='', lineno='', line=''):
        return str(message)
    # create message
    options = ', '.join(["{} ({})".format(*i) for i in options])
    message = "{}: {}\n\tOptions: {}\n".format( category, item, options )
    # raise warning
    warnings.formatwarning = warn_text
    warnings.warn(message)



def map_list_to_catalog(data, catalog, output_format="dataframe", 
                        thr_accept=90, thr_reject=75, reject_value=None,
                        max_options=3, warnings=False, simplify=True):
    """
    Create an equivalence dictionary between data and a catalog.

    Take a 'data' list of dirty strings that will be mapped to a 'catalog' and return the equivalence dictionary with that mapping. Obtains a list of options with similarity scores. Uses fuzzywuzzy.process.extract().
    
    Parameters
    ----------
    data: list of str
        List of strings with the data to be mapped to the catalog
    catalog: list of str
        Catalog
    output_format: "dataframe" or "dictionary"
        If "dataframe" returns a pandas DataFrame where the first columns is the data and the following columns are the options and their scores
        If "dictionary" returns an dictionary { data_item : catalog_item }
    thr_accept: int, default '90'
        Treshold value for acceptance. If the top score is higher than this the top value will be assigned and no options shown
    thr_reject: int, default '75'
        Treshold value for rejection. If the top score is lower than this value no equivalence to the catalog will be created and the equivalence will be replaced by reject_value
    reject_value: str, default 'None'
        Value that will be return in "dictionary" if the score is lower than thr_reject
    max_options: int, default 3
        Number of options to display
    warnings: bool
        If True raises warnings for values between thr_accept and thr_reject
    simplify: bool
        Simplify every string before comparison to improve score


    Returns
    -------
    dataframe 
        pandas DataFrame where the first column is the data and the following columns are the options and their scores
    dictionary
        Dictionary that allows mapping options to the catalog

    Examples
    --------
    >>> catalog = ["Mouse", "Cat", "Dog", "Human"]
    >>> data = ["mice",  "CAT ", "doggo", "PERSON", 999]
    >>> ww.map_list_to_catalog(data, catalog, thr_accept=95, thr_reject=40)
        Data    Option1     Score1  Option2     Score2  Option3     Score3
    0   CAT     Cat     100     None    NaN     None    NaN
    1   doggo   Dog     90  Mouse   20.0    Human   0.0
    2   mice    Mouse   44  Cat     29.0    Human   22.0
    3   PERSON  PERSON  0   None    NaN     None    NaN
    4   999     999     0   None    NaN     None    NaN

    >>> ww.map_list_to_catalog(data, catalog, output_format="dictionary", reject_value='Other')
    {'mice':'Other', 999:999, 'doggo':'Dog', 'PERSON':'Other', 'CAT ':'Cat'}

    """

    
    if thr_reject>=thr_accept:
        raise ValueError("Invalid threshold values")
    if output_format=="dictionary": res = {}
    elif output_format=="dataframe": res = []
    else:raise NameError("output_format should be 'dictionary' or 'dataframe'")

    #Format and save to dic to return to original values
    data_ = list(set(data))
    catalog_ = list(set(catalog))
    if simplify:
        catalog_ = {simplify_string(s):s for s in catalog_}

    #iterate
    for item in data_:
        #check type
        if type(item)!=str: 
            options = [(item,0)]
        else:
            if simplify:
                options = process.extract( simplify_string(item), catalog_.keys(), limit=max_options )
                options = [ ( catalog_[i[0]] , i[1] ) for i in options]
            else: 
                options = process.extract(item, catalog_, limit=max_options)
            top_score = options[0][1]
            if top_score>=thr_accept:
                options = [options[0]]
            elif top_score<thr_reject:
                if warnings:
                    warn_review("REJECT", item, options)
                if reject_value==None: options = [(item,0)]
                else: options = [(reject_value,0)]
            elif warnings:
                warn_review("WOBBLY", item, options)
        logging.info(item,options)
        if output_format=="dataframe":
            res.append( [item]+unnest(options) )
        if output_format=="dictionary":
            res[item]=options[0][0]

    # convert to dataframe
    if output_format=="dataframe":
        res = DataFrame(res)
        # create column names
        n_cols = int( (len(res.columns)+1)/2 )
        cols = [str(i) for i in range(1,n_cols)]
        cols = [["Option"+i, "Score"+i] for i in cols]
        res.columns = ['Data'] + unnest(cols)
        # sort
        res = res.sort_values(["Score1","Data"], ascending=[False,False]) \
                 .reset_index(drop=True)
    return res



def cluster_strings(data, thr_accept=90, max_options=None, simplify=True, randomize=True):
    """
    Cluster similar strings.

    Take a 'data' list of strings and create clusters of those whose levenshtein distance is higher than thr_accept. This is a rough algoritm, once a cluster has been formed none of its elements will belong to an other cluster.
    
    Parameters
    ----------
    data: list of str
        List of strings with the data to be mapped to the catalog
    thr_accept: int, default '90'
        Treshold value for acceptance. If the top score is higher than this the top value will be assigned and no options shown
    max_options: int, default None
        Number of elementos of cluster to return. If None returns all options, else it returns N options.
    simplify: bool
        Simplify every string before comparison to improve score
    simplify: bool
        Shuffle data, the order of the list affects cluster formation.


    Returns
    -------
    list of lists
        List of lists where each list contains the strings that clustered together by levenshtein distance.

    Examples
    --------
    >>> catalog = ["Mouse", "Cat", "Dog", "Human"]
    >>> data = ["mice",  "CAT ", "doggo", "PERSON", 999]
    >>> ww.map_list_to_catalog(data, catalog, thr_accept=95, thr_reject=40)
        Data    Option1     Score1  Option2     Score2  Option3     Score3
    0   CAT     Cat     100     None    NaN     None    NaN
    1   doggo   Dog     90  Mouse   20.0    Human   0.0
    2   mice    Mouse   44  Cat     29.0    Human   22.0
    3   PERSON  PERSON  0   None    NaN     None    NaN
    4   999     999     0   None    NaN     None    NaN

    >>> ww.map_list_to_catalog(data, catalog, output_format="dictionary", reject_value='Other')
    {'mice':'Other', 999:999, 'doggo':'Dog', 'PERSON':'Other', 'CAT ':'Cat'}

    """
    if simplify: # create a dictionary of strings that have been simplified to the same place
        dic_simple = {}
        for old in set(data):
            if type(old)==str:
                new = simplify_string(old)
                if new in dic_simple.keys():
                    dic_simple[new].append(old)
                else: dic_simple[new] = [old]
        logging.info("Save string simplification {}".format(dic_simple))
        data_ = list(dic_simple.keys())
    else: data_ = list(set(data))

    # because list order affects cluster formation
    if randomize: shuffle(data_)
    
    # group if similar enough
    groups = []
    while len(data_)>1:
        target = data_.pop()
        if type(target)==str:
            group = process.extract(target,data_)
            group = [t for t,s in group if s>=thr_accept]
            for s in group: #don't match twice
                data_.remove(s)
        else: group = []
        groups.append([target] + group)
    logging.info("Group by fuzz distance {}".format(groups))
    
    if simplify:
        groups = [[dic_simple[g] for g in group] for group in groups]
        groups = [unnest(group) for group in groups]
        logging.info("Return to original string {}".format(groups))
    
    if max_options!=None:
        groups = [group[0:max_options] for group in groups]
        if max_options==1:
            groups = [group[0] for group in groups]
        logging.info("Return only top N options {}".format(groups))
    
    return(groups)

    



    