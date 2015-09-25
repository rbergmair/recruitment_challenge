from gzip import open as gzip_open;

import matplotlib.pyplot as plt;
import numpy as np;


BINARY_FEATs \
  = [ 9, 11, 14, 15, 22, 23, 25, 37, 39, 41, 44, 45, 46, 48, 49, 51, 55, 58,
      60, 64, 69, 70, 72, 73, 78, 83, 87, 89, 95, 99 ];

def step05( datadir ):

  stats_by_b = {};
  stats_by_cid_b = {};

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

      (total,pos) = stats_by_b.get( b_, (0,0) );
      total += 1;
      if y == '1':
        pos += 1;        
      stats_by_b[ b_ ] = ( total, pos );

      (total,pos) = stats_by_cid_b.get( (cid,b_), (0,0) );
      total += 1;
      if y == '1':
        pos += 1;        
      stats_by_cid_b[ (cid,b_) ] = ( total, pos );


  with open( datadir+"/step05_do_some_more_stats.txt", "wt" ) as out:

    for b in sorted( stats_by_b ):

      ( total, pos ) = stats_by_b[ b ];
      p = float(pos) / float(total);

      print( "{:20s};{:7d};{:7d};{:1.4f}".format( hex(b), pos, total, p ) );
      print( "{:20s};{:7d};{:7d};{:1.4f}".format( hex(b), pos, total, p ), file=out );

    print( "-->", len(stats_by_b) );

    for (cid,b) in sorted( stats_by_cid_b ):

      ( total, pos ) = stats_by_cid_b[ (cid,b) ];
      p = float(pos) / float(total);

      print( "{:20s};{:7d};{:7d};{:1.4f}".format( hex(cid)+'.'+hex(b), pos, total, p ) );
      print( "{:20s};{:7d};{:7d};{:1.4f}".format( hex(cid)+'.'+hex(b), pos, total, p ), file=out );

    print( "-->", len(stats_by_cid_b) );



def main( datadir ):

  step05( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
