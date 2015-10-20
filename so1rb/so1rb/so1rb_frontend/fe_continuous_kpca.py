import numpy as np;
from sklearn.decomposition import KernelPCA;

from so1rb.so1rb_frontend.fe import Frontend;



class KPCAContinuousFrontend( Frontend ):


  def __init__( self, fn, mode ):

    Frontend.__init__( self, fn, mode );
    self._max_rows = 50000;

    self._data = [];


  def train( self, row ):

    if Frontend.train( self, row ):
      return True;

    self._data.append( row );

    return False;


  def _finalize( self ):

    assert Frontend._finalize( self ) is None;

    self._state = KernelPCA( n_components=3, kernel='cosine' );
    self._state.fit( np.array( self._data ) );


  def __call__( self, row ):

    assert Frontend.__call__( self, row ) is row;
    return list( self._state.transform( row )[ 0 ] );
