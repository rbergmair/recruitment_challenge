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

      x = [];
      b = [];

      for i in range( 3, len(line) ):

        if (i-2) in BINARY_FEATs:
          b.append( line[i] );
          continue;

        try:

          xval = line[i];
          if not '.' in xval:
            xval = xval+'.';
          xval = xval.split( '.' );

          assert \
            ( ( xval[0][0] == '-' ) and ( len(xval[0]) == 2 ) ) \
                  or ( ( xval[0][0] != '-' ) and ( len(xval[0]) == 1 ) );
          assert \
            len( xval[1] ) <= 3;

          while len( xval[1] ) < 3:
            xval[1] = xval[1] + '0';

          assert \
            len( xval[1] ) == 3;

          if xval[0][0] == '-':
            xval = - int( xval[0][1:] ) * 1000 - int( xval[1] );
          else:
            xval = int( xval[0] ) * 1000 + int( xval[1] );          

          assert ( float(xval) / 1000.0 ) == float(line[i]);

          x.append( xval );

        except:

          print( xval, line[i] );
          raise;

      yield ( y, cid, x, b );


def get_ntile_bounds( datadir ):

  if isfile( datadir + '/ntile_bound_by_dim.pickle' ):
    with open( datadir + '/ntile_bound_by_dim.pickle', 'rb' ) as f:
      return pickle_load( f );

  if False:

    dbs = [];
    for i in range( 0, 70 ):
      dbs.append(
          plyvel.DB(
              '{}/BY_X_{}'.format( datadir, str(i).zfill(2) ),
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

  if True:

    dbs = [];
    for i in range( 0, 70 ):
      dbs.append(
          plyvel.DB(
              '{}/BY_X_{}'.format( datadir, str(i).zfill(2) )
            )
        );

    try:

      rowids_for_ntile_bounds = [];
      for i in range( 1, 32 ):
        rowids_for_ntile_bounds.append( int( 849742.0 * float(i)/32.0 ) );

      ntile_bound_by_dim = [];
      for i in range( 0, 70 ):
        ntile_bound_by_dim.append( [] );

      pprint( rowids_for_ntile_bounds );

      for i in range( 0, 70 ):

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

      with open( datadir + '/ntile_bound_by_dim.pickle', "wb" ) as f:
        pickle_dump( ntile_bound_by_dim, f );

    finally:

      for db in dbs:
        db.close();

  return ntile_bound_by_dim;



def step22( datadir ):

  ntile_bound_by_dim = get_ntile_bounds( datadir );









def main( datadir ):

  step22( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
