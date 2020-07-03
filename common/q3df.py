#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This procedure is the core routine to fit the continuum and emission lines of
a spectrum. As input, it requires a structure of initialization parameters.
The tags for this structure can be found in INITTAGS.txt.

Returns
-------
IDL save file (.xdr)

Parameters
----------
initproc: in, required, type=string
    Name of procedure to initialize the fit.
cols: in, optional, type=intarr, default=all
       Columns to fit, in 1-offset format. Either a scalar or a
       two-element vector listing the first and last columns to fit.
     ncores: in, optional, type=int, default=1
       Number of cores to split processing over.
     rows: in, optional, type=intarr, default=all
       Rows to fit, in 1-offset format. Either a scalar or a
       two-element vector listing the first and last rows to fit.
     oned: in, optional, type=byte
       Data is assumed to be in a 2d array  choose this switch to
       input data as a 1d array.
     onefit: in, optional, type=byte
       Option to skip second fit  primarily for testing.
     verbose: in, optional, type=byte
       Print error and progress messages. Propagates to most/all
       subroutines.

History
    2020jun29, canicetti, copied header from q3df.py

Created on Mon June 29 22:50 2020

@author: danicetti
"""

__author__ = 'Q3D Team'
__credits__ = ['Carlos Anicetti']
__created__ = '2020 June 29'
__last_modified__ = '2020 June 29'

# invoke the correct q3df helper function depending on whether this is to a single-
# or multi-threaded process
def q3df( initproc, cols=None, rows=None, oned=False, onefit=False, ncores=1, \
    quiet=True ):
     if ncores == 1:
         from common.q3df_helperFunctions import q3df_oneCore
         q3df_oneCore(initproc, cols, rows, oned, onefit, quiet)
     elif ncores > 1:
        from subprocess import call
        # convert cols and rows to string of form "[1,2,3...]" Note no whitespace.
        cols = str(cols)
        cols = cols.replace(" ", "")
        rows = str(rows)
        rows = rows.replace(" ", "")
        # start a new MPI process since MPI cannot be started from within a Python script
        call(["mpiexec", "-n", str(ncores), "python", "common/q3df_helperFunctions.py",\
                initproc, cols, rows, str(oned), str(onefit), str(quiet)])




