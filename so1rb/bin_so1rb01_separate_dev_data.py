from os.path import isfile;
from random import random;
from os import urandom;
from gzip import open as gzip_open;
from shutil import rmtree;
from tempfile import TemporaryDirectory;
from time import sleep;

import plyvel;

import so1rb.cfg as cfg;



def step01():

  if not isfile( cfg.dtadir+"/train_trn_.tsv.gz" ):

    assert isfile( cfg.dtadir+"/train.tsv.gz" );
    assert not isfile( cfg.dtadir+"/train_trn_.tsv.gz" );
    assert not isfile( cfg.dtadir+"/train_dev.tsv.gz" );

    with gzip_open( cfg.dtadir+"/train_trn_.tsv.gz", "wt" ) as trn:
      with gzip_open( cfg.dtadir+"/train_dev.tsv.gz", "wt" ) as dev:
        with gzip_open( cfg.dtadir+"/train.tsv.gz", "rt" ) as f:

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

  if isfile( cfg.dtadir+"/train_trn.tsv.gz" ):
    return;

  dbdn = None;
  with TemporaryDirectory() as tmpdirname:
    dbdn = tmpdirname;

  with gzip_open( cfg.dtadir+"/train_trn.tsv.gz", "wt" ) as fout:
    with gzip_open( cfg.dtadir+"/train_trn_.tsv.gz", "rt" ) as fin:

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



def main():

  step01();



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
