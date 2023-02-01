#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

#######################################################################################


@mpl.rc_context({'axes.labelsize': 15, })
def moments_plot(data, order, bins=300, row='var', column='order', palette='flare', **kwargs):
    """ This function plots the statistical moments of the given orders for a given data.

    :param data: the array of time-series, each column corresponds to a time-serie
    :type data: nd-array of shape (n, dims)
                in which n is the number of time points and dims is the dimension of data (number of time-series)
    :param order: the order(s) of statistical moments to be plotted.
    :type order: an integer or an array-like
    :param bins: If bins is an int, it defines the number of equal-width bins in the given range (10, by default) 
                 If bins is a sequence, it defines the bin edges, including the rightmost edge, allowing for 
                 non-uniform bin widths. If bins is a string from the list {‘auto’, ‘fd’, ‘doane’, ‘scott’, 
                 ‘rice’, ‘sturges’, ‘sqrt’}, it selects the method used to calculate the optimal bin width; 
                 (optional, default: 300)
    :type bins: int or array-like or str
    :param row: the name of column which is used for row of facetgrid, can only be 'var' or 'order';
              if row='var', each line of facetgrid belongs to one of the time-series, 
              if row='order', each line of facetgrid belongs to one of the given orders. (optional, default='var')
    :type row: str
    :param column: the name of column which is used for column of facetgrid, 
                   can only be 'var' or 'order' and should be different from the value of 'row';
                   if row='var', each line of facetgrid belongs to one of the time-series, 
                   if row='order', each line of facetgrid belongs to one of the given orders. 
                   (optional, default='order')
    :type column: str
    :param palette: passed to sns.relplot as a palette. (optional, default='flare')
    :type palette: a seaborn palette 
    

    ---------------
    :return: sns.relplot
    """

    ######################################## assertions ########################################

    assert ((row in ['var', 'order'] and column in ['var', 'order']) and row!=column),\
    f"row and column must be different and be one of the ['var', 'order'] but got {row} and {column}."
    assert len(data.shape) == 2, ValueError('time series must have (n_time_serie, dims) shape')
    assert data.shape[0] > 0, ValueError('no data in time series')
    assert (np.array(order) >= 0).all(), ValueError('nagative order is given')
    
    ############################################################################################

    if type(order) == int:
        order = [order]

    n_time_serie, dims = data.shape
    
    data_ = data - np.mean(data, axis=0)  #zero-mean
    
    x_ = []
    p_ = []

    for i in range(dims):

        probability, bin_edges = np.histogram(data_[:, i], bins=bins, density=True)
        bin_centers = np.array([(bin_edges[i] + bin_edges[i+1]) / 2 for i in range(len(bin_edges)-1)])

        x_.append(bin_centers)
        p_.append(probability)

    x_ = np.array(x_)
    p_ = np.array(p_).reshape(-1)

    df = pd.DataFrame(x_.T)
    df = df.melt(var_name='var', value_name='x')
    df['var'] = 'x' + df['var'].astype(str)

    df['p'] = p_

    for o in order:

        df[o] = (df['x'] ** o) * df['p']

    df = df.melt(id_vars=['var', 'x', 'p'], var_name='order', value_name='moment value')

    ################################################################################

    plot = sns.relplot(data=df, 
                       x='x', 
                       y='moment value', 
                       row=row, 
                       col=column, 
                       hue='p', 
                       palette=palette, 
                       facet_kws={'sharey': False}
                      );

    return plot