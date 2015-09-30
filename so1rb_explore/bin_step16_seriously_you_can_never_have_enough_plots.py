from gzip import open as gzip_open;
from pickle import load as pickle_load;

import matplotlib.pyplot as plt;
import numpy as np;

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

  for i in range( 0, n ):
    for j in range( 0, n ):
      if j >= i:
        continue;

      nullfmt   = NullFormatter()         # no labels

      # definitions for the axes
      left, width = 0.1, 0.65
      bottom, height = 0.1, 0.65
      bottom_h = left_h = left+width+0.02

      rect_scatter = [left, bottom, width, height]
      rect_histx = [left, bottom_h, width, 0.2]
      rect_histy = [left_h, bottom, 0.2, height]

      # start with a rectangular Figure
      fig = plt.figure(1, figsize=(8,8))

      axScatter = plt.axes(rect_scatter)
      axHistx = plt.axes(rect_histx)
      axHisty = plt.axes(rect_histy)

      # no labels
      axHistx.xaxis.set_major_formatter(nullfmt)
      axHisty.yaxis.set_major_formatter(nullfmt)

      # the scatter plot:
      axScatter.plot( data_neg[i], data_neg[j], marker='o', color='b', linestyle='', alpha=0.66 )
      axScatter.plot( data_pos[i], data_pos[j], marker='o', color='r', linestyle='', alpha=0.66 )

      # now determine nice limits by hand:
      binwidth = 0.25
      xymax = np.max( [np.max(np.fabs( data_neg[i] )), np.max(np.fabs( data_neg[j] ))] )
      lim = ( int(xymax/binwidth) + 1) * binwidth

      axScatter.set_xlim( (-lim, lim) )
      axScatter.set_ylim( (-lim, lim) )

      bins = np.arange(-lim, lim + binwidth, binwidth)
      axHistx.hist( data_neg[i], bins=bins, color='b')
      axHistx.hist( data_pos[i], bins=bins, color='r')

      axHisty.hist( data_neg[j], bins=bins, color='b', orientation='horizontal')
      axHisty.hist( data_pos[j], bins=bins, color='r', orientation='horizontal')

      axHistx.set_xlim( axScatter.get_xlim() )
      axHisty.set_ylim( axScatter.get_ylim() )      

      fig.savefig( datadir+'/step16_seriously_you_can_never_have_enough_plots_{}_{}.png'.format( i, j ) );



def main( datadir ):

  step15( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
