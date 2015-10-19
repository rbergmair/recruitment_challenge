from pickle import load as pickle_load;

import matplotlib.pyplot as plt;
import numpy as np;
from numpy import linalg as LA;

from sklearn.decomposition import PCA, KernelPCA;

from functools import reduce;


from matplotlib.ticker import NullFormatter;



DIMCLUSTERs \
  = [ [ -55, -27, 15, 21 ],                                    # 0
      [ -61, -11, 6, 8, 28 ],                                  # 1
      [ -59, -35, 3, 14, 16, 32, 38 ],                         # 2
      [ -67, -30, -26, 23, 39, 62 ],                           # 3
      [ -57, 4, 48 ],                                          # 4
      [ -64, -51, -44, 17 ],                                   # 5
      [ -54, -52, -33, 13, 29, 37, 69 ],                       # 6
      [ -68, -53, -36, 5, 66 ],                                # 7
      [ -49, -45, -43, -40, -34, -25, -20, -10, 9, 22, 56 ],   # 8
      [ -65, -58, 7 ],                                         # 9
      [ 1, 2, 31 ]                                             # 10
    ];

DIMCLUSTERs \
  = [ [ -55, -27, 15, 21 ],                                    # 0  0

      [ -61, -11, 6, 8, 28 ]                                   # 1  1
      + [ -1, -2, -31 ]                                        # 10
      + [ 57, -4, -48 ]                                        # 4
      + [ 64, 51, 44, -17 ]                                    # 5
      + [ 65, 58, -7 ],                                        # 9

      [ -59, -35, 3, 14, 16, 32, 38 ]                          # 2  2
      + [ 54, 52, 33, -13, -29, -37, -69 ]                     # 6
      + [ -68, -53, -36, 5, 66 ]                               # 7
      + [ 49, 45, 43, 40, 34, 25, 20, 10, -9, -22, -56 ]       # 8
      + [ 67, 30, 26, -23, -39, -62 ],                         # 3
    ];



def step15( datadir, subsample ):

  data_ = [];
  classlabels = [];

  with open( datadir+'/step07_'+subsample+'.pickle', 'rb' ) as f:
    data__ = pickle_load( f );

  posdims = [];
  negdims = [];
  for dimcluster in DIMCLUSTERs:
    for dim in dimcluster:
      if dim < 0:
        negdims.append( abs(dim)-1 );
      else:
        posdims.append( abs(dim)-1 );

  rowcount = 0;
  poscnt = 0;
  negcnt = 0;

  for ( y, x ) in data__:
    
    rowcount += 1;
    if rowcount > 2500:
      break;

    row = [];
    for (dim,xval) in enumerate(x):
      if dim in posdims:
        row.append( xval );
      elif dim in negdims:
        # row.append( -xval );
        row.append( xval );
      else:
        #print( "skipping dim", dim );
        row.append( xval );

    data_.append( row );

    if y == '0':
      classlabels.append( 0 );
      negcnt += 1;
    elif y == '1':
      classlabels.append( 1 );
      poscnt += 1;

  data_ = np.array( data_ );
  classlabels = np.array( classlabels );

  ratio = float( poscnt ) / float( poscnt+negcnt );

  data = KernelPCA( n_components=3, kernel='cosine' ).fit_transform( data_ );  

  print( np.cov(data.T) );

  print( data[0] );

  plottable_pos = [];
  plottable_neg = [];
  for i in range(0,3):
    plottable_pos.append( [] );
    plottable_neg.append( [] );

  for (y,x) in zip( classlabels, data ):
    for (i,xval) in enumerate(x):
      if y == 0:
        plottable_neg[ i ].append( xval );
      elif y == 1:
        plottable_pos[ i ].append( xval );

  ( fig, ax ) = plt.subplots( nrows = 3, ncols = 3, figsize = ( 3*3, 3*3 ) );

  for i in range( 0, 3 ):
    for j in range( 0, 3 ):
      if j >= i:
        continue;

      ax[i,j].plot( plottable_neg[i], plottable_neg[j], marker='o', color='b', linestyle='', alpha=0.66 );
      ax[i,j].plot( plottable_pos[i], plottable_pos[j], marker='o', color='r', linestyle='', alpha=0.66 );
      ax[i,j].set_title( str((i,j)) );

  fig.savefig( datadir+'/step20_'+subsample+'.png' );



def main( datadir ):

  step15( datadir, 'data' );
  step15( datadir, 'all_data' );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
