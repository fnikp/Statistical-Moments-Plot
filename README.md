# Statistical Moments Plotter

This repository contains a python function `moments_plot` that plots the statistical moments of a given data for specified orders.

## Statistical Moments

Statistical moment is a value computed from the data set that describes its distributional properties, such as central tendency, spread or skewness. For a set of data points $\{x_1, x_2, ..., x_n\}$, the $n^{th}$ statistical moment is defined as:

$$E[(x - \bar{x})^n] = \frac{\Sigma (x_i - \bar{x})^n}{n}$$

There are four commonly used statistical moments:

1. ***Mean (1st order moment)***: The mean of a dataset is the sum of all the data points divided by the total number of data points. It represents the central tendency of a dataset and is also known as the average.

2. ***Variance (2nd order central moment)***: The variance of a dataset is the average of the squared differences from the mean. It measures the spread of the dataset and is used to quantify the dispersion of the data around the mean.

3. ***Skewness (3rd order standardized moment)***: Skewness is a measure of the asymmetry of a dataset about its mean. A positive skewness indicates that there are more data points on the right side of the mean, while a negative skewness indicates more data points on the left side of the mean.

4. ***Kurtosis (4th order standardized moment)***: Kurtosis is a measure of the "peakedness" of a dataset. A high kurtosis indicates that the dataset has a sharp peak and heavy tails, while a low kurtosis indicates a flatter distribution.

## Requirements

* numpy 1.20.3
* pandas 1.3.4
* matplotlib 3.6.2
* seaborn 0.11.2

## Documentation

***moments_plot(data, order, bins=300, row='var', column='order', palette='flare', )***

*This function plots the statistical moments of the given orders for a given data.*

### Parameters

**data**: the array of time-series, each column corresponds to a time-serie
> **type**: nd-array of shape (n, dims) in which n is the number of time points and dims is the dimension of data (number of time-series)

**order**: the order(s) of statistical moments to be plotted.
> **type**: an integer or an array-like

 **bins**: If bins is an int, it defines the number of equal-width bins in the given range (10, by default). If bins is a sequence, it defines the bin edges, including the rightmost edge, allowing for non-uniform bin widths. If bins is a string from the list {‘auto’, ‘fd’, ‘doane’, ‘scott’, ‘rice’, ‘sturges’, ‘sqrt’}, it selects the method used to calculate the optimal bin width; (optional, default: 300)
 > **type**: int or array-like or str

**row**: the name of column which is used for row of facetgrid, can only be 'var' or 'order'; if row='var', each line of facetgrid belongs to one of the time-series, if row='order', each line of facetgrid belongs to one of the given orders. (optional, default='var')
> **type**: str

 **column**: the name of column which is used for column of facetgrid, can only be 'var' or 'order' and should be different from the value of 'row'; if row='var', each line of facetgrid belongs to one of the time-series, if row='order', each line of facetgrid belongs to one of the given orders. (optional, default='order')
> **type**: str

**palette**: passed to sns.relplot as a palette. (optional, default='flare')
> **type**: a seaborn palette 

---------------

### Return

**return**: `sns.relplot`

## How to use

```python
from Moments_Plot import moments_plot

moments_plot(<data>, <order>, bins=300, row='var', column='order', palette='flare')
```

### Example

```python
from Moments_Plot import moments_plot

x = np.random.normal(size=(10 ** 6, 2))
moments_plot(x, order=[1, 2, 3, 4], row='var', column='order', bins=300, palette='flare')
```
![example plot](img/example_plot.png)

## Contribution

If you would like to contribute to this repository, feel free to submit a pull request. Any contributions, no matter how small, are greatly appreciated!

## License

The MIT License (MIT)

Copyright (c) [2023] [Fatemeh Nikpanjeh]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.