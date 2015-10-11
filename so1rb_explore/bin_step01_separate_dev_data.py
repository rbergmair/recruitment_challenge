from os.path import isfile;
from random import random;
from os import urandom;
from gzip import open as gzip_open;
from shutil import rmtree;
from tempfile import TemporaryDirectory;
from time import sleep;

import plyvel;



def step01( dtadir ):

  if not isfile( dtadir+"/train_trn_.tsv.gz" ):

    assert isfile( dtadir+"/train.tsv.gz" );
    assert not isfile( dtadir+"/train_trn_.tsv.gz" );
    assert not isfile( dtadir+"/train_dev.tsv.gz" );

    with gzip_open( dtadir+"/train_trn_.tsv.gz", "wt" ) as trn:
      with gzip_open( dtadir+"/train_dev.tsv.gz", "wt" ) as dev:
        with gzip_open( dtadir+"/train.tsv.gz", "rt" ) as f:

          firstline = f.readline();

          trn.write( firstline );
          dev.write( firstline );

          if firstline and firstline[-1] == '\n':
            firstline = firstline[:-1];
          firstline = firstline.split( '\t' );

          assert \
               firstline \
            == (   [ '"id"', '"y"', '"cId"' ]
                 + [ '"x{}"'.format(i) for i in range(1,101) ] );

          for line in f:
            if random() < 0.15:
              dev.write( line );
            else:
              trn.write( line );

  if isfile( dtadir+"/train_trn.tsv.gz" ):
    return;

  dbdn = None;
  with TemporaryDirectory() as tmpdirname:
    dbdn = tmpdirname;

  with gzip_open( dtadir+"/train_trn.tsv.gz", "wt" ) as fout:
    with gzip_open( dtadir+"/train_trn_.tsv.gz", "rt" ) as fin:

      firstline = fin.readline();

      fout.write( firstline );

      if firstline and firstline[-1] == '\n':
        firstline = firstline[:-1];
      firstline = firstline.split( '\t' );

      assert \
           firstline \
        == (   [ '"id"', '"y"', '"cId"' ]
             + [ '"x{}"'.format(i) for i in range(1,101) ] );

      leveldb \
        = plyvel.DB(
              dbdn,
              create_if_missing=True
            );

      try:

        for line in fin:
          leveldb.put( urandom(4), line.encode('ascii') );

        with leveldb.iterator() as it:
          for ( id_, line ) in it:
            fout.write( line.decode('ascii') );

      finally:

        sleep( 3.0 );
        leveldb.close();
        rmtree( dbdn );



def main( dtadir ):

  step01( dtadir );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
