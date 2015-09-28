from gzip import open as gzip_open;
from pickle import load as pickle_load;

import matplotlib.pyplot as plt;
import numpy as np;

from sklearn.decomposition import PCA, KernelPCA;


from matplotlib.ticker import NullFormatter


BINARY_FEATs \
  = [ 9, 11, 14, 15, 22, 23, 25, 37, 39, 41, 44, 45, 46, 48, 49, 51, 55, 58,
      60, 64, 69, 70, 72, 73, 78, 83, 87, 89, 95, 99 ];

# based on step07_all_data.pickle plus manual fiddling
DIMCLUSTERs \
  = [ [ -26, 20, 14, -54 ]                                   # 0     # 0
      + [ -27, -5, -7 ],                                     # -9

      [ 32, 2, -34, -36, -12, 13, 15, 51, 53, 24, 31 ]       # 1     # 1
      + [ 65, 66, 37, -38, -52, 25, -58, -61 ]               # 7      
      + [ 33, 39, -8, 9, 42, 44, 48, 19, -21, -55 ]          # -3
      + [ -50, -43, -28, -68 ]                               # -8
      + [ -56, 3, 47 ]                                       # 5
      + [ -35, 4, -67 ],                                     # 6

      [ -64, -57, 60, 6, -63 ]                               # 2     # 2
      + [ 0, 1, 30 ],                                        # 4
    ];



def step15( datadir ):

  data_ = [];
  classlabels = [];

  with open( datadir+'/step07_data.pickle', 'rb' ) as f:
    data__ = pickle_load( f );

  posdims = [];
  negdims = [];
  for dimcluster in DIMCLUSTERs:
    for dim in dimcluster:
      if dim < 0:
        negdims.append( abs(dim) );
      else:
        posdims.append( abs(dim) );

  rowcount = 0;
  poscnt = 0;
  negcnt = 0;

  for ( y, x ) in data__:
    
    rowcount += 1;
    if rowcount > 10000:
      break;

    row = [];
    for (dim,xval) in enumerate(x[1:]):
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
  return;

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

  ( fig, ax ) = plt.subplots( nrows = 3, ncols = 3, figsize = ( 6*3, 6*3 ) );

  for i in range( 0, 3 ):
    for j in range( 0, 3 ):
      if j >= i:
        continue;

      ax[i,j].plot( plottable_neg[i], plottable_neg[j], marker='o', color='b', linestyle='', alpha=0.66 );
      ax[i,j].plot( plottable_pos[i], plottable_pos[j], marker='o', color='r', linestyle='', alpha=0.66 );
      ax[i,j].set_title( str((i,j)) );

  fig.savefig( datadir+'/step20_look_at_this_in_a_plot.png' );



def main( datadir ):

  step15( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
