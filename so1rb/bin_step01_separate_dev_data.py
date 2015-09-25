from os.path import isfile;
from random import random;
from gzip import open as gzip_open;

import numpy as np;
import matplotlib as mpl;



def step01( datadir ):

  assert isfile( datadir+"/train.tsv.gz" );
  assert not isfile( datadir+"/train_trn.tsv.gz" );
  assert not isfile( datadir+"/train_dev.tsv.gz" );

  with gzip_open( datadir+"/train_trn.tsv.gz", "wt" ) as trn:
    with gzip_open( datadir+"/train_dev.tsv.gz", "wt" ) as dev:
      with gzip_open( datadir+"/train.tsv.gz", "rt" ) as f:

        firstline = f.readline();

        trn.write( firstline );
        dev.write( firstline );

        if firstline and firstline[-1] == '\n':
          firstline = firstline[:-1];
        firstline = firstline.split( '\t' );

        assert \
             firstline \
          == (   [ '"id"', '"y"', '"cId"' ]
               + [ '"x{}"'.format(i) for i in range(1,101) ] );

        for line in f:
          if random() < 0.15:
            dev.write( line );
          else:
            trn.write( line );



def main( datadir ):

  step01( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
