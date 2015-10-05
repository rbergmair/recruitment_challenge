from pickle import load as pickle_load;
from pickle import dump as pickle_dump;



class Frontend:


  def __init__( self, fn, mode ):

    self._fn = fn;
    self._mode = mode;
    self._needs_finalization = False;
    self._max_rows = None;
    self._lenrow = None;
    self._rowcount = 0;    
    self._state = None;


  def __enter__( self ):

    if self._mode == "r":
      with open( self._fn, "rb" ) as f:
        self._state = pickle_load( f );
    return self;


  def __exit__( self, exc_type, exc_value, traceback ):

    if exc_type is None and exc_value is None and traceback is None:

      if self._needs_finalization:
        self._finalize();

      if self._mode == "w":
        with open( self._fn, "wb" ) as f:
          pickle_dump( self._state, f );

    return False;


  def train( self, row ):

    self._needs_finalization = True;

    if self._lenrow is None:
      self._lenrow = len( row );
    assert self._lenrow == len( row );

    self._rowcount += 1;
    if self._max_rows is not None and self._rowcount >= self._max_rows:
      return True;

    return False;


  def _finalize( self ):

    self._needs_finalization = False;
    return None;


  def __call__( self, row ):

    if self._needs_finalization:
      self._finalize();      
    return row;
