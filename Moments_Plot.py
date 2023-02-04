#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


############################################################################################
#                                 >>>>> calculations <<<<<                                 #
############################################################################################

def __calculate_moments__(data, order, bins, n_time_series, dims):
    """this function creates a dataframe from binning data and calculating the integrand of 
    the statistical moments of the given orders, and its columns include center of bins (x), 
    the bins widths (delta x), the probability of each bin (p), the error of the probabilities (delta p),
    and the moment values as well as their orders in the column 'order'"""
    
    data_ = (data - np.mean(data, axis=0)) / np.std(data, axis=0) #standardize data (z-score)
    
    x_ = []
    delta_x_ = []

    p_ = []
    delta_p_ = []

    for i in range(dims):

        n_bins, bin_edges = np.histogram(data_[:, i], bins=bins_)
        
        bin_centers = np.array([(bin_edges[i] + bin_edges[i+1]) / 2 for i in range(len(bin_edges)-1)])
        x_.append(bin_centers)
        
        probability = n_bins / n_time_series
        p_.append(probability)

        delta_x = np.diff(bin_edges)
        delta_x_.append(delta_x)

        delta_p = np.sqrt(probability * (1 - probability) / n_time_series)
        delta_p_.append(delta_p)

    x_ = np.array(x_)
    delta_x_ = np.array(delta_x_).reshape(-1)
    p_ = np.array(p_).reshape(-1)
    delta_p_ = np.array(delta_p_).reshape(-1)

    df = pd.DataFrame(x_.T)
    df = df.melt(var_name='var', value_name='x')
    df['var'] = 'x' + df['var'].astype(str)

    df['p'] = p_
    df['delta x'] = np.abs(delta_x_)
    df['delta p'] = np.abs(delta_p_)

    for o in order:

        df[o] = (df['x'] ** o) * df['p']

    df = df.melt(id_vars=df.columns[:-len(order)], var_name='order', value_name='moment value')
    
    df['error'] = np.abs(df['moment value'] * (np.abs(df['delta p'] / df['p']) + \
                                        np.abs(df['order'] * df['delta x'] / df['x'])))
    
    df['error'].fillna(method='ffill', inplace=True)
    
    return df
    
############################################################################################
#                                     >>>>> plot <<<<<                                     #
############################################################################################

@mpl.rc_context({'axes.labelsize': 15, })
def __plot_moments__(df, dims, order, row, column, palette):
    """this function takes the dataframe calculated from the function __calculate_moments__ 
    and plots the moments"""
    
    g = sns.relplot(data=df, 
                       x='x', 
                       y='moment value', 
                       row=row, 
                       col=column, 
                       hue='p', 
                       palette=palette, 
                       facet_kws={'sharey': False}, 
                      );

    ####################################### errorbars ######################################
    
    n_grid = {'var': dims, 'order':len(order)}
    grid_index = {'var': df['var'].unique(), 'order': df['order'].unique()}

    for r in range(n_grid[row]):

        for c in range(n_grid[column]):
            
            ax = g.facet_axis(r, c)
            
            filter_ = (df[row] == grid_index[row][r]) & (df[column] == grid_index[column][c])

            ax.errorbar(df['x'][filter_].values, 
                        df['moment value'][filter_].values, 
                        yerr=df['error'][filter_].values, 
                        ecolor='gray', 
                        elinewidth=1,
                        fmt='none', 
                        zorder=0)
            
    return g

############################################################################################
#                                 >>>>> main function <<<<<                                #
############################################################################################

def moments_plot(data, order, bins=300, row='var', column='order', palette='flare', **kwargs):
    """This function plots the statistical moments of the given orders for a given data.

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
    :return: seaborn facetgrid
    """
    
    ###################################### assertions ######################################

    assert ((row in ['var', 'order'] and column in ['var', 'order']) and row!=column),\
    f"row and column must be different and be one of the ['var', 'order'] but got {row} and {column}."
    assert len(data.shape) == 2, ValueError('time series must have (n_time_serie, dims) shape')
    assert data.shape[0] > 0, ValueError('no data in time series')
    assert (np.array(order) >= 0).all(), ValueError('nagative order is given')
    
    
    ###################################### preliminary #####################################
    
    if type(order) == int:
        order = [order]

    n_time_series, dims = data.shape
    
    
    ###################################### calculations ####################################
    
    df = __calculate_moments__(data, order, bins, n_time_series, dims)
    
    
    ########################################## plot ########################################

    g = __plot_moments__(df, dims, order, row, column, palette)


    return g