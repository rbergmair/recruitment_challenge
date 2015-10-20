from gzip import open as gzip_open;

import matplotlib.pyplot as plt;
import numpy as np;



def step03( datadir ):

  c08_neg_x1 = [];
  c08_neg_x2 = [];
  c08_neg_x99 = [];
  c08_neg_x100 = [];
  c08_pos_x1 = [];
  c08_pos_x2 = [];
  c08_pos_x99 = [];
  c08_pos_x100 = [];

  c42_neg_x1 = []
  c42_neg_x2 = []
  c42_neg_x99 = []
  c42_neg_x100 = []
  c42_pos_x1 = []
  c42_pos_x2 = []
  c42_pos_x99 = []
  c42_pos_x100 = []

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
      x = [ None ] + line[3:];

      if cid == '"8"':
        pass;
      elif cid == '"42"':
        pass;
      else:
        continue;

      if ( len(c08_neg_x1) >= 100 ) and ( len(c08_pos_x1) >= 100 ):
        if ( len(c42_neg_x1) >= 100 ) and ( len(c42_pos_x1) >= 100 ):
          break;

      print( id_, y, cid, x[1], x[2] );

      if cid == '"8"':
        if ( len(c08_neg_x1) < 100 ) or ( len(c08_pos_x1) < 100 ):
          if y == '0':
            c08_neg_x1.append( x[1] );
            c08_neg_x2.append( x[2] );
            c08_neg_x99.append( x[99] );
            c08_neg_x100.append( x[100] );
          else:
            assert y == '1';
            c08_pos_x1.append( x[1] );
            c08_pos_x2.append( x[2] );
            c08_pos_x99.append( x[99] );
            c08_pos_x100.append( x[100] );

      else:
        assert cid == '"42"';
        if ( len(c42_neg_x1) < 100 ) or ( len(c42_pos_x1) < 100 ):
          if y == '0':
            c42_neg_x1.append( x[1] );
            c42_neg_x2.append( x[2] );
            c42_neg_x99.append( x[99] );
            c42_neg_x100.append( x[100] );
          else:
            assert y == '1';
            c42_pos_x1.append( x[1] );
            c42_pos_x2.append( x[2] );
            c42_pos_x99.append( x[99] );
            c42_pos_x100.append( x[100] );

  c08_neg_x1 = np.array( c08_neg_x1 );
  c08_neg_x2 = np.array( c08_neg_x2 );
  c08_neg_x99 = np.array( c08_neg_x99 );
  c08_neg_x100 = np.array( c08_neg_x100 );
  c08_pos_x1 = np.array( c08_pos_x1 );
  c08_pos_x2 = np.array( c08_pos_x2 );
  c08_pos_x100 = np.array( c08_pos_x100 );

  c42_neg_x1 = np.array( c42_neg_x1 );
  c42_neg_x2 = np.array( c42_neg_x2 );
  c42_neg_x99 = np.array( c42_neg_x99 );
  c42_neg_x100 = np.array( c42_neg_x100 );
  c42_pos_x1 = np.array( c42_pos_x1 );
  c42_pos_x2 = np.array( c42_pos_x2 );
  c42_pos_x99 = np.array( c42_pos_x99 );
  c42_pos_x100 = np.array( c42_pos_x100 );

  print( len(c08_neg_x1), len(c08_neg_x2), len(c08_neg_x99), len(c08_neg_x100) );
  print( len(c08_pos_x1), len(c08_pos_x2), len(c08_pos_x99), len(c08_pos_x100) );
  print( len(c42_neg_x1), len(c42_neg_x2), len(c42_neg_x99), len(c42_neg_x100) );
  print( len(c42_pos_x1), len(c42_pos_x2), len(c42_pos_x99), len(c42_pos_x100) );

  ( fig, ax ) = plt.subplots( ncols=2, nrows=5, figsize=(6,12) );

  ax[0,0].plot( c08_neg_x1, c08_neg_x2, marker='o', color='b', linestyle='', alpha=0.66 );
  ax[0,0].plot( c08_pos_x1, c08_pos_x2, marker='o', color='r', linestyle='', alpha=0.66 );
  ax[0,1].plot( c42_neg_x1, c42_neg_x2, marker='o', color='b', linestyle='', alpha=0.66 );
  ax[0,1].plot( c42_pos_x1, c42_pos_x2, marker='o', color='r', linestyle='', alpha=0.66 );

  ax[1,0].plot( c08_neg_x1, c08_neg_x99, marker='o', color='b', linestyle='', alpha=0.66 );
  ax[1,0].plot( c08_pos_x1, c08_pos_x99, marker='o', color='r', linestyle='', alpha=0.66 );
  ax[1,1].plot( c42_neg_x1, c42_neg_x99, marker='o', color='b', linestyle='', alpha=0.66 );
  ax[1,1].plot( c42_pos_x1, c42_pos_x99, marker='o', color='r', linestyle='', alpha=0.66 );

  ax[2,0].plot( c08_neg_x1, c08_neg_x100, marker='o', color='b', linestyle='', alpha=0.66 );
  ax[2,0].plot( c08_pos_x1, c08_pos_x100, marker='o', color='r', linestyle='', alpha=0.66 );
  ax[2,1].plot( c42_neg_x1, c42_neg_x100, marker='o', color='b', linestyle='', alpha=0.66 );
  ax[2,1].plot( c42_pos_x1, c42_pos_x100, marker='o', color='r', linestyle='', alpha=0.66 );

  ax[3,0].plot( c08_neg_x2, c08_neg_x100, marker='o', color='b', linestyle='', alpha=0.66 );
  ax[3,0].plot( c08_pos_x2, c08_pos_x100, marker='o', color='r', linestyle='', alpha=0.66 );
  ax[3,1].plot( c42_neg_x2, c42_neg_x100, marker='o', color='b', linestyle='', alpha=0.66 );
  ax[3,1].plot( c42_pos_x2, c42_pos_x100, marker='o', color='r', linestyle='', alpha=0.66 );

  ax[4,0].plot( c08_neg_x99, c08_neg_x100, marker='o', color='b', linestyle='', alpha=0.66 );
  ax[4,0].plot( c08_pos_x99, c08_pos_x100, marker='o', color='r', linestyle='', alpha=0.66 );
  ax[4,1].plot( c42_neg_x99, c42_neg_x100, marker='o', color='b', linestyle='', alpha=0.66 );
  ax[4,1].plot( c42_pos_x99, c42_pos_x100, marker='o', color='r', linestyle='', alpha=0.66 );

  fig.savefig( datadir+'/step03.png' );



def main( datadir ):

  step03( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
