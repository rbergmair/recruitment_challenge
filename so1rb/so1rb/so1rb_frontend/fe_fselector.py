from pickle import load as pickle_load;
from tempfile import NamedTemporaryFile, TemporaryDirectory;
from os import remove;
from time import sleep;
from shutil import rmtree;
from pprint import pprint;
from math import log;

from kyotocabinet import DB as KDB;
from kyotocabinet import Visitor as KVisitor;
from plyvel import DB as LDB;

from struct import pack, unpack;


from so1rb import cfg;

from so1rb.so1rb_frontend.fe import Frontend;



class FeatureSelector( Frontend ):


  def __init__( self, fn, mode ):    

    Frontend.__init__( self, fn, mode );

    self._kdbfn = None;
    self._kdb = None;

    self._ldbdn = None;
    self._ldb = None;

    self._len_c = None;
    self._len_b = None;
    self._len_x = None;

    self._ic = None;
    self._icbp = None;

    self._needs_initialization = True;

    self._core_dims = set();
    self._satellite_dims = set();
    self._removed_dims = set();

    self._remove_c = set();
    self._remove_b = set();
    self._remove_x = set();

    self.bypass_c = False;
    self.bypass_b = False;
    self.bypass_x = False;


  def __enter__( self ):

    if self._mode == "r":
      with open( self._fn, "rb" ) as f:
        state = pickle_load( f );
        self._len_c = state[ "c" ];
        self._len_b = state[ "b" ];
        self._len_x = state[ "x" ];
        self._lenrow = self._len_c + self._len_b + self._len_x;
        self._ic = state[ "ic" ];
        self._icbp = state[ "icbp" ];

    if self._mode == "w":

      with NamedTemporaryFile() as tmpfn:
        self._kdbfn = tmpfn.name + '.kch';
      self._kdb = KDB();
      try:
        assert self._kdb.open( self._kdbfn, KDB.OWRITER | KDB.OCREATE );
      except:
        print( str( self._kdb.error() ) );
        raise;

      with TemporaryDirectory() as tmpdirname:
        self._ldbdn = tmpdirname;
      self._ldb = LDB( self._ldbdn, create_if_missing=True );

    return self;

  def __exit__( self, exc_type, exc_value, traceback ):

    assert Frontend.__exit__( self, exc_type, exc_value, traceback ) == False;

    if self._ldb is not None:
      sleep( 3.0 );
      self._ldb.close()

    if self._ldbdn is not None:
      rmtree( self._ldbdn );

    if self._kdb is not None:
      try:
        assert self._kdb.close();
      except:
        print( str( self._kdb.error() ) );
        raise;

    if self._kdbfn is not None:
      remove( self._kdbfn );


  def train( self, row ):

    ( y, c, b, x ) = row;

    if self._len_c is None:
      self._len_c = len(c);
    assert self._len_c == len(c);

    if self._len_b is None:
      self._len_b = len(b);
    assert self._len_b == len(b);

    if self._len_x is None:
      self._len_x = len(x);
    assert self._len_x == len(x);

    row = c + b + x;

    if Frontend.train( self, row ):
      return True;

    keyfmt = '>IIIII';

    for i in range( 0, self._lenrow ):
      for j in range( 0, self._lenrow ):

        if ( i >= j ) and ( not ( i == self._lenrow-1 ) ):
          continue;

        key = pack( keyfmt, i, j, y, row[i], row[j] );

        try:
          assert self._kdb.increment( key, 1, 0 );
        except:
          print( str(self._kdb.error()) );
          raise;


  def _stats( self, cnt_by_a, cnt_by_b, cnt_by_ab ):

    h_a = 0.0;
    h_b = 0.0;
    h_ab = 0.0;

    for ( val_a, cnt ) in cnt_by_a.items():
      p = float(cnt) / float(self._rowcount);
      if p > 0.0:      
        h_a -= p * log( p, 2.0 );

    for ( val_b, cnt ) in cnt_by_b.items():
      p = float(cnt) / float(self._rowcount);
      if p > 0.0:      
        h_b -= p * log( p, 2.0 );

    for( (val_a,val_b), cnt ) in cnt_by_ab.items():
      p = float(cnt) / float(self._rowcount);
      if p > 0.0:      
        h_ab -= p * log( p, 2.0 );

    if h_a == 0.0:
      return 1.0;

    if h_b == 0.0:
      return 1.0;
    
    mi = h_a + h_b - h_ab;
    return ( mi / min( h_a, h_b ), h_a, h_b, h_ab, mi );


  def _get_info_content_by_dimension( self, i ):

    keyfmt = '>IIIII';
    valfmt = '>Q';

    j = None;

    cnt_by_a = {};
    cnt_by_b = {};
    cnt_by_ab = {};
    total = 0;

    with self._ldb.iterator() as it:

      it.seek( pack( keyfmt, i,0,0,0,0 ) );

      for ( key, val ) in it:

        key = unpack( keyfmt, key );
        val = unpack( valfmt, val )[ 0 ];

        if not ( key[0] == i ):
          break;

        if j is None:
          j = key[1];

        if not ( key[1] == j ):
          break;

        # key[2] is the y-value
        a = key[2];

        # key[3] is the value for the i-th dimension
        b = key[3];

        cnt_by_ab[ (a,b) ] = cnt_by_ab.get( (a,b), 0 ) + val;
        cnt_by_a[ a ] = cnt_by_a.get( a, 0 ) + val;
        cnt_by_b[ b ] = cnt_by_b.get( b, 0 ) + val;

        total += val;

    try:
      assert total == self._rowcount;
    except:
      print( i, j, total, self._rowcount );
      raise;

    return self._stats( cnt_by_a, cnt_by_b, cnt_by_ab );


  def _get_info_content_by_pair( self, i, j ):

    keyfmt = '>IIIII';
    valfmt = '>Q';

    cnt_by_a = {};
    cnt_by_b = {};
    cnt_by_ab = {};
    total = 0;

    with self._ldb.iterator() as it:

      it.seek( pack( keyfmt, i,j,0,0,0 ) );

      for ( key, val ) in it:

        key = unpack( keyfmt, key );
        val = unpack( valfmt, val )[ 0 ];

        if not ( ( key[0] == i ) and ( key[1] == j ) ):
          break;

        # key[2] is the y-value, key[3] the i-th value for the i-th dim
        a = ( key[2], key[3] ); 

        # key[2] is the y-value, key[4] the i-th value for the j-th dim
        b = ( key[2], key[4] );

        assert (a,b) not in cnt_by_ab;
        cnt_by_ab[ (a,b) ] = cnt_by_ab.get( (a,b), 0 ) + val;

        cnt_by_a[ a ] = cnt_by_a.get( a, 0 ) + val;
        cnt_by_b[ b ] = cnt_by_b.get( b, 0 ) + val;

        total += val;

    assert total == self._rowcount;

    return self._stats( cnt_by_a, cnt_by_b, cnt_by_ab );


  def _finalize( self ):

    assert Frontend._finalize( self ) is None;

    if False:
      print( "unique combinations = ", self._kdb.count() );

    keyfmt = '>IIIII';
    valfmt = '>Q';

    c = self._kdb.cursor();
    c.jump();

    gt2 = 0;
    gt4 = 0;
    gt8 = 0;
    gt16 = 0;
    gt32 = 0;

    while True:

      r = c.get( True );
      if not r:
        break;

      self._ldb.put( r[0], r[1] );

      key = unpack( keyfmt, r[0] );
      val = unpack( valfmt, r[1] )[ 0 ];

      if val > 2:
        gt2 += 1;
      if val > 4:
        gt4 += 1;
      if val > 8:
        gt8 += 1;
      if val > 16:
        gt16 += 1;
      if val > 32:
        gt32 += 1;

    if False:
      print( gt2, gt4, gt8, gt16, gt32 );

    self._ic = {};
    for i in range( 0, self._lenrow ):
      self._ic[ i ] = self._get_info_content_by_dimension( i );

    self._icbp = {};

    for i in range( 0, self._lenrow ):
      for j in range( 0, self._lenrow ):

        if i >= j:
          continue;

        self._icbp[ (i,j) ] = self._get_info_content_by_pair( i, j );


    self._state \
      = { "ic": self._ic,
          "icbp": self._icbp,
          "c": self._len_c,
          "b": self._len_b,
          "x": self._len_x };


  def _fmt_dim( self, d_ ):

    d = None;
    if d_ < self._len_c:
      d = "c" + str( d_ );
    elif d_ < self._len_c + self._len_b:
      d = "b" + str( d_ - self._len_c );
    elif d_ < self._len_c + self._len_b + self._len_x:
      d = "x" + str( d_ - self._len_c - self._len_b );
    else:
      assert False;
    return "{:d}({:s})".format( d_, d );


  def _init( self ):

    self._needs_initialization = False;

    if False:

      for i in sorted( self._ic ):

        (corr,h_a,h_b,h_ab,mi) = self._ic[ i ];

        print(
            "{:s} {:1.4f} {:1.4f} {:1.4f} {:1.4f} {:1.4f}"\
             .format(
                  self._fmt_dim( i ),
                  corr,
                  h_a,
                  h_b,
                  h_ab,
                  mi
                )
          );

      for (i,j) in sorted( self._icbp ):

        (corr,h_a,h_b,h_ab,mi) = self._icbp[ (i,j) ];

        print(
            "{:s} {:s} {:1.4f} {:1.4f} {:1.4f} {:1.4f} {:1.4f}"\
             .format(
                  self._fmt_dim( i ),
                  self._fmt_dim( j ),
                  corr,
                  h_a,
                  h_b,
                  h_ab,
                  mi
                )
          );

    entropy \
      = [ ( h_ab, i ) \
          for ( i, (corr,h_a,h_b,h_ab,mi) ) in self._ic.items() ];          

    output_correlation \
      = [ ( corr, i ) \
          for ( i, (corr,h_a,h_b,h_ab,mi) ) in self._ic.items() ];

    self._core_dims = set();

    self._core_dims \
      |= { i \
           for ( h_ab, i ) \
           in sorted( entropy, reverse=True )[ :5 ] };

    self._core_dims \
      |= { i \
           for ( h_ab, i ) \
           in sorted( output_correlation, reverse=True )[ :3 ] };

    if False:
      print(
          "core = ",
          " ".join([ self._fmt_dim(d) for d in self._core_dims ])
        );

    self._satellite_dims = set();

    for core_dim in self._core_dims:

      satellite_dim = None;
      satellite_dim_c = None;
      satellite_dim_stats = None;

      for ( (i,j), (corr,h_a,h_b,h_ab,mi) ) in self._icbp.items():

        if corr <= 0.5:
          continue;

        other_dim = None;
        if i == core_dim:
          other_dim = j;
        elif j == core_dim:
          other_dim = i;
        else:
          continue;

        if ( satellite_dim_c is None ) or ( corr > satellite_dim_c ):

          satellite_dim = other_dim;
          satellite_dim_c = corr;
          satellite_dim_stats = (corr,h_a,h_b,h_ab,mi);

      if satellite_dim is not None:

        self._satellite_dims.add( satellite_dim );      

        if False:

          print(
              '->',
              self._fmt_dim(core_dim),
              self._fmt_dim(satellite_dim)
            );

          print(
              "{:1.4f} {:1.4f} {:1.4f} {:1.4f} {:1.4f}"\
               .format( *(corr,h_a,h_b,h_ab,mi) )
            );

    if False:

      print(
          "satellite = ",
          " ".join([ self._fmt_dim(d) for d in self._satellite_dims ])
        );

    self._removed_dims = set();
    for i in self._ic:
      if i not in self._core_dims and i not in self._satellite_dims:
        self._removed_dims.add( i );

    if False:

      print(
          "removed = ",
          " ".join([ self._fmt_dim(d) for d in self._removed_dims ])
        );

    for d_ in self._removed_dims:
      if d_ < self._len_c:
        self._remove_c.add( d_ );
      elif d_ < self._len_c + self._len_b:
        self._remove_b.add( d_ - self._len_c );
      elif d_ < self._len_c + self._len_b + self._len_x:
        self._remove_x.add( d_ - self._len_c - self._len_b );
      else:
        assert False;


  def apply_c( self, c ):

    if self.bypass_c:
      return c;

    if self._needs_initialization:
      self._init();

    c_ = [];
    for ( i, cval ) in enumerate( c ):
      if not i in self._remove_c:
        c_.append( cval );
    return c_;


  def apply_b( self, b ):

    if self.bypass_b:
      return b;

    if self._needs_initialization:
      self._init();

    b_ = [];
    for ( i, bval ) in enumerate( b ):
      if not i in self._remove_b:
        b_.append( bval );
    return b_;


  def apply_x( self, x ):

    if self.bypass_x:
      return x;

    if self._needs_initialization:
      self._init();

    x_ = [];
    for ( i, xval ) in enumerate( x ):
      if not i in self._remove_x:
        x_.append( xval );
    return x_;


  def __call__( self, row ):

    if self._needs_initialization:
      self._init();

    ( y, c, b, x ) = row;

    y_ = y;

    return \
      ( y_,
        self.apply_c( c ),
        self.apply_b( b ),
        self.apply_x( x ) );
