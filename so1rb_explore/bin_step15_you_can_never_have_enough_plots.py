from gzip import open as gzip_open;
from pickle import load as pickle_load;

import matplotlib.pyplot as plt;
import numpy as np;



BINARY_FEATs \
  = [ 9, 11, 14, 15, 22, 23, 25, 37, 39, 41, 44, 45, 46, 48, 49, 51, 55, 58,
      60, 64, 69, 70, 72, 73, 78, 83, 87, 89, 95, 99 ];

# based on step 14
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

# based on manual fiddling

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

  data_pos = [];
  data_neg = [];
  for i in range( 0, len(DIMCLUSTERs) ):
    data_pos.append( [] );
    data_neg.append( [] );
  print( data_pos, data_neg );

  with open( datadir+'/step07_'+subsample+'.pickle', 'rb' ) as f:
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
          xval += -x[ abs(dim)-1 ];
        else:
          xval += x[ abs(dim)-1 ];
        nx += 1.0;        
      if y == '0':
        data_neg[ i ].append( xval/nx );
      elif y == '1':
        data_pos[ i ].append( xval/nx );

  data_pos = np.array( data_pos );
  data_neg = np.array( data_neg );

  print( np.cov( data_neg ) );

  n = len(DIMCLUSTERs);
  ( fig, ax ) = plt.subplots( nrows = n, ncols = n, figsize = ( 3*n, 3*n ) );

  for i in range( 0, n ):
    for j in range( 0, n ):
      if j >= i:
        continue;

      ax[i,j].plot( data_neg[i], data_neg[j], marker='o', color='b', linestyle='', alpha=0.66 );
      ax[i,j].plot( data_pos[i], data_pos[j], marker='o', color='r', linestyle='', alpha=0.66 );
      ax[i,j].set_title( str((i,j)) );

  fig.savefig( datadir+'/step15.png' );



def main( datadir ):

  step15( datadir, 'data' );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
