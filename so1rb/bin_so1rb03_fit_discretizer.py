from os.path import isfile;
from pickle import load as pickle_load;
from pickle import dump as pickle_dump;

from so1rb import cfg;

from so1rb.so1rb_data.da_read import da_read;
from so1rb.so1rb_frontend.fe_discretizer import FeatureDiscretizer;


def step03():

  assert isfile( cfg.dtadir+"/train_trn_.tsv.gz" );

  with open( cfg.dtadir+"/bfe.pickle", "rb" ) as f:
    bfe_ = pickle_load( f );

  with open( cfg.dtadir+"/cfe.pickle", "rb" ) as f:
    cfe_ = pickle_load( f );

  with open( cfg.dtadir+"/hbcfe.pickle", "rb" ) as f:
    hbcfe_ = pickle_load( f );

  with open( cfg.dtadir+"/kpcacfe.pickle", "rb" ) as f:
    kpcacfe_ = pickle_load( f );

  with FeatureDiscretizer() as fdp:
    with FeatureDiscretizer() as fdq:
      with bfe_ as bfe:
        with cfe_ as cfe:
          with hbcfe_ as hbcfe:
            with kpcacfe_ as kpcacfe:

              rows = da_read( cfg.dtadir+"/train_trn_.tsv.gz" );

              i = 0;

              for ( id_, y, c, b, x ) in rows:

                i += 1;
                # print( i );
                
                c = cfe( c );
                b = bfe( b );
                xp = hbcfe( x );
                xq = kpcacfe( x );

                is_enough = [];
                is_enough.append( fdp.train( xp ) );
                is_enough.append( fdq.train( xq ) );

                if all( is_enough ):
                  break;

              fdp.finalize();
              fdq.finalize();

              with open( cfg.dtadir+"/fdp.pickle", "wb" ) as f:
                pickle_dump( fdp, f );

              with open( cfg.dtadir+"/fdq.pickle", "wb" ) as f:
                pickle_dump( fdq, f );



def main():

  step03();



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
