from gzip import open as gzip_open;
from pickle import load as pickle_load;

import matplotlib.pyplot as plt;
import numpy as np;



BINARY_FEATs \
  = [ 9, 11, 14, 15, 22, 23, 25, 37, 39, 41, 44, 45, 46, 48, 49, 51, 55, 58,
      60, 64, 69, 70, 72, 73, 78, 83, 87, 89, 95, 99 ];

# based on step07_all_data.pickle
DIMCLUSTERs \
  = [ [ -26, 20, 14, -54 ],                                  # 0
      [ 32, 2, -34, -36, -12, 13, 15, 51, 53, 24, 31 ],      # 1
      [ -64, -57, 60, 6, -63 ],                              # 2
      [ -33, -39, 8, -9, -42, -44, -48, -19, 21, 55 ],       # 3
      [ 0, 1, 30 ],                                          # 4
      [ -56, 3, 47 ],                                        # 5
      [ -35, 4, -67 ],                                       # 6
      [ 65, 66, 37, -38, -52, 25, -58, -61 ],                # 7
      [ 50, 43, 28, 68 ],                                    # 8
      [ 27, 5, 7 ]                                           # 9
    ];

# based on step07_data.pickle
DIMCLUSTERs_ \
  = [ [ 5, 7, -10, 27, -60, -30 ],                           # 0
      [ 0, 1, -57, -64, 6 ],                                 # 1
      [ -33, -39, 8, -9, -42, -44, -48, -19, 21, 55, -24 ],  # 2
      [ -54, -26, 29, 14, -22 ],                             # 3
      [ 16, -50, -43, -63 ],                                 # 4
      [ -56, 3, 47 ],                                        # 5
      [ 31, -34, 13, 15 ],                                   # 6
      [ 65, 2, 66, 37, -38, -52, 25, -58, -61 ],             # 7
      [ -32, 36, 68, 12, -51, -53, 28 ]                      # 8
    ];

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

  data_pos = [];
  data_neg = [];
  for i in range( 0, len(DIMCLUSTERs) ):
    data_pos.append( [] );
    data_neg.append( [] );
  print( data_pos, data_neg );

  with open( datadir+'/step07_data.pickle', 'rb' ) as f:
    data = pickle_load( f );

  rowcount = 0;

  for ( y, x ) in data:
    
    rowcount += 1;
    if rowcount > 10000:
      break;

    for ( i, dims ) in enumerate( DIMCLUSTERs ):
      xval = 0.0;
      nx = 0.0;
      for dim in dims:
        if dim < 0:
          xval += -x[ 1+abs(dim) ];
        else:
          xval += x[ 1+abs(dim) ];
        nx += 1.0;        
      if y == '0':
        data_neg[ i ].append( xval/nx );
      elif y == '1':
        data_pos[ i ].append( xval/nx );

  data_pos = np.array( data_pos );
  data_neg = np.array( data_neg );

  print( np.cov( data_neg ) );

  n = len(DIMCLUSTERs);
  ( fig, ax ) = plt.subplots( nrows = n, ncols = n, figsize = ( 6*n, 6*n ) );

  for i in range( 0, n ):
    for j in range( 0, n ):
      if j >= i:
        continue;

      ax[i,j].plot( data_neg[i], data_neg[j], marker='o', color='b', linestyle='', alpha=0.66 );
      ax[i,j].plot( data_pos[i], data_pos[j], marker='o', color='r', linestyle='', alpha=0.66 );
      ax[i,j].set_title( str((i,j)) );

  fig.savefig( datadir+'/step15_you_can_never_have_enough_plots.png' );



def main( datadir ):

  step15( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
