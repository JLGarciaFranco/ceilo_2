# -*- coding: utf-8 -*-
"""
Plotting example 1
========================

The gallery is capable of transforming Python files into reStructuredText files
with a notebook structure. For this to be used you need to respect some syntax
rules.

It makes a lot of sense to contrast this output rst file with the
:download:`original Python script <plot_notebook.py>` to get better feeling of
the necessary file structure.

Anything before the Python script docstring is ignored by sphinx-gallery and
will not appear in the rst file, nor will it be executed.
This Python docstring requires an reStructuredText title to name the file and
correctly build the reference links.

Once you close the docstring you would be writing Python code. This code gets
executed by sphinx gallery shows the plots and attaches the generating code.
Nevertheless you can break your code into blocks and give the rendered file
a notebook style. In this case you have to include a code comment breaker
a line of at least 20 hashes and then every comment start with the a new hash.

As in this example we start by first writing this module
style docstring, then for the first code block we write the example file author
and script license continued by the import modules instructions.
"""

# Code source: Óscar Nájera
# License: BSD 3 clause

import numpy as np
import matplotlib.pyplot as plt
from ceilotools import readmatrixfile, readmlh
matrixfile='/home/jlgf/Documents/Python/scripts/serverversion/ceilo_2/20130101_UNAM_matrix.txt'
mlhfile='/home/jlgf/Documents/Python/scripts/serverversion/ceilo_2/20130101_UNAM_mlh.txt'
filename=mlhfile.split('/')[-1]
##############################################################################
# This code block is executed, although it produces no output. Lines starting
# with a simple hash are code comment and get treated as part of the code
# block. To include this new comment string we started the new block with a
# long line of hashes.
#
# The sphinx-gallery parser will assume everything after this splitter and that
# continues to start with a **comment hash and space** (respecting code style)
# is text that has to be rendered in
# html format. Keep in mind to always keep your comments always together by
# comment hashes. That means to break a paragraph you still need to commend
# that line break.
#
# In this example the next block of code produces some plotable data. Code is
# executed, figure is saved and then code is presented next, followed by the
# inlined figure.

z,time,allprf=readmatrixfile(matrixfile)
mlhtime,mlh=readmlh(mlhfile)
levels=np.arange(0,150,7.5)
for i in range(len(allprf[0,:])):
  for j in range(len(allprf[:,0])):
    if allprf[j,i] > max(levels):
    	allprf[j,i] = max(levels)
    elif allprf[j,i] < min(levels):
        allprf[j,i] = min(levels)
plt.figure(figsize=(12,7))
plt.contourf(time,z,allprf,cmap='gist_ncar',levels=levels)
plt.colorbar()
plt.scatter(mlhtime,mlh,c='k',marker='o',s=5)
plt.xlabel('Time [h]',fontsize=14)
plt.ylabel('Height [m]',fontsize=14)
plt.title("Backscaterring matrix and MLH on "+filename[0:8],fontsize=16)
#plt.savefig('auto_examples/images/20160212.png')
plt.show()
###########################################################################
# Again it is psossble to continue the discussion with a new Python string. This
# time to introduce the next code block generates 2 separate figures.
