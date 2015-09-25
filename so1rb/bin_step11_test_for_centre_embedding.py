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


BINARY_FEATs \
  = [ 9, 11, 14, 15, 22, 23, 25, 37, 39, 41, 44, 45, 46, 48, 49, 51, 55, 58,
      60, 64, 69, 70, 72, 73, 78, 83, 87, 89, 95, 99 ];


def discretize( value, septiles ):

  assert septiles[ 0 ] <= value;

  r = None;

  if septiles[ 0 ] <= value < septiles[ 1 ]:
    r = 0;
  elif septiles[ 1 ] <= value < septiles[ 2 ]:
    r = 1;
  elif septiles[ 2 ] <= value < septiles[ 3 ]:
    r = 2;
  elif septiles[ 3 ] <= value < septiles[ 4 ]:
    r = 3;
  elif septiles[ 4 ] <= value < septiles[ 5 ]:
    r = 4;
  elif septiles[ 5 ] <= value < septiles[ 6 ]:
    r = 5;
  elif septiles[ 6 ] <= value <= septiles[ 7 ]:
    r = 6;

  assert value <= septiles[ 7 ];

  return r;


def step11( datadir ):

  with open( datadir+'/step07_binplane_data.pickle', 'rb' ) as f:
    data = pickle_load( f );

  print( len(data) );

  values_by_dim = {};
  values_by_dim_pos = {};
  values_by_dim_neg = {};

  i = 0;

  for ( y, x ) in data:

    i += 1;
    if i >= 10000:
      break;

    for ( i, x_val ) in enumerate( x ):

      if i == 0:
        continue;

      values_by_dim[ i ] = values_by_dim.get( i, [] ) + [ x_val ];
      if y == '0':
        values_by_dim_neg[ i ] = values_by_dim_neg.get( i, [] ) + [ x_val ];
      elif y == '1':
        values_by_dim_pos[ i ] = values_by_dim_pos.get( i, [] ) + [ x_val ];
      else:
        assert False;

  septiles_by_dim = {};
  septiles_by_dim_pos = {};
  septiles_by_dim_neg = {};

  for i in values_by_dim:

    values_by_dim[ i ].sort();
    values_by_dim_pos[ i ].sort();
    values_by_dim_neg[ i ].sort();

    N = float( len( values_by_dim[ i ] ) );
    Np = float( len( values_by_dim_pos[ i ] ) );
    Nn = float( len( values_by_dim_neg[ i ] ) );

    septiles_by_dim[ i ] \
      = ( values_by_dim[ i ][ int( (0.0*N)/7.0 ) ],
          values_by_dim[ i ][ int( (1.0*N)/7.0 ) ],
          values_by_dim[ i ][ int( (2.0*N)/7.0 ) ],
          values_by_dim[ i ][ int( (3.0*N)/7.0 ) ],
          values_by_dim[ i ][ int( (4.0*N)/7.0 ) -1 ],
          values_by_dim[ i ][ int( (5.0*N)/7.0 ) -1 ],
          values_by_dim[ i ][ int( (6.0*N)/7.0 ) -1 ],
          values_by_dim[ i ][ int( (7.0*N)/7.0 ) -1 ] );

    septiles_by_dim_pos[ i ] \
      = ( values_by_dim_pos[ i ][ int( (0.0*Np)/7.0 ) ],
          values_by_dim_pos[ i ][ int( (1.0*Np)/7.0 ) ],
          values_by_dim_pos[ i ][ int( (2.0*Np)/7.0 ) ],
          values_by_dim_pos[ i ][ int( (3.0*Np)/7.0 ) ],
          values_by_dim_pos[ i ][ int( (4.0*Np)/7.0 ) -1 ],
          values_by_dim_pos[ i ][ int( (5.0*Np)/7.0 ) -1 ],
          values_by_dim_pos[ i ][ int( (6.0*Np)/7.0 ) -1 ],
          values_by_dim_pos[ i ][ int( (7.0*Np)/7.0 ) -1 ] );

    septiles_by_dim_neg[ i ] \
      = ( values_by_dim_neg[ i ][ int( (0.0*Nn)/7.0 ) ],
          values_by_dim_neg[ i ][ int( (1.0*Nn)/7.0 ) ],
          values_by_dim_neg[ i ][ int( (2.0*Nn)/7.0 ) ],
          values_by_dim_neg[ i ][ int( (3.0*Nn)/7.0 ) ],
          values_by_dim_neg[ i ][ int( (4.0*Nn)/7.0 ) -1 ],
          values_by_dim_neg[ i ][ int( (5.0*Nn)/7.0 ) -1 ],
          values_by_dim_neg[ i ][ int( (6.0*Nn)/7.0 ) -1 ],
          values_by_dim_neg[ i ][ int( (7.0*Nn)/7.0 ) -1 ] );

  pos = set();
  neg = set();

  for ( y, x ) in data:

    signature = 0;

    for ( i, x_val ) in enumerate( x ):

      if i == 0:
        continue;

      septiles = septiles_by_dim[i];

      is_central = 0;
      if septiles[ 3 ] <= x_val <= septiles[ 4 ]:
        is_central = 1;

      signature |= is_central << i;

    if y == '1':
      pos.add( signature );
    elif y == '0':
      neg.add( signature );
    else:
      assert False;

  with open( datadir+"/step11_test_for_centre_embedding.txt", "wt" ) as out:

    three_d_projections = None;

    for i in range( 1, 4 ):

      print( "-->", i );
      print( "-->", i, file=out );

      count_dim = [];

      for mask in combinations( range(0,70), i ):
        mask_ = reduce( or_, [ 1<<j for j in mask ] );
        pos_cnt = 0;
        neg_cnt = 0;
        for x in pos:
          if ( x & mask_ ) == mask_:
            pos_cnt += 1;
        for x in neg:
          if ( x & mask_ ) == mask_:
            neg_cnt += 1;
        if ( ( pos_cnt + neg_cnt ) < 10 ):
          continue;
        count_dim.append( ( float(pos_cnt) / float(pos_cnt+neg_cnt), pos_cnt, neg_cnt, mask_ ) );

      print( list( sorted( count_dim, reverse=True )[ :7 ] ) );
      print( list( sorted( count_dim, reverse=True )[ :7 ] ), file=out );

      if i == 3:
        three_d_projections = count_dim;

    for ( p, pos, neg, mask ) in sorted( three_d_projections, reverse=True ):
      if ( p < ( 396.0 / 2436.0 ) ):
        break;
      if ( pos <= 2 ):
        continue;
      dims = None;
      for i in range( 0, 70 ):
        if ( mask & (1<<i) ) == (1<<i):
          if dims is None:
            dims = (i,);
          else:
            dims = dims + (i,);
      print( "{:s}, # {:d}, {:d}, ({:1.4f})".format( repr(dims), pos, neg, p ) );
      print( "{:s}, # {:d}, {:d}, ({:1.4f})".format( repr(dims), pos, neg, p ), file=out );



def main( datadir ):

  step11( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
