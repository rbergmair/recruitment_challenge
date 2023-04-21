from pickle import load as pickle_load;

import matplotlib.pyplot as plt;
import numpy as np;
from numpy import linalg as LA;

from functools import reduce;



DIMCLUSTERs \
  = [ [ -55, -27, 15, 21 ],                                    # 0
      [ -61, -11, 6, 8, 28 ],                                  # 1
      [ -59, -35, 3, 14, 16, 32, 38 ],                         # 2
      [ -67, -30, -26, 23, 39, 62 ],                           # 3
      [ -57, 4, 48 ],                                          # 4
      [ -64, -51, -44, 17 ],                                   # 5
      [ -54, -52, -33, 13, 29, 37, 69 ],                       # 6
      [ -68, -53, -36, 5, 66 ],                                # 7
      [ -49, -45, -43, -40, -34, -25, -20, -10, 9, 22, 56 ],   # 8
      [ -65, -58, 7 ],                                         # 9
      [ 1, 2, 31 ]                                             # 10
    ];

DIMCLUSTERs \
  = [ [ -55, -27, 15, 21 ],                                    # 0  0

      [ -61, -11, 6, 8, 28 ]                                   # 1  1
      + [ -1, -2, -31 ]                                        # 10
      + [ 57, -4, -48 ]                                        # 4
      + [ 64, 51, 44, -17 ]                                    # 5
      + [ 65, 58, -7 ],                                        # 9

      [ -59, -35, 3, 14, 16, 32, 38 ]                          # 2  2
      + [ 54, 52, 33, -13, -29, -37, -69 ]                     # 6
      + [ -68, -53, -36, 5, 66 ]                               # 7
      + [ 49, 45, 43, 40, 34, 25, 20, 10, -9, -22, -56 ]       # 8
      + [ 67, 30, 26, -23, -39, -62 ],                         # 3
    ];


USE_MAHALANOBIS \
  = True;



def step18( datadir, subsample ):

  data_pos = [];
  data_neg = [];

  with open( datadir+'/step07_'+subsample+'.pickle', 'rb' ) as f:
    data = pickle_load( f );

  rowcount = 0;

  for ( y, x ) in data:
    
    rowcount += 1;
    if rowcount > 2500:
      break;

    row = [];

    for ( i, dims ) in enumerate( DIMCLUSTERs ):
      xval = 0.0;
      nx = 0.0;
      for dim in dims:
        if dim < 0:
          xval += -x[ abs(dim)-1 ];
        else:
          xval += x[ abs(dim)-1 ];
        nx += 1.0;        
      row.append( xval/nx );

    if y == '0':
      data_neg.append( row );
    elif y == '1':
      data_pos.append( row );

  print( len(data_pos), len(data) );
  
  ratio = float( len(data_pos) ) / float( len(data) )
  
  pthresholds \
    = [ ratio * ( float(i) / 10.0 ) for i in range(5,26) ];
  dthresholds \
    = [ ( 0.5 + 0.1417 * float(len(DIMCLUSTERs)-3) ) * float(i)/10.0 \
        for i in range(5,26) ];

  print( ", ".join( [ "{:1.4f}".format(p) for p in pthresholds ] ) );
  print( ", ".join( [ "{:1.4f}".format(d) for d in dthresholds ] ) );

  cov = np.cov( np.array( data_pos+data_neg ).T );
  cov_inv = LA.inv( cov );

  print( cov );
  print( cov_inv );

  data_pos = np.array( data_pos );
  data_neg = np.array( data_neg );

  with open( datadir+'/step18_'+subsample+'.csv', 'wt' ) as out:

    for p_threshold in pthresholds:

      for d_threshold in dthresholds:

        print( '  {:1.2f} {:1.2f}'.format( p_threshold, d_threshold ) );

        total_covered = set();
        pos_covered = set();
        
        for (i,ref_row) in enumerate( data_pos ):

          pos_in_vicinity = set();
          neg_in_vicinity = set();

          ref_row_vec = ref_row.reshape(1,len(ref_row)).T;

          for (j,pos_row) in enumerate( data_pos ):

            pos_row_vec = pos_row.reshape(1,len(pos_row)).T;
            diff = pos_row_vec - ref_row_vec;
            if USE_MAHALANOBIS:
              dist = np.sqrt( np.dot( np.dot( diff.T, cov_inv ), diff ) );
            else:
              dist = LA.norm( diff );

            if dist <= d_threshold:
              pos_in_vicinity.add( j );             

          for (j,neg_row) in enumerate( data_neg ):

            neg_row_vec = neg_row.reshape(1,len(neg_row)).T;
            diff = neg_row_vec - ref_row_vec;
            if USE_MAHALANOBIS:
              dist = np.sqrt( np.dot( np.dot( diff.T, cov_inv ), diff ) );
            else:
              dist = LA.norm( diff );

            if dist <= d_threshold:
              neg_in_vicinity.add( j );
          
          total_in_vicinity = len( pos_in_vicinity ) + len( neg_in_vicinity );

          if total_in_vicinity < 7:
            continue;

          p = float( len( pos_in_vicinity ) ) / float( total_in_vicinity );

          if p > p_threshold:
            total_covered |= pos_in_vicinity;
            total_covered |= neg_in_vicinity;
            pos_covered |= pos_in_vicinity;
            # print( '  ', d_threshold, *stats );

        if ( len(total_covered) > 1 ):
          recall = float( len(pos_covered) ) / float( len(data_pos) );
          precision = float( len(pos_covered) ) / float( len(total_covered) );
          f1 = 2.0 * ( precision * recall ) / ( precision + recall );
          print( '-> {:1.2f} {:1.2f} {:1.4f} {:1.4f} {:1.4f}'.format( p_threshold, d_threshold, f1, precision, recall ) );
          print( '{:1.2f};{:1.2f};{:1.4f};{:1.4f};{:1.4f}'.format( p_threshold, d_threshold, f1, precision, recall ), file=out );



def main( datadir ):

  step18( datadir, 'data' );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
