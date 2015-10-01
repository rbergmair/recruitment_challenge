import numpy as np;
from sklearn.decomposition import KernelPCA;

from so1rb.so1rb_frontend.fe import Frontend;



class KPCAContinuousFrontend( Frontend ):


  def __init__( self ):

    self._lenrow = None;
    self._rowcount = 0;
    self._data = [];
    self._kpca = None;


  def __getstate__( self ):

    return self._kpca;


  def __setstate___( self, state ):

    self._kpca = state;


  def train( self, row ):

    if self._rowcount >= 50000:
      return True;

    self._data.append( row );

    self._rowcount += 1;
    if self._rowcount >= 50000:
      return True;

    return False;


  def finalize( self ):

    self._kpca = KernelPCA( n_components=3, kernel='cosine' );
    self._kpca.fit( np.array( self._data ) );
