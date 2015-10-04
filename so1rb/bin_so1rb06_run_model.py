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



def step06():

  with open( cfg.dtadir+"/results_train_dev.tsv", "wt" ) as outf:

    outf.write( '"id"\t"y"\t"score"\n' );

    with FeatureSelector( cfg.dtadir+"/fs.pickle", "r" ) as fs:
      with FeatureDiscretizer( cfg.dtadir+"/fdp.pickle", "r" ) as fdp:
        with FeatureDiscretizer( cfg.dtadir+"/fdq.pickle", "r" ) as fdq:
          with KPCAContinuousFrontend( cfg.dtadir+"/kpcacfe.pickle", "r" ) as kpcacfe:
            with HomebrewContinuousFrontend( cfg.dtadir+"/hbcfe.pickle", "r" ) as hbcfe:
              with CategoricalFrontend( cfg.dtadir+"/cfe.pickle", "r" ) as cfe:
                with BinaryFrontend( cfg.dtadir+"/bfe.pickle", "r" ) as bfe:

                  mdl_ \
                    = BKNNModel(
                          cfg.dtadir+"/mdlp.kch", "r",
                          cfe, bfe, hbcfe, fdp, fs
                        );

                  with mdl_ as mdl:

                    rows = da_read( cfg.dtadir+"/train_dev.tsv.gz" );

                    i = 0;

                    for ( id_, y, c, b, x ) in rows:

                      i += 1;
                      if i >= 10000:
                        break;

                      score = mdl( ( c, b, x ) );

                      print(
                          "{:d}".format(id_),
                          "{:d}".format(y),
                          "{:1.3f}".format(score),
                          sep = '\t',
                          file = outf
                        );



def main():

  step06();



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
