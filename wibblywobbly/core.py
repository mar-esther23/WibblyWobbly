import logging
from pandas import DataFrame
from fuzzywuzzy import process

from unidecode import unidecode
from re import sub as resub
import warnings

def map_list_to_catalog(data, catalog, result="dictionary", thr_reject=50, reject_value=None, max_options=3, warnings=False, thr_warn=90):
    """
    Create an equivalence dictionary between data and a catalog.

    Take a 'data' list of dirty strings that will be mapped to a 'catalog' and return the equivalence dictionary with that mapping. Obtains a list of options with similarity scores. Uses fuzzywuzzy.process.extract().
    
    Parameters
    ----------
    data: list of str
        List of strings with the data to be mapped to the catalog
    catalog: list of str
        Catalog
    result: ["dictionary", "dataframe"]
        if "dictionary" returns an dictionary { data_item : catalog_item }
        if "dataframe" returns a pandas DataFrame where the first columns is the data and the following columns are the top options and their scores
    thr_reject: int, default '50'
        Treshold value for rejection. If the top score is lower than this value no equivalence to the catalog will be created and the equivalence will be replaced by reject_value.
    reject_value: str, default 'None'
        Value that will be return in "dictionary" if the score is lower than thr_reject.
    max_options: int, default 3
        Number of options to display
    warnings: bool
        if True raises warnings with top options if the top score is lower than thr_warn
    thr_warn: int, default '90'
        Treshold value for manual revision.


    Returns
    -------
    dictionary
        Dictionary that allows mapping options to the catalog

    Examples
    --------
    """

    def save(item, options):
        """
        item: str
        options: [(), ... ]
        """
        if result=="dictionary": 
            res[item] = options[0][0] #save best
        if result=="dataframe":
            options = unnest(options)
            res.append( [item] + options )

    def unnest(l):
        return [i for sub in l for i in sub]

    if result=="dictionary": res = {}
    elif result=="dataframe": res = []
    else: raise NameError("result should be 'dictionary' or 'dataframe'")

    #Format and save to dic to return to original values
    data_ = list(set(data))
    catalog_ = list(set(catalog))
    catalog_ = {simplify_string(s):s for s in catalog_}

    #iterate
    for item in data_:
        #check type
        if type(item)!=str: save(item, [(item,0)])
        else:
            #compare with catalog
            options = process.extract(simplify_string(item), 
                                      catalog_.keys(), 
                                      limit=max_options)
            # reverse simplify_string in catalog
            options = [(catalog_[i[0]],i[1]) for i in options]
            # check score
            top_score = options[0][1]
            if top_score<=thr_reject: #reject 
                if warnings: warn_review("REJECT", item, options)
                if result=="dictionary" :
                    if reject_value==None:
                        options = [(item,0)]
                    if reject_value!=None:
                        options = [(reject_value,0)]
            elif warnings and top_score<=thr_warn: #warning
                    warn_review("WOBBLY", item, options)
            save(item,options)

    # convert to dataframe
    if result=="dataframe":
        res = DataFrame(res)
        # create column names
        cols = [str(i+1) for i in range(max_options)]
        cols = [["Option"+i, "Score"+i] for i in cols]
        res.columns = ['Data'] + unnest(cols)
        # sort
        res = res.sort_values("Score1", ascending=False) \
                 .reset_index(drop=True)
    return res
    

def simplify_string(text):
    """Simplify a string to remove special characters, double spaces and use lower case."""
    text = text.lower()
    text = ' '.join([t for t in text.split()])
    text = unidecode(text)
    text = resub(r"[^a-zA-Z0-9]+", ' ', text)
    text = ' '.join([t for t in text.split()]) #paranoia
    return text

def warn_review(category, item, options):
    def warn_text(message, category='', filename='', lineno='', line=''):
        return str(message)
    # create message
    options = ', '.join(["{} ({})".format(*i) for i in options])
    message = "{}: {}\n\tOptions: {}\n".format( category, item, options )
    # raise warning
    warnings.formatwarning = warn_text
    warnings.warn(message)

    