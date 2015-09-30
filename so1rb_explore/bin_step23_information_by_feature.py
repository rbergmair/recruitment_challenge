from os.path import isfile;
from math import log;

from gzip import open as gzip_open;

from pickle import load as pickle_load;
from pickle import dump as pickle_dump;

from struct import pack, unpack;

from time import sleep;

from pprint import pprint;

import plyvel;


def step23( datadir ):

  with open( datadir + '/step23_feature_strengths.csv', 'wt' ) as outf:
    
    for dim in range( 0, 30 ):

      total_neg_0_ = 0;
      total_neg_1_ = 0;
      total_pos_0_ = 0;
      total_pos_1_ = 0;

      count_by_pq = {};
      count_by_q = {};

      i = 0;

      with open( datadir + '/step22_data.pickle', 'rb' ) as f:

        while True:

          is_eof = None;
          try:
            ( y, cid, x, b ) = pickle_load( f );
            is_eof = False;
          except EOFError:
            is_eof = True;

          if is_eof:
            break;

          i += 1;
          #if i >= 10000:
          #  break;

          if y == '0':
            if b[ dim ] == 0:
              total_neg_0_ += 1;
            else:
              assert b[ dim ] == 1;
              total_neg_1_ += 1;
          else:
            assert y == '1';
            if b[ dim ] == 0:
              total_pos_0_ += 1;
            else:
              assert b[ dim ] == 1;
              total_pos_1_ += 1;

          q = ( y, ) + tuple(x);
          pq = ( y, b[dim] ) + tuple(x);

          count_by_q[ q ] = count_by_q.get( q, 0 ) + 1;
          count_by_pq[ pq ] = count_by_pq.get( pq, 0 ) + 1;

      total_neg_ = total_neg_0_ + total_neg_1_;
      total_pos_ = total_pos_0_ + total_pos_1_;
      oversampling_factor = float(total_neg_) / float(total_pos_);

      total_0 = float( total_neg_0_ ) + ( float( total_pos_0_ ) * oversampling_factor );
      total_1 = float( total_neg_1_ ) + ( float( total_pos_1_ ) * oversampling_factor );
      total = total_0 + total_1;

      p_0 = total_0 / total;
      p_1 = total_1 / total;

      h_p = 0.0;
      h_p -= p_0 * log( p_0, 2.0 );
      h_p -= p_1 * log( p_1, 2.0 );

      h_q = 0.0;
      for ( ( y, x0, x1, x2 ), cnt ) in count_by_q.items():
        if y == '0':
          cnt = float(cnt);
        else:
          assert y == '1';
          cnt = float(cnt) * oversampling_factor;
        p = cnt / total;
        h_q -= p * log( p, 2.0 );

      h_pq = 0.0;
      for ( ( y, b, x0, x1, x2 ), cnt ) in count_by_pq.items():
        if y == '0':
          cnt = float(cnt);
        else:
          assert y == '1';
          cnt = float(cnt) * oversampling_factor;
        p = cnt / total;
        h_pq -= p * log( p, 2.0 );

      i = h_p + h_q - h_pq;

      if False:

        print( "total_neg_0_ = {:d}".format(total_neg_0_) );
        print( "total_neg_1_ = {:d}".format(total_neg_1_) );
        print( "total_pos_0_ = {:d}".format(total_pos_0_) );
        print( "total_pos_1_ = {:d}".format(total_pos_1_) );

        print( "h_p = {:2.6f}".format(h_p) );
        print( "h_q = {:2.6f}".format(h_q) );
        print( "h_pq = {:2.6f}".format(h_pq) );
        print( "i = {:2.6f}".format(i) );

      print( dim, "{:1.4f}".format( i / h_p ), sep='|' );
      print( dim, "{:1.4f}".format( i / h_p ), sep='|', file=outf );



def main( datadir ):

  step23( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
