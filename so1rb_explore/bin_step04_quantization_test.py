from gzip import open as gzip_open;

import matplotlib.pyplot as plt;
import numpy as np;



def step04( datadir ):

  uvalues_by_dim = {};


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

      for dim in range(1,101):

        if not dim in uvalues_by_dim:
          uvalues_by_dim[ dim ] = set();
        if len( uvalues_by_dim[dim] ) < 500:
          uvalues_by_dim[ dim ].add( x[dim] );

  dim_by_uvalues = [];
  binary = [];
  for ( dim, uvalues ) in uvalues_by_dim.items():
    if len( uvalues ) < 5:
      uvalues_ = uvalues;
    else:
      uvalues_ = None;
    if len( uvalues ) == 2:
      binary.append( dim );
    dim_by_uvalues.append( ( len(uvalues), dim, uvalues_ ) );


  with open( datadir+"/step04.txt", "wt" ) as out:

    for ( uvalues, dim, uvalues_ ) in sorted( dim_by_uvalues ):
      print( "{:3d} {:7d} {:s}".format( dim, uvalues, repr(uvalues_) ) );
      print( "{:3d} {:7d} {:s}".format( dim, uvalues, repr(uvalues_) ), file=out );

    print( "-->", repr(binary) );
    print( "-->", repr(binary), file=out );



def main( datadir ):

  step04( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
