from pickle import dump as pickle_dump;

from so1rb import cfg;

from so1rb.so1rb_data.da_read import da_read;

from so1rb.so1rb_frontend.fe_binary import BinaryFrontend;
from so1rb.so1rb_frontend.fe_categorical import CategoricalFrontend;
from so1rb.so1rb_frontend.fe_continuous_homebrew import HomebrewContinuousFrontend;
from so1rb.so1rb_frontend.fe_continuous_kpca import KPCAContinuousFrontend;



def step02():

  assert isfile( cfg.dtadir+"/train_trn_.tsv.gz" );

  with KPCAContinuousFrontend() as kpcacfe:
    with HomebrewContinuousFrontend() as hbcfe:
      with CategoricalFrontend() as cfe:
        with BinaryFrontend() as bfe:

          for ( id_, y, c, b, x ) in da_read( cfg.dtadir+"/train_trn_.tsv.gz" ):

            is_enough = [];
            is_enough.append( bfe.train( b ) );
            is_enough.append( cfe.train( [c] ) );
            is_enough.append( hbcfe.train( x ) );
            is_enough.append( kpcacfe.train( x ) );
            if all( is_enough ):
              break;

          bfe.finalize();
          cfe.finalize();
          hbcfe.finalize();
          kpcacfe.finalize();

          with open( cfg.dtadir+"/bfe.pickle", "wb" ) as f:
            pickle_dump( bfe, f );

          with open( cfg.dtadir+"/cfe.pickle", "wb" ) as f:
            pickle_dump( cfe, f );

          with open( cfg.dtadir+"/hbcfe.pickle", "wb" ) as f:
            pickle_dump( hbcfe, f );

          with open( cfg.dtadir+"/kpcacfe.pickle", "wb" ) as f:
            pickle_dump( kpcacfe, f );



def main():

  step02();



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
