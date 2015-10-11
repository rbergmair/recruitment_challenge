from gzip import open as gzip_open;

from pickle import load as pickle_load;

import matplotlib.pyplot as plt;
import numpy as np;


INTERESTING_COMBINATIONs \
  = [ (10,63) ];




def step09( datadir ):

  with open( datadir+'/step07_data.pickle', 'rb' ) as f:
    data = pickle_load( f );

  neg_x1 = {};
  neg_x2 = {};
  pos_x1 = {};
  pos_x2 = {};

  for (y,x) in data:

    for (dim1,dim2) in INTERESTING_COMBINATIONs:

      dimpair = "{}_{}".format( dim1, dim2 );

      x1 = x[ dim1 ];
      x2 = x[ dim2 ];
      if y == '0':
        neg_x1[ dimpair ] = neg_x1.get( dimpair, [] ) + [ x1 ];
        neg_x2[ dimpair ] = neg_x2.get( dimpair, [] ) + [ x2 ];
      elif y == '1':
        pos_x1[ dimpair ] = pos_x1.get( dimpair, [] ) + [ x1 ];
        pos_x2[ dimpair ] = pos_x2.get( dimpair, [] ) + [ x2 ];
      else:
        assert False;

  clusters1 = set();
  clusters2 = set();
  clusters3 = set();

  for (dim1,dim2) in INTERESTING_COMBINATIONs:

    dimpair = "{}_{}".format( dim1, dim2 );    

    ( fig, ax ) = plt.subplots( nrows=1, ncols=1, figsize=(6,6) );

    ax.plot( neg_x1[ dimpair ], neg_x2[ dimpair ], marker='o', color='b', linestyle='', alpha=0.66 );
    ax.plot( pos_x1[ dimpair ], pos_x2[ dimpair ], marker='o', color='r', linestyle='', alpha=0.66 );

    fig.savefig( datadir+'/step09.png' );





def main( datadir ):

  step09( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
