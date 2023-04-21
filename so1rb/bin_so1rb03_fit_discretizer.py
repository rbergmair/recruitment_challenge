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


def step03():

  assert isfile( cfg.dtadir+"/train_trn_.tsv.gz" );

  with FeatureDiscretizer( cfg.dtadir+"/fdp.pickle", "w" ) as fdp:
    with FeatureDiscretizer( cfg.dtadir+"/fdq.pickle", "w" ) as fdq:
      with KPCAContinuousFrontend( cfg.dtadir+"/kpcacfe.pickle", "r" ) as kpcacfe:
        with HomebrewContinuousFrontend( cfg.dtadir+"/hbcfe.pickle", "r" ) as hbcfe:
          with CategoricalFrontend( cfg.dtadir+"/cfe.pickle", "r" ) as cfe:
            with BinaryFrontend( cfg.dtadir+"/bfe.pickle", "r" ) as bfe:

              rows = da_read( cfg.dtadir+"/train_trn_.tsv.gz" );

              i = 0;

              for ( id_, y, c, b, x ) in rows:

                i += 1;
                # print( i );
                # if i >= 100:
                #   break;
                
                c = cfe( c );
                b = bfe( b );
                xp = hbcfe( x );
                xq = kpcacfe( x );

                is_enough = [];
                is_enough.append( fdp.train( xp ) );
                is_enough.append( fdq.train( xq ) );

                if all( is_enough ):
                  break;



def main():

  step03();



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
