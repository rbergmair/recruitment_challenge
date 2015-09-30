from pickle import load as pickle_load;
from pickle import dump as pickle_dump;

import numpy as np;
import matplotlib.pyplot as plt;



def step10( datadir ):

  weight_by_dim = [ None ] * 71;

  with open( datadir+'/step08_median_shift_by_dim.txt', 'rt' ) as f:

    for line in f:

      if line and line[:-1] == '\n':
        line = line[:-1];

      ( dim, weight ) = line.split( ';' );
      dim = int(dim);
      weight = float(weight);
      weight_by_dim[ dim ] = weight;
  
  # print( weight_by_dim );

  with open( datadir+'/step07_data.pickle', 'rb' ) as f:
    data = pickle_load( f );

  vals_x_pos = [];
  vals_y_pos = [];
  vals_x_neg = [];
  vals_y_neg = [];

  for (y,x) in data:

    x_ = 0.0;
    y_ = 0.0;

    for (i,valx) in enumerate(x):
      if i == 0:
        continue;
      if weight_by_dim[i] >= 0.0:
        x_ += valx * weight_by_dim[i];
      else:
        y_ += valx * weight_by_dim[i];

    if y == '0':
      vals_x_neg.append( x_ );
      vals_y_neg.append( y_ );
    elif y == '1':
      vals_x_pos.append( x_ );
      vals_y_pos.append( y_ );

  ( fig, ax ) = plt.subplots( nrows=1, ncols=1, figsize=(6,6) );
  ax.plot( vals_x_neg, vals_y_neg, marker='o', color='b', linestyle='', alpha=0.66 );
  ax.plot( vals_x_pos, vals_y_pos, marker='o', color='r', linestyle='', alpha=0.66 );
  
  fig.savefig( datadir+'/step10_try_some_sums.pdf' );



def main( datadir ):

  step10( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
