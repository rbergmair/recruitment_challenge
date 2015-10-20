from pickle import load as pickle_load;

import matplotlib.pyplot as plt;
import numpy as np;
from numpy import linalg as LA;

from sklearn.decomposition import PCA, KernelPCA;

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



def step19( datadir, subsample, kernel ):

  data_ = [];
  classlabels = [];

  with open( datadir+'/step07_'+subsample+'.pickle', 'rb' ) as f:
    data__ = pickle_load( f );

  posdims = [];
  negdims = [];
  for dimcluster in DIMCLUSTERs:
    for dim in dimcluster:
      if dim < 0:
        negdims.append( abs(dim)-1 );
      else:
        posdims.append( abs(dim)-1 );

  rowcount = 0;
  poscnt = 0;
  negcnt = 0;

  for ( y, x ) in data__:
    
    rowcount += 1;
    if rowcount > 2500:
      break;

    row = [];
    for (dim,xval) in enumerate(x):
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

  if kernel == 'pca':
    data = PCA( n_components=3 ).fit_transform( data_ );
  else:
    data = KernelPCA( n_components=3, kernel=kernel ).fit_transform( data_ );

  print( data[0] );

  pthresholds \
    = [ ratio * ( float(i) / 10.0 ) for i in range(5,26) ];
  dthresholds \
    = [ ( 0.5 + 0.1417 * float(3-3) ) * float(i)/10.0 \
        for i in range(5,15) ];

  print( ", ".join( [ "{:1.4f}".format(p) for p in pthresholds ] ) );
  print( ", ".join( [ "{:1.4f}".format(d) for d in dthresholds ] ) );

  cov = np.cov( data.T );
  cov_inv = LA.inv( cov );

  print( cov );
  print( cov_inv );

  with open( datadir+'/step19_{}.csv'.format( kernel ), 'wt' ) as out:

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



def main( datadir ):

  step19( datadir, 'data', 'cosine' );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
