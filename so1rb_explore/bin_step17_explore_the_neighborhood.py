from pickle import load as pickle_load;

import matplotlib.pyplot as plt;
import numpy as np;
from numpy import linalg as LA;

from functools import reduce;



# all dimensions
DIMs \
  = range(0,70);

# interesting dimensions as per results from step 14
DIMs \
  = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 19, 20, 21, 22,
      24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 42, 43,
      44, 47, 48, 50, 51, 52, 53, 54, 55, 56, 57, 58, 60, 61, 63, 64, 65, 66,
      67, 68 ];

# handful of dimensions for testing
DIMs \
  = [ 0, 21, 42 ];

PTHRESHOLDs \
  = [ 0.1, 0.2, 0.3, 0.4, 0.5 ];

PTHRESHOLDs \
  = [ 0.1, 0.2, 0.3 ];

DTHRESHOLDs \
  = [ ( 0.5 + 0.1417 * float(len(DIMs)-3) ) * float(i)/10.0 \
        for i in range(5,15) ];



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
    for dim in DIMs:
      row.append( x[1+dim] );

    if y == '0':
      data_neg.append( row );
    elif y == '1':
      data_pos.append( row );

  print( len(data_pos), len(data) );
  
  dthresholds = DTHRESHOLDs;
  pthresholds = PTHRESHOLDs

  ratio = float( len(data_pos) ) / float( len(data) )
  
  pthresholds \
    = [ ratio * ( float(i) / 10.0 ) for i in range(5,26) ];
  dthresholds \
    = [ ( 0.5 + 0.1417 * float(len(DIMs)-3) ) * float(i)/10.0 \
        for i in range(5,16) ];

  print( [ "{:1.4f}".format(p) for p in pthresholds ] );
  print( [ "{:1.4f}".format(d) for d in dthresholds ] );

  cov = np.cov( np.array( data_pos+data_neg ).T );
  cov_inv = LA.inv( cov );

  print( cov );
  print( cov_inv );

  data_pos = np.array( data_pos );
  data_neg = np.array( data_neg );

  with open( datadir+'/step17_explore_the_neighborhood.csv', 'wt' ) as out:

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
