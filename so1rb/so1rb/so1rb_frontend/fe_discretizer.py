from tempfile import TemporaryDirectory;
from time import sleep;
from shutil import rmtree;
from pprint import pprint;

from struct import pack, unpack;

import plyvel;



class FeatureDiscretizer:


  def __init__( self ):

    self._rowcount = 0;
    self._dbs = {};
    self._dbdirs = [];
    self._ntile_bounds = None;


  def __getstate__( self ):

    return { "ntile_bounds": self._ntile_bounds };


  def __setstate__( self, state ):

    self.__init__();
    self._ntile_bounds = state[ "ntile_bounds" ];


  def __enter__( self ):
    
    return self;
  
  def __exit__( self, exc_type, exc_value, traceback ):

    sleep( 3.0 );

    for db in self._dbs.values():
      db.close();    
    for dn in self._dbdirs:
      rmtree( dn );


  def train( self, x ):

    if self._rowcount >= 50000:
      return True;

    for ( i, xval ) in enumerate( x ):

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

    self._rowcount += 1;
    if self._rowcount >= 50000:
      return True;

    return False;


  def finalize( self ):

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

    self._ntile_bounds = ntile_bound_by_dim;



  def __call__( self, row ):

    row_ = [];

    for ( dim, val ) in enumerate( row ):

      val \
        = int( float(val) * 1000.0 );

      boundaries = [ None ] + self._ntile_bounds[ dim ] + [ None ];

      for i in range( 0, len(boundaries)-1 ):

        lower = boundaries[ i ];
        upper = boundaries[ i+1 ];

        assert not ( lower is None and upper is None );

        if lower is None:
          assert upper is not None;
          if val <= upper:
            row_.append( i );
            continue;

        if upper is None:
          assert lower is not None;
          if lower < val:
            row_.append( i );
            continue;

        if ( lower is not None ) and ( upper is not None ):
          if lower < val <= upper:
            row_.append( i );
            continue;

    return row_;
