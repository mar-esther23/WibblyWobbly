import pandas as pd

def list_to_nestdic(l, as_list=False):
    """
    Takes an iterable and returns a nested dic.
    If the iterable len is 1, returns the element.
    
    Examples
    --------
    >>> list_to_dic([1,2,3,4])
    {1: {2: {3: 4}}}
    >>> list_to_dic([1])
    1
    """
    dic = l.pop()
    if as_list: dic=[dic]
    while True:
        try: dic={l.pop():dic}
        except IndexError: break
    return dic

def create_hierarchical_catalog(df):
    # love
    from functools import reduce
    from operator import getitem
    # sort
    df.sort_values(df.columns.to_list())
    # initial data
    data = df.iloc[0].to_list()
    old  = df.iloc[0].to_list()
    data = list_to_nestdic(data)
    dic  = data
    # iterate
    for row in df.iloc[1:].iterrows():
        data = row[1].to_list()
        # compare and slice
        last_equal = [i==j for i,j in zip(data,old)].index(False) - 1
        if last_equal==-1:
            info = None
            poin = dic
        else: 
            info = reduce(getitem, data[0:last_equal], dic)
            poin = data[last_equal]
        data = list_to_nestdic(data[last_equal+1:])
        # create
        if info==None: dic.update(data)
        else: info[poin].update(data)
        # next
        old = row[1].to_list()
    return dic



import warnings


def warn_text(message, category='', filename='', lineno='', line=''):
    return str(message)

def warn_review(category, item, options):
    """
    Overwrite formatwarning to simplify options evaluation.
    """
    # create message
    options = ', '.join(["{} ({})".format(*i) for i in options])
    message = "{}: {}\n\tOptions: {}\n".format( category, item, options )
    # raise warning
    warnings.formatwarning = warn_text
    warnings.warn(message)

def get_list_from_hierarchical_catalog_keys(catalog, keys=None, error=[]):
    catl = catalog
    # check keys
    if keys!=None:
        if type(keys) not in [list,tuple]: keys = [keys]
        for k in keys:
            if k in catl.keys():
                catl = catl[k]
            else:
                message =  "NameError: '{}' not in catalog. Retuning: {}\n\tKeys: {}\n".format(k, error, keys)
                warnings.formatwarning = warn_text
                warnings.warn(message)
                catl = error
    # simplify to list
    if type(catl)==dict: catl = catl.keys()
    return catl

def map_hierarchical_catalog(df, catalog, target=0, keys=None, **kwargs):
    if keys==None: #not a hierarchical clasify
        grouped = [(None,df)]
    else: grouped = df.groupby(keys)
    res = []
    for name, group in grouped:
        logging.info('Target: '+str(target)+'\tGroup: ' + str(name) +'\tSize: ' +str(group.size))
        data = group[target]
        catl = get_list_from_hierarchical_catalog_keys(catalog, keys=name)
        if len(catl)>0:
            catl = ww.map_list_to_catalog(data, catl, output_format="dictionary", **kwargs)
        if len(catl)>0:
            data = data.replace( catl )
        res.append( data )
    logging.info(res)
    res = pd.concat(res)
    return res
