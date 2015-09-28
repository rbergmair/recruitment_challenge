from pickle import load as pickle_load;

import matplotlib.pyplot as plt;
import numpy as np;
from numpy import linalg as LA;

from sklearn.decomposition import PCA, KernelPCA;

from functools import reduce;



# based on step07_all_data.pickle
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

# based on step07_data.pickle
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

# based on step07_all_data.pickle plus manual fiddling (best)
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


def step17( datadir, n_components ):

  n_components = int(n_components);

  data_ = [];
  classlabels = [];

  with open( datadir+'/step07_data.pickle', 'rb' ) as f:
    data__ = pickle_load( f );

  posdims = [];
  negdims = [];
  for dimcluster in DIMCLUSTERs:
    for dim in dimcluster:
      if dim < 0:
        negdims.append( abs(dim) );
      else:
        posdims.append( abs(dim) );

  rowcount = 0;
  poscnt = 0;
  negcnt = 0;

  for ( y, x ) in data__:
    
    rowcount += 1;
    if rowcount > 10000:
      break;

    row = [];
    for (dim,xval) in enumerate(x[1:]):
      if dim in posdims:
        row.append( xval );
      elif dim in negdims:
        # row.append( -xval );
        row.append( xval );
      else:
        #print( "skipping dim", dim );
        row.append( xval );

    data_.append( row );

    if y == '0':
      classlabels.append( 0 );
      negcnt += 1;
    elif y == '1':
      classlabels.append( 1 );
      poscnt += 1;

  data_ = np.array( data_ );
  classlabels = np.array( classlabels );

  ratio = float( poscnt ) / float( poscnt+negcnt );

  data = KernelPCA( n_components=n_components, kernel='cosine' ).fit_transform( data_ );

  print( data[0] );

  pthresholds \
    = [ ratio * ( float(i) / 10.0 ) for i in range(5,26) ];
  dthresholds \
    = [ ( 0.5 + 0.1417 * float(n_components-3) ) * float(i)/10.0 \
        for i in range(5,15) ];

  print( " ".join( [ "{:1.4f}".format(p) for p in pthresholds ] ) );
  print( " ".join( [ "{:1.4f}".format(d) for d in dthresholds ] ) );

  cov = np.cov( data.T );
  cov_inv = LA.inv( cov );

  print( cov );
  print( cov_inv );

  with open( datadir+'/step19_explore_the_neighborhood_even_more_{}.csv'.format( n_components ), 'wt' ) as out:

    for p_threshold in pthresholds:

      for d_threshold in dthresholds:

        print( '  {:1.2f} {:1.2f}'.format( p_threshold, d_threshold ) );

        total_covered = set();
        pos_covered = set();
        
        for (i,ref_row) in enumerate( data ):

          if classlabels[i] != 1:
            continue;

          pos_in_vicinity = set();
          neg_in_vicinity = set();

          ref_row_vec = ref_row.reshape(1,len(ref_row)).T;

          for (j,row) in enumerate( data ):

            row_vec = row.reshape(1,len(row)).T;
            diff = row_vec - ref_row_vec;
            # dist = LA.norm( diff );
            dist = np.sqrt( np.dot( np.dot( diff.T, cov_inv ), diff ) );
            if dist <= d_threshold:
              if classlabels[j] == 0:
                neg_in_vicinity.add( j );
              else:
                assert classlabels[j] == 1;
                pos_in_vicinity.add( j );
          
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
          recall = float( len(pos_covered) ) / float( poscnt );
          precision = float( len(pos_covered) ) / float( len(total_covered) );
          f1 = 2.0 * ( precision * recall ) / ( precision + recall );
          print( '-> {:1.2f} {:1.2f} {:1.4f} {:1.4f} {:1.4f}'.format( p_threshold, d_threshold, f1, precision, recall ) );
          print( '{:1.2f};{:1.2f};{:1.4f};{:1.4f};{:1.4f}'.format( p_threshold, d_threshold, f1, precision, recall ), file=out );



def main( datadir, n_components ):

  step17( datadir, n_components );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
