class Model:

  def __init__( self, fn, mode, catfe, binfe, contfe, fdisc, fsel ):

    self._fn = fn;
    self._mode = mode;
    self._catfe = catfe;
    self._binfe = binfe;
    self._contfe = contfe;
    self._fdisc = fdisc;
    self._fsel = fsel;


  def __enter__( self ):

    assert False;


  def __exit__( self, exc_type, exc_value, traceback ):

    assert False;


  def train( self, row ):

    assert False;


  def __call__( self, row ):

    assert False;
