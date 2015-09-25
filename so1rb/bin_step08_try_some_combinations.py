from gzip import open as gzip_open;
from os.path import isfile;

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


def step08( datadir ):

  with open( datadir+'/step07_data.pickle', 'rb' ) as f:
    data = pickle_load( f );

  values_by_dim = {};
  values_by_dim_pos = {};
  values_by_dim_neg = {};

  for ( y, x ) in data:

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

  stats_by_dimpair = {};

  for ( y, x ) in data:

    for dim1 in septiles_by_dim:

      x1 = discretize( x[dim1], septiles_by_dim[dim1] );

      for dim2 in septiles_by_dim:

        if dim1 >= dim2:
          continue;

        x2 = discretize( x[dim2], septiles_by_dim[dim2] );

        if (dim1,dim2) not in stats_by_dimpair:
          stats_by_dimpair[ (dim1,dim2) ] = {};

        ( total, pos ) = stats_by_dimpair[ (dim1,dim2) ].get( (x1,x2), (0,0) );

        total += 1;
        if y == '1':
          pos += 1;

        stats_by_dimpair[ (dim1,dim2) ][ (x1,x2) ] = ( total, pos );

  maxprop_dimpair = [];

  for ( dimpair, stats_by_valuepair ) in stats_by_dimpair.items():
    maxprop = None;
    maxtotal = 0;
    for ( total, pos ) in stats_by_valuepair.values():
      if total < 10:
        continue;
      prop = float(pos) / float(total);
      if maxprop is None:
        maxprop = prop;
      else:
        if prop > maxprop:
          maxprop = prop;
          maxtotal = total;
    maxprop_dimpair.append( (-maxprop,dimpair,maxtotal) );

  with open( datadir+"/step08_median_shift_by_dim.txt", "wt" ) as out:

    median_shift_dim = [];
    for i in values_by_dim:
      median_pos = ( septiles_by_dim_pos[ i ][ 3 ] + septiles_by_dim_pos[ i ][ 4 ] ) / 2.0;
      median_neg = ( septiles_by_dim_neg[ i ][ 3 ] + septiles_by_dim_neg[ i ][ 4 ] ) / 2.0;
      median_shift_dim.append( ( abs(median_pos - median_neg), i, median_pos - median_neg ) );
    for ( abs_median_shift, dim, median_shift ) in sorted( median_shift_dim, reverse=True ):
      print( dim, median_shift, sep=';' );
      print( dim, median_shift, sep=';', file=out );

  with open( datadir+"/step08_interesting_combinations.txt", "wt" ) as out:

    for (maxprop,dimpair,maxtotal) in sorted( maxprop_dimpair ):
      print( dimpair[0], dimpair[1], -maxprop, maxtotal, sep=';' );
      print( dimpair[0], dimpair[1], -maxprop, maxtotal, sep=';', file=out );



def main( datadir ):

  step08( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
