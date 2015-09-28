from pickle import load as pickle_load;

import matplotlib.pyplot as plt;
import numpy as np;
from numpy import linalg as LA;

from functools import reduce;



# based on step07_all_data.pickle 2
DIMCLUSTERs \
  = [ [ -26, 20, 14, -54 ],                                  # 0
      [ 32, 2, -34, -36, -12, 13, 15, 51, 53, 24, 31 ],      # 1
      [ -64, -57, 60, 6, -63 ],                              # 2
      [ -33, -39, 8, -9, -42, -44, -48, -19, 21, 55 ],       # 3
      [ 0, 1, 30 ],                                          # 4
      [ -56, 3, 47 ],                                        # 5
      [ -35, 4, -67 ],                                       # 6
      [ 65, 66, 37, -38, -52, 25, -58, -61 ],                # 7
      [ 50, 43, 28, 68 ],                                    # 8
      [ 27, 5, 7 ]                                           # 9
    ];

# based on step07_data.pickle 1
DIMCLUSTERs \
  = [ [ 5, 7, -10, 27, -60, -30 ],                           # 0
      [ 0, 1, -57, -64, 6 ],                                 # 1
      [ -33, -39, 8, -9, -42, -44, -48, -19, 21, 55, -24 ],  # 2
      [ -54, -26, 29, 14, -22 ],                             # 3
      [ 16, -50, -43, -63 ],                                 # 4
      [ -56, 3, 47 ],                                        # 5
      [ 31, -34, 13, 15 ],                                   # 6
      [ 65, 2, 66, 37, -38, -52, 25, -58, -61 ],             # 7
      [ -32, 36, 68, 12, -51, -53, 28 ]                      # 8
    ];

# based on step07_all_data.pickle plus manual fiddling ?
DIMCLUSTERs \
  = [ [ -26, 20, 14, -54 ]                                   # 0     # 0
      + [ -27, -5, -7 ],                                     # -9

      [ 32, 2, -34, -36, -12, 13, 15, 51, 53, 24, 31 ]       # 1     # 1
      + [ 65, 66, 37, -38, -52, 25, -58, -61 ]               # 7      
      + [ 33, 39, -8, 9, 42, 44, 48, 19, -21, -55 ]          # -3
      + [ -50, -43, -28, -68 ]                               # -8
      + [ -56, 3, 47 ]                                       # 5
      + [ -35, 4, -67 ],                                     # 6

      [ -64, -57, 60, 6, -63 ]                               # 2     # 2
      + [ 0, 1, 30 ],                                        # 4
    ];


def step17( datadir ):

  data_pos = [];
  data_neg = [];

  with open( datadir+'/step07_data.pickle', 'rb' ) as f:
    data = pickle_load( f );

  rowcount = 0;

  for ( y, x ) in data:
    
    rowcount += 1;
    if rowcount > 10000:
      break;

    row = [];

    for ( i, dims ) in enumerate( DIMCLUSTERs ):
      xval = 0.0;
      nx = 0.0;
      for dim in dims:
        if dim < 0:
          xval += -x[ 1+abs(dim) ];
        else:
          xval += x[ 1+abs(dim) ];
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

  print( " ".join( [ "{:1.4f}".format(p) for p in pthresholds ] ) );
  print( " ".join( [ "{:1.4f}".format(d) for d in dthresholds ] ) );

  cov = np.cov( np.array( data_pos+data_neg ).T );
  cov_inv = LA.inv( cov );

  print( cov );
  print( cov_inv );

  data_pos = np.array( data_pos );
  data_neg = np.array( data_neg );

  with open( datadir+'/step18_explore_the_neighborhood_some_more.csv', 'wt' ) as out:

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
            dist = np.sqrt( np.dot( np.dot( diff.T, cov_inv ), diff ) );
            if dist <= d_threshold:
              pos_in_vicinity.add( j );

          for (j,neg_row) in enumerate( data_neg ):

            neg_row_vec = neg_row.reshape(1,len(neg_row)).T;
            diff = neg_row_vec - ref_row_vec;
            dist = np.sqrt( np.dot( np.dot( diff.T, cov_inv ), diff ) );
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

  step17( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
