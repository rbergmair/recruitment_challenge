from pickle import load as pickle_load;
from pickle import dump as pickle_dump;

import numpy as np;
import matplotlib.pyplot as plt;



def step10( datadir ):

  vals_x_pos = {};
  vals_y_pos = {};
  vals_x_neg = {};
  vals_y_neg = {};

  for subsample in [ 'data', 'binplane_data', 'catplane_data', 'all_data' ]:

    vals_x_pos[ subsample ] = [];
    vals_y_pos[ subsample ] = [];
    vals_x_neg[ subsample ] = [];
    vals_y_neg[ subsample ] = [];

    weight_by_dim = [ None ] * 70;

    with open( datadir+'/step08_'+subsample+'_median_shift_by_dim.txt', 'rt' ) as f:

      for line in f:

        if line and line[:-1] == '\n':
          line = line[:-1];

        ( dim, weight ) = line.split( ';' );
        dim = int(dim);
        weight = float(weight);
        weight_by_dim[ dim ] = weight;
    
    # print( weight_by_dim );

    with open( datadir+'/step07_'+subsample+'.pickle', 'rb' ) as f:
      data = pickle_load( f );

    for (y,x) in data:

      x_ = 0.0;
      y_ = 0.0;

      for (i,valx) in enumerate(x):
        if weight_by_dim[i] >= 0.0:
          x_ += valx * weight_by_dim[i];
          # x_ += valx;
        else:
          y_ += valx * weight_by_dim[i];
          # y_ += valx;

      if y == '0':
        vals_x_neg[ subsample ].append( x_ );
        vals_y_neg[ subsample ].append( y_ );
      elif y == '1':
        vals_x_pos[ subsample ].append( x_ );
        vals_y_pos[ subsample ].append( y_ );


  ( fig, ax ) = plt.subplots( nrows=2, ncols=2, figsize=(6,6) );

  ax[0,0].plot( vals_x_neg['data'], vals_y_neg['data'], marker='o', color='b', linestyle='', alpha=0.66 );
  ax[0,0].plot( vals_x_pos['data'], vals_y_pos['data'], marker='o', color='r', linestyle='', alpha=0.66 );

  ax[0,1].plot( vals_x_neg['binplane_data'], vals_y_neg['binplane_data'], marker='o', color='b', linestyle='', alpha=0.66 );
  ax[0,1].plot( vals_x_pos['binplane_data'], vals_y_pos['binplane_data'], marker='o', color='r', linestyle='', alpha=0.66 );

  ax[1,0].plot( vals_x_neg['catplane_data'], vals_y_neg['catplane_data'], marker='o', color='b', linestyle='', alpha=0.66 );
  ax[1,0].plot( vals_x_pos['catplane_data'], vals_y_pos['catplane_data'], marker='o', color='r', linestyle='', alpha=0.66 );

  ax[1,1].plot( vals_x_neg['all_data'], vals_y_neg['all_data'], marker='o', color='b', linestyle='', alpha=0.66 );
  ax[1,1].plot( vals_x_pos['all_data'], vals_y_pos['all_data'], marker='o', color='r', linestyle='', alpha=0.66 );

  fig.savefig( datadir+'/step10.png' );



def main( datadir ):

  step10( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
