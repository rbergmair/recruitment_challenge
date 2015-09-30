from gzip import open as gzip_open;

from os.path import isfile;
from pprint import pprint;

from math import log;

from pickle import dump as pickle_dump;
from pickle import load as pickle_load;

import matplotlib.pyplot as plt;
import numpy as np;


BINARY_FEATs \
  = [ 9, 11, 14, 15, 22, 23, 25, 37, 39, 41, 44, 45, 46, 48, 49, 51, 55, 58,
      60, 64, 69, 70, 72, 73, 78, 83, 87, 89, 95, 99 ];



def get_stats( datadir ):

  if isfile( datadir + '/step24_stats_by_b.pickle' ):
    with open( datadir + '/step24_stats_by_b.pickle', 'rb' ) as f:
      return pickle_load( f );

  stats = {};

  with gzip_open( datadir+"/train_trn.tsv.gz", "rt" ) as f:

    firstline = f.readline();
    if firstline and firstline[-1] == '\n':
      firstline = firstline[:-1];
    firstline = firstline.split( '\t' );

    assert \
         firstline \
      == (   [ '"id"', '"y"', '"cId"' ]
           + [ '"x{}"'.format(i) for i in range(1,101) ] );

    for line in f:

      if line and line[-1] == '\n':
        line = line[:-1];
      line = line.split( '\t' );

      id_ = line[0];
      y = line[1];
      cid = line[2];

      assert cid[0] == '"';
      assert cid[-1] == '"';
      cid = int( cid[1:-1] );

      x = [ None ];
      b = [];

      for i in range( 3, len(line) ):
        if (i-2) in BINARY_FEATs:
          b.append( line[i] );
        else:
          x.append( line[i] );

      b_ = 0;
      for i in range( 0, len(b) ):
        if b[i] == '0':
          b_i = 0;
        elif b[i] == '1':
          b_i = 1;
        else:
          assert False;
        b_ |= b_i << i;

      (total,pos) = stats.get( b_, (0,0) );
      total += 1;
      if y == '1':
        pos += 1;        
      stats[ b_ ] = ( total, pos );

  with open( datadir + '/step24_stats_by_b.pickle', 'wb' ) as f:

    pickle_dump( stats, f );



def corr( stats, dims_a, dims_b ):

  mask_a = 0;  
  for i in dims_a:
    mask_a |= (1<<i);

  mask_b = 0;  
  for i in dims_b:
    mask_b |= (1<<i);

  cnt_by_a = {};
  cnt_by_b = {};
  cnt_by_ab = {};
  total = 0;

  for ( val, (cnt,cnt_) ) in stats.items():

    val_a = val & mask_a;
    val_b = val & mask_b;

    total += cnt;
    cnt_by_a[ val_a ] = cnt_by_a.get( val_a, 0 ) + cnt;
    cnt_by_b[ val_b ] = cnt_by_b.get( val_b, 0 ) + cnt;
    cnt_by_ab[ (val_a,val_b) ] = cnt_by_ab.get( (val_a,val_b), 0 ) + cnt;

  h_a = 0.0;
  h_b = 0.0;
  h_ab = 0.0;

  for ( val_a, cnt ) in cnt_by_a.items():
    p = float(cnt) / float(total);
    if p > 0.0:      
      h_a -= p * log( p, 2.0 );

  for ( val_b, cnt ) in cnt_by_b.items():
    p = float(cnt) / float(total);
    if p > 0.0:      
      h_b -= p * log( p, 2.0 );

  for( (val_a,val_b), cnt ) in cnt_by_ab.items():
    p = float(cnt) / float(total);
    if p > 0.0:      
      h_ab -= p * log( p, 2.0 );

  if h_a == 0.0:
    return 1.0;

  if h_b == 0.0:
    return 1.0;
  
  inf = h_a + h_b - h_ab;
  return inf / min( h_a, h_b );



def split( stats, dims ):

  if len( dims ) <= 2:
    dim1 = dims.pop();
    dim2 = dims.pop();
    return ( { dim1 }, { dim2 }, set() );

  first_dim = None;
  first_dim_c = None;
  
  for i in dims:

    a = { i };
    b = dims - a;
    c = corr( stats, a, b );

    if ( first_dim_c is None ) or ( c < first_dim_c ):
      first_dim_c = c;
      first_dim = i;

  second_dim = None;
  second_dim_c = None;

  for i in dims - { first_dim }:

    a = { first_dim };
    b = { i };
    c = corr( stats, a, b );

    if ( second_dim_c is None ) or ( c < second_dim_c ):
      second_dim_c = c;
      second_dim = i;

  left = { first_dim };
  right = { second_dim };
  rest = dims - { first_dim, second_dim };

  while True:

    removable = set();

    for i in rest:

      cl = corr( stats, left, {i} );
      cr = corr( stats, right, {i} );

      if ( cl == cr ):
        continue;

      if ( cr > cl ) and ( cr >= 0.5 ):
        removable.add( i );
        right.add( i );

      if ( cl > cr ) and ( cl >= 0.5 ):
        removable.add( i );
        left.add( i );

    rest -= removable;
    if not removable:
      break;

  #print( "---> {:s} {:s} {:1.4f}".format( repr(left), repr(right), corr( stats, left, right ) ) );
  return ( left, right, rest );

  for i in left:
    a = { i };
    b = left - a;
    print( "-L-> {:d} {:1.4f}".format( i, corr( stats, a, b ) ) );

  for i in right:
    a = { i };
    b = right - a;
    print( "-R-> {:d} {:1.4f}".format( i, corr( stats, a, b ) ) );



def step24( datadir ):

  stats = get_stats( datadir );

  clusters = [];
  rest = set( range(0,30) );

  while rest:
    if len( rest ) >= 2:
      ( left, right, rest ) = split( stats, rest );
      clusters.append( left );
      clusters.append( right );
    else:
      clusters.append( rest );
      rest = set();

  for ( cluster_id, cluster ) in enumerate( clusters ):
    print( "-->", cluster_id, cluster );
    for i in cluster:
      a = { i };
      b = cluster - a;
      print( "    {:d} {:1.4f}".format( i, corr( stats, a, b ) ) );

  pprint( clusters );




def main( datadir ):

  step24( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
