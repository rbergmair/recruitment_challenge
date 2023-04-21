from os.path import isfile;
from pickle import dump as pickle_dump;

from so1rb import cfg;

from so1rb.so1rb_data.da_read import da_read;

from so1rb.so1rb_frontend.fe_binary import BinaryFrontend;
from so1rb.so1rb_frontend.fe_categorical import CategoricalFrontend;
from so1rb.so1rb_frontend.fe_continuous_homebrew import HomebrewContinuousFrontend;
from so1rb.so1rb_frontend.fe_continuous_kpca import KPCAContinuousFrontend;



def step02():

  assert isfile( cfg.dtadir+"/train_trn_.tsv.gz" );

  with KPCAContinuousFrontend( cfg.dtadir+"/kpcacfe.pickle", "w" ) as kpcacfe:
    with HomebrewContinuousFrontend( cfg.dtadir+"/hbcfe.pickle", "w" ) as hbcfe:
      with CategoricalFrontend( cfg.dtadir+"/cfe.pickle", "w" ) as cfe:
        with BinaryFrontend( cfg.dtadir+"/bfe.pickle", "w" ) as bfe:

          rows = da_read( cfg.dtadir+"/train_trn_.tsv.gz" );

          i = 0;

          for ( id_, y, c, b, x ) in rows:

            i += 1;
            # print( i );
            # if i >= 100:
            #   break;

            is_enough = [];
            is_enough.append( bfe.train( b ) );
            is_enough.append( cfe.train( [c] ) );
            is_enough.append( hbcfe.train( x ) );
            is_enough.append( kpcacfe.train( x ) );

            if all( is_enough ):
              break;



def main():

  step02();



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
