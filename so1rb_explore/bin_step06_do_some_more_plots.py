from gzip import open as gzip_open;

import matplotlib.pyplot as plt;
import numpy as np;


BINARY_FEATs \
  = [ 9, 11, 14, 15, 22, 23, 25, 37, 39, 41, 44, 45, 46, 48, 49, 51, 55, 58,
      60, 64, 69, 70, 72, 73, 78, 83, 87, 89, 95, 99 ];


INTERESTING_POINTS \
  = [ '0x18.0x1fd57fcf', '0xe.0x3fffffff' ]




def step06( datadir ):

  neg_x1 = {};
  neg_x2 = {};
  neg_x69 = {};
  neg_x70 = {};

  pos_x1 = {};
  pos_x2 = {};
  pos_x69 = {};
  pos_x70 = {};


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

      point = hex(cid)+'.'+hex(b_);

      if point not in INTERESTING_POINTS:
        continue;

      if y == '0':

        neg_x1[ point ] = neg_x1.get( point, [] ) + [ x[1] ];
        neg_x2[ point ] = neg_x2.get( point, [] ) + [ x[2] ];
        neg_x69[ point ] = neg_x69.get( point, [] ) + [ x[69] ];
        neg_x70[ point ] = neg_x70.get( point, [] ) + [ x[70] ];

      else:
        assert y == '1';

        pos_x1[ point ] = pos_x1.get( point, [] ) + [ x[1] ];
        pos_x2[ point ] = pos_x2.get( point, [] ) + [ x[2] ];
        pos_x69[ point ] = pos_x69.get( point, [] ) + [ x[69] ];
        pos_x70[ point ] = pos_x70.get( point, [] ) + [ x[70] ];

  
  ( fig, ax ) = plt.subplots( ncols=2, nrows=5, figsize=(6,12) );

  ax[0,0].plot( neg_x1[ '0xe.0x3fffffff' ], neg_x2[ '0xe.0x3fffffff' ], marker='o', color='b', linestyle='', alpha=0.66 );
  ax[0,0].plot( pos_x1[ '0xe.0x3fffffff' ], pos_x2[ '0xe.0x3fffffff' ], marker='o', color='r', linestyle='', alpha=0.66 );
  ax[0,1].plot( neg_x1[ '0x18.0x1fd57fcf' ], neg_x2[ '0x18.0x1fd57fcf' ], marker='o', color='b', linestyle='', alpha=0.66 );
  ax[0,1].plot( pos_x1[ '0x18.0x1fd57fcf' ], pos_x2[ '0x18.0x1fd57fcf' ], marker='o', color='r', linestyle='', alpha=0.66 );

  ax[1,0].plot( neg_x1[ '0xe.0x3fffffff' ], neg_x69[ '0xe.0x3fffffff' ], marker='o', color='b', linestyle='', alpha=0.66 );
  ax[1,0].plot( pos_x1[ '0xe.0x3fffffff' ], pos_x69[ '0xe.0x3fffffff' ], marker='o', color='r', linestyle='', alpha=0.66 );
  ax[1,1].plot( neg_x1[ '0x18.0x1fd57fcf' ], neg_x69[ '0x18.0x1fd57fcf' ], marker='o', color='b', linestyle='', alpha=0.66 );
  ax[1,1].plot( pos_x1[ '0x18.0x1fd57fcf' ], pos_x69[ '0x18.0x1fd57fcf' ], marker='o', color='r', linestyle='', alpha=0.66 );

  ax[2,0].plot( neg_x1[ '0xe.0x3fffffff' ], neg_x70[ '0xe.0x3fffffff' ], marker='o', color='b', linestyle='', alpha=0.66 );
  ax[2,0].plot( pos_x1[ '0xe.0x3fffffff' ], pos_x70[ '0xe.0x3fffffff' ], marker='o', color='r', linestyle='', alpha=0.66 );
  ax[2,1].plot( neg_x1[ '0x18.0x1fd57fcf' ], neg_x70[ '0x18.0x1fd57fcf' ], marker='o', color='b', linestyle='', alpha=0.66 );
  ax[2,1].plot( pos_x1[ '0x18.0x1fd57fcf' ], pos_x70[ '0x18.0x1fd57fcf' ], marker='o', color='r', linestyle='', alpha=0.66 );

  ax[3,0].plot( neg_x2[ '0xe.0x3fffffff' ], neg_x70[ '0xe.0x3fffffff' ], marker='o', color='b', linestyle='', alpha=0.66 );
  ax[3,0].plot( pos_x2[ '0xe.0x3fffffff' ], pos_x70[ '0xe.0x3fffffff' ], marker='o', color='r', linestyle='', alpha=0.66 );
  ax[3,1].plot( neg_x2[ '0x18.0x1fd57fcf' ], neg_x70[ '0x18.0x1fd57fcf' ], marker='o', color='b', linestyle='', alpha=0.66 );
  ax[3,1].plot( pos_x2[ '0x18.0x1fd57fcf' ], pos_x70[ '0x18.0x1fd57fcf' ], marker='o', color='r', linestyle='', alpha=0.66 );

  ax[4,0].plot( neg_x69[ '0xe.0x3fffffff' ], neg_x70[ '0xe.0x3fffffff' ], marker='o', color='b', linestyle='', alpha=0.66 );
  ax[4,0].plot( pos_x69[ '0xe.0x3fffffff' ], pos_x70[ '0xe.0x3fffffff' ], marker='o', color='r', linestyle='', alpha=0.66 );
  ax[4,1].plot( neg_x69[ '0x18.0x1fd57fcf' ], neg_x70[ '0x18.0x1fd57fcf' ], marker='o', color='b', linestyle='', alpha=0.66 );
  ax[4,1].plot( pos_x69[ '0x18.0x1fd57fcf' ], pos_x70[ '0x18.0x1fd57fcf' ], marker='o', color='r', linestyle='', alpha=0.66 );

  fig.savefig( datadir+'/step06.png'.format( point ) );



def main( datadir ):

  step06( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
