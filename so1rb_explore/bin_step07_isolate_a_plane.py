from gzip import open as gzip_open;

from pickle import load as pickle_load;
from pickle import dump as pickle_dump;


BINARY_FEATs \
  = [ 9, 11, 14, 15, 22, 23, 25, 37, 39, 41, 44, 45, 46, 48, 49, 51, 55, 58,
      60, 64, 69, 70, 72, 73, 78, 83, 87, 89, 95, 99 ];



def step07( datadir ):

  data = [];
  binplane_data = [];
  catplane_data = [];
  all_data = [];

  with gzip_open( datadir+"/train_trn.tsv.gz", "rt" ) as f:

    pass;

    firstline = f.readline();
    if firstline and firstline[-1] == '\n':
      firstline = firstline[:-1];
    firstline = firstline.split( '\t' );

    assert \
         firstline \
      == (   [ '"id"', '"y"', '"cId"' ]
           + [ '"x{}"'.format(i) for i in range(1,101) ] );

    for line in f:

      if line and line[-1] == '\n':
        line = line[:-1];
      line = line.split( '\t' );

      id_ = line[0];
      y = line[1];
      cid = line[2];

      assert cid[0] == '"';
      assert cid[-1] == '"';
      cid = int( cid[1:-1] );

      x = [ None ];
      b = [];

      for i in range( 3, len(line) ):
        if (i-2) in BINARY_FEATs:
          b.append( line[i] );
        else:
          x.append( float(line[i]) );

      b_ = 0;
      for i in range( 0, len(b) ):
        if b[i] == '0':
          b_i = 0;
        elif b[i] == '1':
          b_i = 1;
        else:
          assert False;
        b_ |= b_i << i;

      cid_ = hex(cid);
      b_ = hex(b_);

      all_data.append( (y,x) );
      if ( cid_ == '0xe' ) and ( b_ == '0x3fffffff' ):
        data.append( (y,x) );
      if ( cid_ == '0xe' ):
        catplane_data.append( (y,x) );
      if ( b_ == '0x3fffffff' ):
        binplane_data.append( (y,x) );

  with open( datadir+'/step07_all_data.pickle', 'wb' ) as f:
    pickle_dump( all_data, f );

  with open( datadir+'/step07_binplane_data.pickle', 'wb' ) as f:
    pickle_dump( binplane_data, f );

  with open( datadir+'/step07_catplane_data.pickle', 'wb' ) as f:
    pickle_dump( catplane_data, f );

  with open( datadir+'/step07_data.pickle', 'wb' ) as f:
    pickle_dump( data, f );



def main( datadir ):

  step07( datadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
