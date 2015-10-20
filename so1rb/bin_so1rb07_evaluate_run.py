from gzip import open as gzip_open;

from so1rb import cfg;



def step07( dataf, runf ):

  decision = {};

  with gzip_open( cfg.dtadir + "/" + dataf, "rt" ) as f:

    firstline = f.readline();

    if firstline and firstline[-1] == '\n':
      firstline = firstline[:-1];

    firstline = firstline.split( '\t' )[ :2 ];
    assert firstline == [ '"id"', '"y"' ];

    for line in f:

      if line and line[-1] == '\n':
        line = line[:-1];
      line = line.split( '\t' );

      ( id_, y ) = line[ :2 ];

      decision[ id_ ] = int(y);

  tp = 0;
  fp = 0;
  tn = 0;
  fn = 0;

  with gzip_open( cfg.dtadir + "/" + runf, "rt" ) as f:

    firstline = f.readline();

    if firstline and firstline[-1] == '\n':
      firstline = firstline[:-1];

    firstline = firstline.split( '\t' );

    assert firstline == [ '"id"', '"y"' ];

    for line in f:

      if line and line[-1] == '\n':
        line = line[:-1];
      line = line.split( '\t' );

      ( id_, y_mdl ) = line;

      y_mdl = int( y_mdl );

      y = decision[ id_ ];

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



def main( dataf, runf ):

  step07( dataf, runf );



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
