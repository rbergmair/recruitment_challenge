from os.path import isfile;
from pickle import load as pickle_load;
from pickle import dump as pickle_dump;


from so1rb import cfg;

from so1rb.so1rb_data.da_read import da_read;

from so1rb.so1rb_frontend.fe_binary import BinaryFrontend;
from so1rb.so1rb_frontend.fe_categorical import CategoricalFrontend;
from so1rb.so1rb_frontend.fe_continuous_homebrew import HomebrewContinuousFrontend;
from so1rb.so1rb_frontend.fe_continuous_kpca import KPCAContinuousFrontend;

from so1rb.so1rb_frontend.fe_discretizer import FeatureDiscretizer;

from so1rb.so1rb_frontend.fe_fselector import FeatureSelector;



def step04():

  assert isfile( cfg.dtadir+"/train_trn_.tsv.gz" );

  with FeatureSelector( cfg.dtadir+"/fs.pickle", "w" ) as fs:
    with FeatureDiscretizer( cfg.dtadir+"/fdp.pickle", "r" ) as fdp:
      with HomebrewContinuousFrontend( cfg.dtadir+"/hbcfe.pickle", "r" ) as hbcfe:
        with CategoricalFrontend( cfg.dtadir+"/cfe.pickle", "r" ) as cfe:
          with BinaryFrontend( cfg.dtadir+"/bfe.pickle", "r" ) as bfe:

            rows = da_read( cfg.dtadir+"/train_trn_.tsv.gz" );

            i = 0;

            for ( id_, y, c, b, x ) in rows:

              i += 1;
              #print( i );
              #if i > 10000:
              #  break;
              
              c = cfe( c );
              b = bfe( b );
              x = hbcfe( x );
              x_ = fdp( x );

              if fs.train( ( y, c, b, x_ ) ):
                break;



def main():

  step04();



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
