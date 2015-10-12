from os.path import isfile;
from random import random;
from gzip import open as gzip_open;
from math import floor, sqrt;

import numpy as np;
import matplotlib.pyplot as plt;



def step12( datadir ):

  with open( datadir+"/step12_pos.txt", "wt" ) as pos:
    with open( datadir+"/step12_neg.txt", "wt" ) as neg:
      with gzip_open( datadir+"/train.tsv.gz", "rt" ) as f:

        firstline = f.readline();

        if firstline and firstline[-1] == '\n':
          firstline = firstline[:-1];
        firstline = firstline.split( '\t' );

        assert \
             firstline \
          == (   [ '"id"', '"y"', '"cId"' ]
               + [ '"x{}"'.format(i) for i in range(1,101) ] );

        max_len_bin = 0;
        max_len_cnt = 0;

        pos_n = 0;
        pos_sumx1 = 0;
        pos_sumx1sq = 0;
        pos_sumx2 = 0;
        pos_sumx2sq = 0;
        pos_valsx1 = [];
        pos_valsx2 = [];

        neg_n = 0;
        neg_sumx1 = 0;
        neg_sumx1sq = 0;
        neg_sumx2 = 0;
        neg_sumx2sq = 0;
        neg_valsx1 = [];
        neg_valsx2 = [];

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
          allx = [ None ];
          cntx = [ None ];
          assert cid.startswith( '"' );
          assert cid.endswith( '"' );
          cid = int( cid[1:-1] );

          for x in line[3:]:

            if "." in x:
              max_len_cnt = max( max_len_cnt, len(x) );
            else:
              max_len_bin = max( max_len_bin, len(x) );

            if "." in x:

              if not x.startswith('-'):
                x = '+'+x;
              xorig = x;
              while len(x) < 6:
                x = x + '0';
              x = x.replace( '.', '' );
              x = int(x);
              if False:
                x = hex(x);
                if x.startswith('-'):
                  x = '-' + x[3:].zfill(3);
                else:
                  x = '+' + x[2:].zfill(3);
              cntx.append( x );

            else:

              x = int(x);

            allx.append( x );          

          x1 = allx[cid];
          x2 = cntx[cid];

          if y == '0':

            print( id_, y, cid, x1, x2, *allx[1:], sep='\t', file=neg );

            neg_n += 1;
            neg_sumx1 += x1;
            neg_sumx1sq += x1*x1;
            neg_sumx2 += x2;
            neg_sumx2sq += x2*x2;

            neg_valsx1.append(x1);
            neg_valsx2.append(x2);

          elif y == '1':

            print( id_, y, cid, allx[cid], cntx[cid], *allx[1:], sep='\t', file=pos );

            pos_n += 1;
            pos_sumx1 += x1;
            pos_sumx1sq += x1*x1;
            pos_sumx2 += x2;
            pos_sumx2sq += x2*x2;

            pos_valsx1.append(x1);
            pos_valsx2.append(x2);


  print( max_len_bin, max_len_cnt );

  neg_avg_x1 = float(neg_sumx1) / float(neg_n);
  neg_std_x1 = ( float(neg_sumx1sq) / float(neg_n) ) - neg_avg_x1*neg_avg_x1;
  pos_avg_x1 = float(pos_sumx1) / float(pos_n);
  pos_std_x1 = ( float(pos_sumx1sq) / float(pos_n) ) - pos_avg_x1*pos_avg_x1;

  neg_avg_x2 = float(neg_sumx2) / float(neg_n);
  neg_std_x2 = ( float(neg_sumx2sq) / float(neg_n) ) - neg_avg_x2*neg_avg_x2;
  pos_avg_x2 = float(pos_sumx2) / float(pos_n);
  pos_std_x2 = ( float(pos_sumx2sq) / float(pos_n) ) - pos_avg_x2*pos_avg_x2;

  print( '--> 1', neg_avg_x1, sqrt(neg_std_x1), pos_avg_x1, sqrt(pos_std_x1) );
  print( '--> 2', neg_avg_x2, sqrt(neg_std_x2), pos_avg_x2, sqrt(pos_std_x2) );

  ( fig, ax ) = plt.subplots( nrows=1, ncols=2, figsize=(8,4) );
  ax[0].hist( [ neg_valsx1, pos_valsx1 ], 20, histtype='bar', color='br', label='rb' );  
  ax[1].hist( [ neg_valsx2, pos_valsx2 ], 20, histtype='bar', color='br', label='rb' );  
  fig.savefig( datadir+'/step12.png' );



def main( datadir ):

  step12( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
