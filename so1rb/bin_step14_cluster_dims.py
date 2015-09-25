from gzip import open as gzip_open;
from os.path import isfile;

from itertools import combinations;
from functools import reduce;
from operator import or_;

from pickle import load as pickle_load;
from pickle import dump as pickle_dump;

from pprint import pprint;

import matplotlib.pyplot as plt;
import numpy as np;

from sklearn.cluster import AgglomerativeClustering;



def step14( datadir ):

  with open( datadir+'/step07_data.pickle', 'rb' ) as f:
    data = pickle_load( f );

  print( len(data) );

  data_ = [];
  for ( y, x ) in data:
    data_.append( x[1:] );

  data_ = np.array( data_ ).T;

  cov = np.cov( data_ );

  cov_pair = [];

  (n1,n2) = cov.shape;
  for i in range(0,n1):
    for j in range(0,n1):
      if i >= j:
        continue;
      cov_pair.append( ( abs(cov[i,j]), (i,j), cov[i,j] ) );

  for ( abscov, ij, cov_ ) in sorted( cov_pair, reverse=True ):
    print( ij, cov_ );

  print( cov );
  print( abs(cov) );

  c = AgglomerativeClustering( 20, affinity='precomputed', linkage='complete' );
  clusters = c.fit_predict( -abs(cov) );

  clusters_ = {};
  for dim in range(0,n1):
    c = clusters[dim];
    if not c in clusters_:
      clusters_[ c ] = set();
    clusters_[ c ].add( dim );

  clusters__ = [];

  for ( c, dims ) in clusters_.items():

    min_ = None;
    max_ = None;
    sum_ = 0.0;
    n_ = 0.0;

    for dim1 in dims:
      for dim2 in dims:

        if dim1 == dim2:
          continue;

        assert cov[dim1,dim2] == cov[dim2,dim1];
        cov_ = abs(cov[dim1,dim2]);

        if min_ is None:
          min_ = cov_;
        else:
          min_ = min( min_, cov_ );

        if max_ is None:
          max_ = cov_;
        else:
          max_ = max( max_, cov_ );

        sum_ = sum_ + cov_;
        n_ += 1;

    if n_ <= 2.0:
      continue;

    print( c, min_, sum_/n_, max_, len(dims), dims );

    newcluster = []
    mindim = min(dims);
    for dim in dims:
      if cov[ dim, mindim ] >= 0.0:
        newcluster.append( dim );
      else:
        newcluster.append( -dim );
    clusters__.append( newcluster );

  pprint( clusters__ );














def main( datadir ):

  step14( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
