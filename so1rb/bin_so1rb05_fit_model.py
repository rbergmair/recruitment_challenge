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

from so1rb.so1rb_model.mdl_bknn import BKNNModel;



def step05():

  assert isfile( cfg.dtadir+"/train_trn_.tsv.gz" );

  with FeatureSelector( cfg.dtadir+"/fs.pickle", "r" ) as fs:
    with FeatureDiscretizer( cfg.dtadir+"/fdp.pickle", "r" ) as fdp:
      with FeatureDiscretizer( cfg.dtadir+"/fdq.pickle", "r" ) as fdq:
        with KPCAContinuousFrontend( cfg.dtadir+"/kpcacfe.pickle", "r" ) as kpcacfe:
          with HomebrewContinuousFrontend( cfg.dtadir+"/hbcfe.pickle", "r" ) as hbcfe:
            with CategoricalFrontend( cfg.dtadir+"/cfe.pickle", "r" ) as cfe:
              with BinaryFrontend( cfg.dtadir+"/bfe.pickle", "r" ) as bfe:

                mdl_ \
                  = BKNNModel(
                        cfg.dtadir+"/mdlp.kch", "w",
                        cfe, bfe, hbcfe, fdp, fs
                      );

                with mdl_ as mdl:

                  rows = da_read( cfg.dtadir+"/train_trn_.tsv.gz" );

                  i = 0;

                  for ( id_, y, c, b, x ) in rows:

                    i += 1;
                    # print( i );
                    # if i > 1000:
                    #   break;

                    if mdl.train( ( y, c, b, x ) ):
                      break;



def main():

  step05();



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
