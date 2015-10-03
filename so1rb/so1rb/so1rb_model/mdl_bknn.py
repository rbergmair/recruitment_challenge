from pickle import load as pickle_load;
from pickle import dump as pickle_dump;
from struct import pack, unpack;
from os import remove;
from os.path import isfile;


import numpy as np;
from numpy import linalg as LA;

from kyotocabinet import DB;


from so1rb.so1rb_model.mdl import Model;



class BKNNModel( Model ):


  def __init__( self, fn, mode, catfe, binfe, contfe, fdisc, fsel ):

    Model.__init__( self, fn, mode, catfe, binfe, contfe, fdisc, fsel );

    self._fn_cdata = self._fn;
    self._fn_ddata = self._fn.replace( '.kch', '-discrete.kch' );
    self._fn_dom = self._fn.replace( '.kch', '-dom.pickle' );
    self._fn_icov = self._fn.replace( '.kch', '-icov.pickle' );

    self._cdata = None;
    self._ddata = None;

    self._dom_c = [];
    self._dom_b = [];
    self._dom_x = [];

    self._icov = None;

    self._covsample = [];

    self._needs_finalization = False;


  def __enter__( self ):

    self._cdata = DB();
    self._ddata = DB();

    try:
      if self._mode == "r":
        assert self._cdata.open( self._fn_cdata, DB.OREADER );
      elif self._mode == "w":
        if isfile( self._fn_cdata ):
          remove( self._fn_cdata );
        assert self._cdata.open( self._fn_cdata, DB.OWRITER | DB.OCREATE );
      else:
        assert False;
    except:
      if self._cdata is not None:
        print( str( self._cdata.error() ) );
      raise;

    try:
      if self._mode == "r":
        assert self._ddata.open( self._fn_ddata, DB.OREADER );
      elif self._mode == "w":
        if isfile( self._fn_ddata ):
          remove( self._fn_ddata );
        assert self._ddata.open( self._fn_ddata, DB.OWRITER | DB.OCREATE );
      else:
        assert False;
    except:
      if self._ddata is not None:
        print( str( self._ddata.error() ) );
      raise;

    if self._mode == "r":

      with open( self._fn_dom, 'rb' ) as f:
        r = pickle_load( f );
        self._dom_c = r[0];
        self._dom_b = r[1];
        self._dom_x = r[2];    

      with open( self._fn_icov, 'rb' ) as f:
        self._icov = pickle_load( f );

    return self;


  def __exit__( self, exc_type, exc_value, traceback ):

    ex_w_exc = False;
    ex_w_exc = ex_w_exc or ( exc_type is not None );
    ex_w_exc = ex_w_exc or ( exc_value is not None );
    ex_w_exc = ex_w_exc or ( traceback is not None );

    if ( not ex_w_exc ) and ( self._mode == "w" ):

      if self._needs_finalization:
        self._finalize();

      with open( self._fn_dom, 'wb' ) as f:

        r = ( self._dom_c,
              self._dom_b,
              self._dom_x )

        pickle_dump( r, f );

      with open( self._fn_icov, 'wb' ) as f:

        pickle_dump( self._icov, f );

    if self._cdata is not None:
      try:
        assert self._cdata.close();
      except:
        print( str( self._cdata.error() ) );
        raise;
      self._cdata = None;

    if self._ddata is not None:
      try:
        assert self._ddata.close();
      except:
        print( str( self._ddata.error() ) );
        raise;
      self._ddata = None;

    if ex_w_exc and ( self._mode == "w" ):

      if isfile( self._fn_cdata ):
        remove( self._fn_cdata );

      if isfile( self._fn_ddata ):
        remove( self._fn_ddata );

      if isfile( self._fn_dom ):
        remove( self._fn_dom );

      if isfile( self._fn_icov ):
        remove( self._fn_icov );

    return False;


  def train( self, row ):

    self._needs_finalization = True;

    ( y, c, b, x ) = row;

    c = self._fsel.apply_c( self._catfe( c ) );
    b = self._fsel.apply_b( self._binfe( b ) );

    x = self._contfe( x );
    x_ = self._fdisc( x );

    x = self._fsel.apply_x( x );
    x_ = self._fsel.apply_x( x_ );

    if False:
      print( y, c, b, x, x_ );

    if not self._dom_c:
      for i in range( 0, len(c) ):
        self._dom_c.append( set() );
    for i in range( 0, len(c) ):
      self._dom_c[ i ].add( c[i] );

    if not self._dom_b:
      for i in range( 0, len(b) ):
        self._dom_b.append( set() );
    for i in range( 0, len(b) ):
      self._dom_b[ i ].add( b[i] );

    if not self._dom_x:
      for i in range( 0, len(x_) ):
        self._dom_x.append( set() );
    for i in range( 0, len(x_) ):
      self._dom_x[ i ].add( x_[i] );

    dkey = '>' + ( 'I' * len(c+b) );
    self._ddata.increment( pack( dkey, *(c+b) ), 1, 0 );

    ckey = '>' + ( 'I' * len(x_) );
    cval = '>' + ( 'f' * len(x) );
    self._cdata.append( pack( ckey, *x_ ), pack( cval, *x ) );

    if len( self._covsample ) < 50000:
      self._covsample.append( x );

    return False;


  def _finalize( self ):

    self._needs_finalization = False;

    covsample = np.array( self._covsample );
    cov = np.cov( covsample.T );
    self._icov = LA.inv( cov );

    return None;
