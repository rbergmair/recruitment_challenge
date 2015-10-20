from pickle import load as pickle_load;
from pickle import dump as pickle_dump;
from struct import pack, unpack, calcsize;
from os import remove;
from os.path import isfile;
from itertools import product;
from math import log;
from pprint import pprint;


import numpy as np;
from numpy import linalg as LA;

from kyotocabinet import DB;


from so1rb.so1rb_model.mdl import Model;



SMOOTHING = 0.33;



class BKNNModel( Model ):


  def __init__( self, fn, mode, catfe, binfe, contfe, fdisc, fsel, kval ):

    Model.__init__( self, fn, mode, catfe, binfe, contfe, fdisc, fsel );

    self._kval = kval;

    self._fn_cdata = self._fn;
    self._fn_ddata = self._fn.replace( '.kch', '-discrete.kch' );
    self._fn_meta = self._fn.replace( '.kch', '-meta.pickle' );
    self._fn_icov = self._fn.replace( '.kch', '-icov.pickle' );

    self._cdata = None;
    self._ddata = None;

    self._len_c = None;
    self._len_b = None;
    self._len_x = None;

    self._rowcount = None;
    self._total_pos = None;
    self._total_neg = None;

    self._icov = None;
    self._co = None;

    self._sample_y = [];
    self._sample_c = [];
    self._sample_b = [];
    self._sample_x = [];
    self._sample_x_ = [];

    self._needs_finalization = False;
    self._needs_initialization = True;

    self._dmarginals = {};
    self._dscores = {};

    self._sparse_points = 0;

    self._bias = None;


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

      with open( self._fn_meta, 'rb' ) as f:
        r = pickle_load( f );
        self._len_c = r[ "c" ];
        self._len_b = r[ "b" ];
        self._len_x = r[ "x" ];
        self._co = r[ "co" ];

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

      with open( self._fn_meta, 'wb' ) as f:

        r = { "c": self._len_c,
              "b": self._len_b,
              "x": self._len_x,
              "co": self._co };

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

      if isfile( self._fn_meta ):
        remove( self._fn_meta );

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

    if self._len_c is None:
      self._len_c = len(c);
    assert self._len_c == len(c);

    if self._len_b is None:
      self._len_b = len(b);
    assert self._len_b == len(b);

    if self._len_x is None:
      self._len_x = len(x);
    assert self._len_x == len(x);

    if self._rowcount is None:
      self._rowcount = 0;

    self._rowcount += 1;

    dkeyfmt = '>' + ( 'I' * ( 1 + self._len_c + self._len_b ) );
    self._ddata.increment( pack( dkeyfmt, y, *(c+b) ), 1, 0 );

    ckeyfmt = '>' + ( 'I' * len(x) );
    cvalfmt = '>I' + ( 'f' * len(x) );
    self._cdata.append( pack( ckeyfmt, *x_ ), pack( cvalfmt, y, *x ) );

    if len( self._sample_x ) < 50000:

      assert len( self._sample_x ) == len( self._sample_y );
      assert len( self._sample_x ) == len( self._sample_c );
      assert len( self._sample_x ) == len( self._sample_b );
      assert len( self._sample_x ) == len( self._sample_x_ );

      self._sample_y.append( y );
      self._sample_c.append( c );
      self._sample_b.append( b );
      self._sample_x.append( x );
      self._sample_x_.append( x_ );

    return False;


  def _init( self ):

    self._needs_initialization = False;

    c = self._ddata.cursor();
    c.jump();

    keyfmt = '>' + ( 'I' * ( 1 + self._len_c + self._len_b ) );
    valfmt = '>Q';


    while True:

      r = c.get( True );
      if not r:
        break;

      dbkey = unpack( keyfmt, r[0] );
      dbval = unpack( valfmt, r[1] )[ 0 ];

      additional_count = dbval;

      y = dbkey[ 0 ];

      for ( i, value_of_variable_i ) in enumerate( dbkey[ 1: ] ):

        if not i in self._dmarginals:
          self._dmarginals[ i ] = {};

        self._dmarginals[ i ][ (y,value_of_variable_i) ] \
          = self._dmarginals[ i ].get( (y,value_of_variable_i), 0 ) \
              + additional_count;


    for ( i, count_by_val ) in self._dmarginals.items():

      total = 0;
      total_neg = 0;
      total_pos = 0;

      for ( ( y, val ), cnt ) in count_by_val.items():
        total += cnt;
        if y == 0:
          total_neg += cnt;
        elif y == 1:
          total_pos += cnt;

      if self._rowcount is None:
        self._rowcount = total;
      assert self._rowcount == total;

      if self._total_neg is None:
        self._total_neg = total_neg;
      try:
        assert self._total_neg == total_neg;
      except: 
        print( self._total_neg, total_neg );
        raise;

      if self._total_pos is None:
        self._total_pos = total_pos;
      try:
        assert self._total_pos == total_pos;
      except: 
        print( self._total_pos, total_pos );
        raise;

    assert ( self._total_pos + self._total_neg ) == self._rowcount;


    for i in self._dmarginals:

      values = set([ val for (y,val) in self._dmarginals[ i ].keys() ]);

      if i not in self._dscores:
        self._dscores[ i ] = {};

      for val in values:

        pos_cnt = self._dmarginals[ i ].get( (1,val), 0 );
        neg_cnt = self._dmarginals[ i ].get( (0,val), 0 );

        p_pos \
          =   log( float(pos_cnt) + SMOOTHING, 2.0 ) \
            - log( float(self._total_pos) + float( len(values) ) * SMOOTHING, 2.0 );

        p_neg \
          =   log( float(neg_cnt) + SMOOTHING, 2.0 ) \
            - log( float(self._total_neg) + float( len(values) ) * SMOOTHING, 2.0 );

        self._dscores[ i ][ val ] = p_pos - p_neg;

    
    p_pos \
      =   log( float(self._total_pos), 2.0 ) \
        - log( float(self._rowcount), 2.0 );

    p_neg \
      =   log( float(self._total_neg), 2.0 ) \
        - log( float(self._rowcount), 2.0 );

    self._bias = p_pos - p_neg;


    if False:
      for i in sorted( self._dscores.keys() ):
        score_by_val = self._dscores[ i ];
        for ( val, score ) in score_by_val.items():
          print( "{:d} {:10d} {:+2.4f}".format( i, val, score ) );


  def _apply( self, row ):

    if self._needs_initialization:
      self._init();

    ( c, b, x, x_ ) = row;

    ckeyfmt = '>' + ( 'I' * len(x_) );
    cvalfmt = '>I' + ( 'f' * len(x) );
    cvalsz = calcsize( cvalfmt );

    rng = [];
    for xval in x_:
      rng.append(
          [ xv \
              for xv \
               in [ xval-2, xval-1, xval, xval+1, xval+2 ] \
               if 0 <= xv <= 31 ]
        );

    x_vec = np.array( x ).reshape( 1, self._len_x ).T;

    nearest_positive = [];
    all_negative = [];
    found_ident = 0;

    for xvals in product( *rng ):

      try:
        ckey = pack( ckeyfmt, *xvals );
      except:
        print( ckeyfmt, xvals );
        raise;
      val = self._cdata.get( ckey );

      while val:

        if len(val) <= cvalsz:
          assert len(val) == cvalsz;

        val_ = val[:cvalsz];
        val = val[cvalsz:];

        pt = unpack( cvalfmt, val_ );
        pt_y = pt[0];
        pt_x = pt[1:];

        pt_x_vec = np.array( pt_x ).reshape( 1, self._len_x ).T;
        diff = pt_x_vec - x_vec;
        dist = np.sqrt( np.dot( np.dot( diff.T, self._icov ), diff ) );

        if dist <= 0.0001:
          found_ident += 1;
          continue;

        if pt_y == 0:
          all_negative.append( dist );
          continue;

        assert pt_y == 1;

        nearest_positive.append( dist );
        nearest_positive.sort();
        nearest_positive = nearest_positive[:self._kval];

    # assert found_ident == 1;
    # assert len( nearest_positive ) == self._kval;
    if len( nearest_positive ) < self._kval:
      self._sparse_points += 1;

    score = self._bias;

    # if len( nearest_positive ) > 0:
    if True:

      if len( nearest_positive ) == 0:
        threshold = None;
      else:
        threshold = nearest_positive[-1];

      neg_cnt = 0;
      for dist in all_negative:
        if ( threshold is None ) or ( dist <= threshold ):
          neg_cnt += 1;

      p_pos \
        =   log( float( len(nearest_positive) ) + SMOOTHING, 2.0 ) \
          - log( float(self._total_pos) + 2.0 * SMOOTHING, 2.0 );

      p_neg \
        =   log( float(neg_cnt) + SMOOTHING, 2.0 ) \
          - log( float(self._total_neg) + 2.0 * SMOOTHING, 2.0 );

      score += p_pos - p_neg;

    for ( i, dval ) in enumerate( c+b ):
      score += self._dscores[ i ].get( dval, 0.0 );

    if self._co is None:
      return score;
    else:
      if score >= self._co:
        return 1;
      else:
        return 0;


  def _finalize( self ):

    self._needs_finalization = False;

    covsample = np.array( self._sample_x );
    cov = np.cov( covsample.T );
    self._icov = LA.inv( cov );

    sample \
      = zip(
            self._sample_c,
            self._sample_b,
            self._sample_x,
            self._sample_x_
          );

    scores = [];
    for ( c, b, x, x_ ) in sample:
      scores.append( self._apply( [ c, b, x, x_ ] ) );

    sorted_scores = list( sorted( scores ) );

    cutoffs = [];
    for idx in range(0,1000):
      ratio = float(idx) / 1000.0;
      cutoffs.append(
          sorted_scores[ int( float( len(sorted_scores) ) * ratio ) ]
        );

    if False:
      pprint( cutoffs );

    stats_by_co = [];
    for coidx in range( 0, len(cutoffs) ):
      stats_by_co.append( { "tp": 0, "fp": 0, "tn": 0, "fn": 0 } );

    for ( y, score ) in zip( self._sample_y, scores ):
      for ( coidx, co ) in enumerate( cutoffs ):
        if score >= co:
          if y == 1:
            stats_by_co[ coidx ][ "tp" ] += 1;
          else:
            assert y == 0;
            stats_by_co[ coidx ][ "fp" ] += 1;
        else:
          if y == 0:
            stats_by_co[ coidx ][ "tn" ] += 1;
          else:
            assert y == 1;
            stats_by_co[ coidx ][ "fn" ] += 1;

    max_fscore = None;
    max_fscore_coidx = None;
    
    for ( coidx, co ) in enumerate( cutoffs ):

      tp = stats_by_co[ coidx ][ "tp" ];
      fp = stats_by_co[ coidx ][ "fp" ];
      tn = stats_by_co[ coidx ][ "tn" ];
      fn = stats_by_co[ coidx ][ "fn" ];

      if (tp+fp) <= 0:
        continue;

      if (tp+fn) <= 0:
        continue;

      precision = float(tp) / float(tp+fp);
      recall = float(tp) / float(tp+fn);

      if (precision+recall) <= 0.0:
        continue;

      fscore = 2.0 * ( ( precision * recall ) / ( precision + recall ) );

      if ( max_fscore is None ) or ( fscore > max_fscore ):

        max_fscore = fscore;
        max_fscore_coidx = coidx;

    assert max_fscore_coidx is not None;
    self._co = cutoffs[ max_fscore_coidx ];

    # assert self._sparse_points == 0;

    if True:
      print( self._sparse_points );
      print( self._co );
      print( max_fscore );


  def __call__( self, row ):

    ( c, b, x ) = row;

    c = self._fsel.apply_c( self._catfe( c ) );
    b = self._fsel.apply_b( self._binfe( b ) );

    x = self._contfe( x );
    x_ = self._fdisc( x );

    x = self._fsel.apply_x( x );
    x_ = self._fsel.apply_x( x_ );

    try:
      assert self._len_c == len(c);
      assert self._len_b == len(b);
      assert self._len_x == len(x);
      assert self._len_x == len(x_);
    except:
      print( self._len_c, self._len_b, self._len_x );
      raise;

    return self._apply( ( c, b, x, x_ ) );
