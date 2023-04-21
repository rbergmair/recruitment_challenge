from math import log;

from so1rb.so1rb_frontend.fe import Frontend;



class BinaryFrontend( Frontend ):


  def __init__( self, fn, mode ):

    Frontend.__init__( self, fn, mode );
    self._max_rows = 100000;
    
    self._stats = {};


  def train( self, row ):

    if Frontend.train( self, row ):
      return True;

    b = 0;
    for i in range( 0, len(row) ):
      if row[i] == 1:
        b |= (1<<i);

    self._stats[ b ] = self._stats.get( b, 0 ) + 1;

    return False;


  def _i_corr( self, dims_a, dims_b ):

    mask_a = 0;  
    for i in dims_a:
      mask_a |= (1<<i);

    mask_b = 0;  
    for i in dims_b:
      mask_b |= (1<<i);

    cnt_by_a = {};
    cnt_by_b = {};
    cnt_by_ab = {};
    total = 0;

    for ( val, cnt ) in self._stats.items():

      val_a = val & mask_a;
      val_b = val & mask_b;

      total += cnt;
      cnt_by_a[ val_a ] = cnt_by_a.get( val_a, 0 ) + cnt;
      cnt_by_b[ val_b ] = cnt_by_b.get( val_b, 0 ) + cnt;
      cnt_by_ab[ (val_a,val_b) ] = cnt_by_ab.get( (val_a,val_b), 0 ) + cnt;

    h_a = 0.0;
    h_b = 0.0;
    h_ab = 0.0;

    for ( val_a, cnt ) in cnt_by_a.items():
      p = float(cnt) / float(total);
      if p > 0.0:      
        h_a -= p * log( p, 2.0 );

    for ( val_b, cnt ) in cnt_by_b.items():
      p = float(cnt) / float(total);
      if p > 0.0:      
        h_b -= p * log( p, 2.0 );

    for( (val_a,val_b), cnt ) in cnt_by_ab.items():
      p = float(cnt) / float(total);
      if p > 0.0:      
        h_ab -= p * log( p, 2.0 );

    if h_a == 0.0:
      return 1.0;

    if h_b == 0.0:
      return 1.0;
    
    mi = h_a + h_b - h_ab;
    return mi / min( h_a, h_b );


  def _split( self, dims ):

    if len( dims ) <= 2:
      dim1 = dims.pop();
      dim2 = dims.pop();
      return ( { dim1 }, { dim2 }, set() );

    first_dim = None;
    first_dim_c = None;
    
    for i in dims:

      a = { i };
      b = dims - a;
      c = self._i_corr( a, b );

      if ( first_dim_c is None ) or ( c < first_dim_c ):
        first_dim_c = c;
        first_dim = i;

    second_dim = None;
    second_dim_c = None;

    for i in dims - { first_dim }:

      a = { first_dim };
      b = { i };
      c = self._i_corr( a, b );

      if ( second_dim_c is None ) or ( c < second_dim_c ):
        second_dim_c = c;
        second_dim = i;

    left = { first_dim };
    right = { second_dim };
    rest = dims - { first_dim, second_dim };

    while True:

      removable = set();

      for i in rest:

        cl = self._i_corr( left, {i} );
        cr = self._i_corr( right, {i} );

        if ( cl == cr ):
          continue;

        if ( cr > cl ) and ( cr >= 0.5 ):
          removable.add( i );
          right.add( i );

        if ( cl > cr ) and ( cl >= 0.5 ):
          removable.add( i );
          left.add( i );

      rest -= removable;
      if not removable:
        break;

    return ( left, right, rest );


  def _finalize( self ):

    assert Frontend._finalize( self ) is None;

    self._state = [];
    rest = set( range( 0, self._lenrow ) );

    while rest:
      if len( rest ) >= 2:
        ( left, right, rest ) = self._split( rest );
        self._state.append( left );
        self._state.append( right );
      else:
        self._state.append( rest );
        rest = set();

    if False:

      for ( cluster_id, cluster ) in enumerate( self._state ):
        print( "-->", cluster_id, cluster );
        for i in cluster:
          a = { i };
          b = cluster - a;
          print( "    {:d} {:1.4f}".format( i, self._i_corr( a, b ) ) );


  def __call__( self, row ):

    assert Frontend.__call__( self, row ) is row;

    val = 0;
    for (i,row_i) in enumerate( row ):
      if row_i == 1:
        val |= (1<<i);

    row_ = [];

    for cluster in self._state:
      mask = 0;
      for dim in cluster:
        mask |= (1<<dim);
      row_.append( val & mask );

    return row_;
