import numpy as np;
from copy import copy;

from so1rb.so1rb_frontend.fe import Frontend;



class HomebrewContinuousFrontend( Frontend ):


  def __init__( self, fn, mode ):

    Frontend.__init__( self, fn, mode );
    self._max_rows = 100000;

    self._data = [];


  def train( self, row ):

    if Frontend.train( self, row ):
      return True;

    self._data.append( row );

    return False;


  def _cluster_val( self, data, dims ):

    vals = None;
    for dim in dims:
      if vals is None:
        vals = copy( data[ abs(dim)-1 ] );
      elif dim > 0:
        vals += data[ abs(dim)-1 ];
      elif dim < 0:
        vals -= data[ abs(dim)-1 ];
      else:
        assert False;

    vals /= len(dims);

    return vals;


  def _merge( self, data, dim_clusters ):

    maxcorr = None;
    maxcorr_dims = None;

    for ( i, dci ) in enumerate( dim_clusters ):

      ivals = self._cluster_val( data, dci );

      for ( j, dcj ) in enumerate( dim_clusters ):

        if i >= j:
          continue;

        jvals = self._cluster_val( data, dcj );

        corr = np.corrcoef( ivals, jvals )[ 0 ][ 1 ];

        if ( maxcorr is None ) or ( abs(corr) > abs(maxcorr) ):
          maxcorr = corr;
          maxcorr_dims = (i,j);

    if abs( maxcorr ) < 0.33:
      return dim_clusters;

    (i,j) = maxcorr_dims;

    dim_i = dim_clusters[i];
    dim_j = dim_clusters[j];
    dim_clusters.remove( dim_i );
    dim_clusters.remove( dim_j );
    
    if maxcorr < 0.0:
      dim_j_ = set();
      for j in dim_j:
        dim_j_.add( -j );
      dim_j = dim_j_;

    dim_clusters.append( dim_i | dim_j );

    return dim_clusters;


  def _finalize( self ):

    assert Frontend._finalize( self ) is None;

    data = np.array( self._data ).T;

    rest = [];
    for i in range( 1, len(data)+1 ):
      rest.append( {i} );

    while True:
      len_rest_before = len(rest);
      rest = self._merge( data, rest );    
      # print( rest );
      if len( rest ) == len_rest_before:
        break;

    self._state = rest;

    if False:

      print( "-- CLUSTERS --" );

      print( len(rest), rest );

    if False:

      print( "-- INSIDE CORRELATIONS --" );

      for dc in rest:
        print( dc );
        for di in dc:
          for dj in dc:
            if abs(di) >= abs(dj):
              continue;
            corr = np.corrcoef( data[abs(di)-1], data[abs(dj)-1] )[ 0 ][ 1 ];
            print( di, dj, corr );

    if False:

      print( "-- OUTSIDE CORRELATIONS --" );

      for ( i, dci ) in enumerate( rest ):
        ivals = self._cluster_val( data, dci );
        for ( j, dcj ) in enumerate( rest ):
          if i >= j:
            continue;
          jvals = self._cluster_val( data, dcj );
          corr = np.corrcoef( ivals, jvals )[ 0 ][ 1 ];
          print( i, j, corr );


  def __call__( self, row ):

    assert Frontend.__call__( self, row ) is row;

    row_ = [];

    for cluster in self._state:

      val = 0.0;

      for dim in cluster:
        if dim > 0:
          val += row[dim];
        else:
          assert dim < 0;
          val -= row[dim];

      val /= len(cluster);

      row_.append( val );

    return row_;
