from os.path import isfile;
from random import random, choice;
from gzip import open as gzip_open;
from math import floor, sqrt;

import numpy as np;
import matplotlib.pyplot as plt;



def step13( datadir ):

  with gzip_open( datadir+"/train.tsv.gz", "rt" ) as f:

    firstline = f.readline();

    if firstline and firstline[-1] == '\n':
      firstline = firstline[:-1];
    firstline = firstline.split( '\t' );

    assert \
         firstline \
      == (   [ '"id"', '"y"', '"cId"' ]
           + [ '"x{}"'.format(i) for i in range(1,101) ] );

    pos_valsx = [];
    neg_valsx = [];
    pos_rndx = [];
    neg_rndx = [];

    pos_valsx_ = [];
    neg_valsx_ = [];
    pos_rndx_ = [];
    neg_rndx_ = [];

    i = 1;
    for line in f:

      i += 1;
      if i > 10000:
        break;

      line_ = line;

      if line and line[-1] == '\n':
        line = line[:-1];
      line = line.split( '\t' );

      id_ = line[0];
      y = line[1];
      cid = line[2];
      x = [ None ];
      assert cid.startswith( '"' );
      assert cid.endswith( '"' );
      cid = int( cid[1:-1] );

      for x_ in line[3:]:
        x.append( float(x_) )

      relevant_x = x[cid];
      random_x = choice( x[1:] );

      if y == '0':

        neg_valsx.append(relevant_x);
        if relevant_x not in [ 0.0, 1.0 ]:
          neg_valsx_.append(relevant_x);

        neg_rndx.append(random_x);
        if random_x not in [ 0.0, 1.0 ]:
          neg_rndx_.append(random_x);

      elif y == '1':

        pos_valsx.append(relevant_x);
        if relevant_x not in [ 0.0, 1.0 ]:
          pos_valsx_.append(relevant_x);

        pos_rndx.append(random_x);
        if random_x not in [ 0.0, 1.0 ]:
          pos_rndx_.append(random_x);

  ( fig, ax ) = plt.subplots( nrows=2, ncols=2, figsize=(6,6) );
  ax[0,0].hist( [ neg_valsx, pos_valsx ], 100, histtype='step', color='br', linewidth=3 );  
  ax[0,1].hist( [ neg_rndx, pos_rndx ], 100, histtype='step', color='br', linewidth=3 );  
  ax[1,0].hist( [ neg_valsx_, pos_valsx_ ], 100, histtype='step', color='br', linewidth=3 );  
  ax[1,1].hist( [ neg_rndx_, pos_rndx_ ], 100, histtype='step', color='br', linewidth=3 );  
  fig.savefig( datadir+'/step13.png' );



def main( datadir ):

  step13( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
