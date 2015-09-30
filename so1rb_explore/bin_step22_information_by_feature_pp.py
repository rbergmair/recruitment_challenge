from os.path import isfile;

from gzip import open as gzip_open;

from pickle import load as pickle_load;
from pickle import dump as pickle_dump;

from struct import pack, unpack;

from time import sleep;

from pprint import pprint;

import plyvel;



BINARY_FEATs \
  = [ 9, 11, 14, 15, 22, 23, 25, 37, 39, 41, 44, 45, 46, 48, 49, 51, 55, 58,
      60, 64, 69, 70, 72, 73, 78, 83, 87, 89, 95, 99 ];

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



def iterate_data( datadir ):

  with gzip_open( datadir+"/train_trn.tsv.gz", "rt" ) as f:

    pass;

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

      x_ = [ None ];
      b = [];

      for i in range( 3, len(line) ):

        if (i-2) in BINARY_FEATs:
          b.append( int(line[i]) );
        else:
          x_.append( float(line[i]) )
          continue;

      x = [];

      for ( i, dims ) in enumerate( DIMCLUSTERs ):
        xval = 0.0;
        nx = 0.0;
        for dim in dims:
          if dim < 0:
            xval += -x_[ 1+abs(dim) ];
          else:
            xval += x_[ 1+abs(dim) ];
          nx += 1.0;        
        x.append( int( ( xval/nx ) * 10000.0 ) );

      yield ( y, cid, x, b );


def get_ntile_bounds( datadir ):

  if isfile( datadir + '/step22_ntile_bound_by_dim.pickle' ):
    with open( datadir + '/step22_ntile_bound_by_dim.pickle', 'rb' ) as f:
      return pickle_load( f );

  if False:

    dbs = [];
    for i in range( 0, 3 ):
      dbs.append(
          plyvel.DB(
              '{}/step22_by_x_{}'.format( datadir, str(i).zfill(2) ),
              create_if_missing=True
            )
        );

    try:

      rowcount = 0;
      for ( y, cid, x, b ) in iterate_data( datadir ):
        rowcount += 1;
        for ( i, xval ) in enumerate( x ):
          xval = pack( ">I", (1<<31) + xval );
          xcnt = unpack( ">I", dbs[ i ].get( xval, default=pack( ">I", 0 ) ) )[ 0 ];
          xcnt += 1;
          dbs[ i ].put( xval, pack( ">I", xcnt ) );

      print( rowcount );

    finally:

      sleep( 3.0 );
      for db in dbs:
        db.close();

    return None;

  if True:

    dbs = [];
    for i in range( 0, 3 ):
      dbs.append(
          plyvel.DB(
              '{}/step22_by_x_{}'.format( datadir, str(i).zfill(2) )
            )
        );

    try:

      rowids_for_ntile_bounds = [];
      for i in range( 1, 8 ):
        rowids_for_ntile_bounds.append( int( 849742.0 * float(i)/8.0 ) );

      ntile_bound_by_dim = [];
      for i in range( 0, 3 ):
        ntile_bound_by_dim.append( [] );

      pprint( rowids_for_ntile_bounds );

      for i in range( 0, 3 ):

        print( '->', i );

        with dbs[ i ].iterator() as it:

          rowid = 0;

          for ( valid, ( xval, xcnt ) ) in enumerate( it ):

            xval = unpack( '>I', xval )[ 0 ] - (1<<31);
            xcnt = unpack( '>I', xcnt )[ 0 ];

            rowid_old = rowid;
            rowid = rowid_old + xcnt;

            for bound in rowids_for_ntile_bounds:
              if rowid_old < bound <= rowid:
                ntile_bound_by_dim[ i ].append( xval );

      pprint( ntile_bound_by_dim );

      with open( datadir + '/step22_ntile_bound_by_dim.pickle', "wb" ) as f:
        pickle_dump( ntile_bound_by_dim, f );

    finally:

      for db in dbs:
        db.close();

  return ntile_bound_by_dim;



def convert_to_ntile( val, boundaries ):

  boundaries = [ None ] + boundaries + [ None ];

  for i in range( 0, len(boundaries)-1 ):

    lower = boundaries[ i ];
    upper = boundaries[ i+1 ];

    assert not ( lower is None and upper is None );

    if lower is None:
      assert upper is not None;
      if val <= upper:
        return i;

    if upper is None:
      assert lower is not None;
      if lower < val:
        return i;

    if ( lower is not None ) and ( upper is not None ):
      if lower < val <= upper:
        return i;



def step22( datadir ):

  ntile_bound_by_dim = get_ntile_bounds( datadir );

  with open( datadir + '/step22_data.pickle', 'wb' ) as f:

    data = [];

    for ( y, cid, x_, b ) in iterate_data( datadir ):

      x = [];
      for ( i, xval ) in enumerate( x_ ):        
        x.append( convert_to_ntile( xval, ntile_bound_by_dim[ i ] ) );

      # print( y, cid, x, b );

      pickle_dump( ( y, cid, x, b ), f );



def main( datadir ):

  step22( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
