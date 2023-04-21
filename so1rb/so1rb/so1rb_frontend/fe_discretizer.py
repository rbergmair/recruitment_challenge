from tempfile import TemporaryDirectory;
from time import sleep;
from shutil import rmtree;
from pprint import pprint;

from struct import pack, unpack;


import plyvel;


from so1rb.so1rb_frontend.fe import Frontend;



class FeatureDiscretizer( Frontend ):


  def __init__( self, fn, mode ):

    Frontend.__init__( self, fn, mode );
    self._max_rows = 50000;

    self._dbs = {};
    self._dbdirs = [];


  def __exit__( self, exc_type, exc_value, traceback ):

    assert Frontend.__exit__( self, exc_type, exc_value, traceback ) == False;

    sleep( 3.0 );

    for db in self._dbs.values():
      db.close();    
    for dn in self._dbdirs:
      rmtree( dn );

    return False;


  def train( self, row ):

    if Frontend.train( self, row ):
      return True;

    for ( i, xval ) in enumerate( row ):

      if not i in self._dbs:
        dbdn = None;
        with TemporaryDirectory() as tmpdirname:
          dbdn = tmpdirname;        
        self._dbdirs.append( dbdn );
        self._dbs[ i ] = plyvel.DB( dbdn, create_if_missing=True );

      xval \
        = int( float(xval) * 1000.0 );

      assert xval < (1<<30);

      xval \
        = pack( ">I", (1<<31) + xval );

      xcnt \
        = unpack(
              ">I",
              self._dbs[ i ].get( xval, default=pack( ">I", 0 ) )
            )[ 0 ];

      xcnt += 1;

      self._dbs[ i ].put( xval, pack( ">I", xcnt ) );

    return False;


  def _finalize( self ):

    assert Frontend._finalize( self ) is None;

    rowids_for_ntile_bounds = [];
    for i in range( 1, 32 ):
      rowids_for_ntile_bounds.append(
          int( float(self._rowcount) * float(i)/32.0 )
        );

    ntile_bound_by_dim = {};
    for i in self._dbs:
      ntile_bound_by_dim[ i ] = [];

    for ( i, db ) in self._dbs.items():

      with db.iterator() as it:

        rowid = 0;

        for ( valid, ( xval, xcnt ) ) in enumerate( it ):

          xval = unpack( '>I', xval )[ 0 ] - (1<<31);
          xcnt = unpack( '>I', xcnt )[ 0 ];

          rowid_old = rowid;
          rowid = rowid_old + xcnt;

          for bound in rowids_for_ntile_bounds:
            if rowid_old < bound <= rowid:
              ntile_bound_by_dim[ i ].append( xval );

    self._state = ntile_bound_by_dim;


  def __call__( self, row, fold=1 ):

    row_ = [];

    for ( dim, val ) in enumerate( row ):

      val \
        = int( float(val) * 1000.0 );

      boundaries = [ None ] + self._state[ dim ] + [ None ];

      for i in range( 0, len(boundaries)-1 ):

        lower = boundaries[ i ];
        upper = boundaries[ i+1 ];

        assert not ( lower is None and upper is None );

        if lower is None:
          assert upper is not None;
          if val <= upper:
            row_.append( i // fold );
            continue;

        if upper is None:
          assert lower is not None;
          if lower < val:
            row_.append( i // fold );
            continue;

        if ( lower is not None ) and ( upper is not None ):
          if lower < val <= upper:
            row_.append( i // fold );
            continue;

    return row_;
