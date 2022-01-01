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

