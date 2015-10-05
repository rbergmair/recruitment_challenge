from os.path import isfile;
from gzip import open as gzip_open;



BINARY_FEATs \
  = [ 9, 11, 14, 15, 22, 23, 25, 37, 39, 41, 44, 45, 46, 48, 49, 51, 55, 58,
      60, 64, 69, 70, 72, 73, 78, 83, 87, 89, 95, 99 ];



def da_read( fn ):

  assert isfile( fn );

  with gzip_open( fn, "rt" ) as f:

    firstline = f.readline();

    if firstline and firstline[-1] == '\n':
      firstline = firstline[:-1];
    firstline = firstline.split( '\t' );

    assert \
         firstline \
      == (   [ '"id"', '"y"', '"cId"' ]
           + [ '"x{}"'.format(i) for i in range(1,101) ] );

    x_check = {};

    for line in f:

      if line and line[-1] == '\n':
        line = line[:-1];
      line = line.split( '\t' );

      id_ = line[0];
      id_ = int( id_ );

      y = line[1];
      assert y in [ "0", "1" ];
      y = int( y );

      c = line[2];

      assert c[0] == '"';
      assert c[-1] == '"';
      c = int( c[1:-1] );

      b = [];
      x = [];

      for i in range( 3, len(line) ):

        try:

          val = line[i];

          if (i-2) in BINARY_FEATs:

            assert val in [ "0", "1" ];
            val = int(val)
            b.append( val );
            continue;

          if not '.' in val:
            val = val+'.';
          val = val.split( '.' );

          assert \
            ( ( val[0][0] == '-' ) and ( len(val[0]) == 2 ) ) \
                  or ( ( val[0][0] != '-' ) and ( len(val[0]) == 1 ) );
          assert \
            len( val[1] ) <= 3;

          while len( val[1] ) < 3:
            val[1] = val[1] + '0';

          assert \
            len( val[1] ) == 3;

          if val[0][0] == '-':
            val = - int( val[0][1:] ) * 1000 - int( val[1] );
          else:
            val = int( val[0] ) * 1000 + int( val[1] );          

          assert ( float(val) / 1000.0 ) == float(line[i]);

          x_check_ = x_check.get( i, set() );
          if len( x_check_ ) < 3:
            x_check_.add( val );
            x_check[ i ] = x_check_;

          x.append( val );

        except:

          print( repr(val), line[i] );
          raise;

      yield ( id_, y, [c], b, x );

    for v in x_check.values():
      assert len( v ) > 2;
