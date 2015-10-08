from gzip import open as gzip_open;

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



def step06( modelf, dataf ):

  tp = 0;
  fp = 0;
  tn = 0;
  fn = 0;

  modelf_ = modelf.replace( '.kch', '' );

  with gzip_open( cfg.dtadir + "/results_{}_{}".format( modelf_, dataf ), "wt" ) as outf:

    outf.write( '"id"\t"y"\n' );

    with FeatureSelector( cfg.dtadir+"/fs.pickle", "r" ) as fs:
      with FeatureDiscretizer( cfg.dtadir+"/fdp.pickle", "r" ) as fdp:
        with FeatureDiscretizer( cfg.dtadir+"/fdq.pickle", "r" ) as fdq:
          with KPCAContinuousFrontend( cfg.dtadir+"/kpcacfe.pickle", "r" ) as kpcacfe:
            with HomebrewContinuousFrontend( cfg.dtadir+"/hbcfe.pickle", "r" ) as hbcfe:
              with CategoricalFrontend( cfg.dtadir+"/cfe.pickle", "r" ) as cfe:
                with BinaryFrontend( cfg.dtadir+"/bfe.pickle", "r" ) as bfe:

                  if modelf == "mdlp.kch":

                    mdl_ \
                      = BKNNModel(
                            cfg.dtadir + "/" + modelf, "r",
                            cfe, bfe, hbcfe, fdp, fs, 7
                          );

                  elif modelf == "mdlq.kch":

                    fs.bypass_x = True;

                    mdl_ \
                      = BKNNModel(
                            cfg.dtadir+"/"+modelf, "r",
                            cfe, bfe, kpcacfe, fdq, fs, 7
                          );

                  with mdl_ as mdl:

                    rows = da_read( cfg.dtadir + "/" + dataf );

                    i = 0;

                    for ( id_, y, c, b, x ) in rows:

                      i += 1;
                      if i >= 50000:
                        break;

                      # print( y, c, b, x );

                      y_mdl = mdl( ( c, b, x ) );

                      print(
                          "{:d}".format(id_),
                          "{:d}".format(y_mdl),
                          sep = '\t',
                          file = outf
                        );

                      if y is None:
                        continue;

                      if y_mdl == 1:
                        if y == 1:
                          tp += 1;
                        else:
                          assert y == 0;
                          fp += 1;
                      else:
                        assert y_mdl == 0;
                        if y == 0:
                          tn += 1;
                        else:
                          fn += 1;


  precision = float(tp) / float(tp+fp);
  recall = float(tp) / float(tp+fn);
  fscore = 2.0 * ( ( precision * recall ) / ( precision + recall ) );

  print( "fscore = {:1.4f}".format(fscore) );

  print( "precision = {:1.4f}".format(precision) );
  print( "recall = {:1.4f}".format(recall) );

  print( "true_positives = {:d}".format( tp ) );
  print( "false_positives = {:d}".format( fp ) );
  print( "true_negatives = {:d}".format( tn ) );
  print( "false_negatives = {:d}".format( fn ) );



def main( modelf, dataf ):

  step06( modelf, dataf );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
