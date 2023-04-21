from gzip import open as gzip_open;

import matplotlib.pyplot as plt;
import numpy as np;



def step02( datadir ):

  stats_by_cid = {};

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

      assert cid[0] == '"';
      assert cid[-1] == '"';
      cid = cid[1:-1];
      cid = cid.zfill(2);

      (total,pos) = stats_by_cid.get( cid, (0,0) );

      total += 1;
      if y == '1':
        pos += 1;        

      stats_by_cid[ cid ] = ( total, pos );

  with open( datadir+"/step02.txt", "wt" ) as out:

    for cid in sorted( stats_by_cid.keys() ):
      
      ( total, pos ) = stats_by_cid[ cid ];
      p = float(pos) / float(total);

      print( "{:20s} {:7d} {:7d} {:1.4f}".format( cid, pos, total, p ) );
      print( "{:20s} {:7d} {:7d} {:1.4f}".format( cid, pos, total, p ), file=out );



def main( datadir ):

  step02( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
