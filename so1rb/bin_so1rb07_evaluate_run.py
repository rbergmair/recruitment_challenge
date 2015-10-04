from pprint import pprint;

from so1rb import cfg;



def ntiles():

  scores = [];

  with open( cfg.dtadir+"/results_train_trn_.tsv", "rt" ) as f:

    f.readline();

    for (i,line) in enumerate(f):

      if i >= 10000:
        break;

      if line and line[-1] == '\n':
        line = line[:-1];

      ( id_, y, score ) = line.split( '\t' );
      y = int(y);
      score = float(score);

      scores.append( score );
  
  scores.sort();

  rslt = [];
  for idx in range(0,100):
    ratio = float(idx) / 100.0;
    rslt.append( scores[ int( float( len(scores) ) * ratio ) ] );

  return rslt;



def step07():

  ntiles_ = ntiles();

  stats_by_co = [];
  for co_idx in range( 0, len(ntiles_) ):
    stats_by_co.append( { "tp": 0, "fp": 0, "tn": 0, "fn": 0 } );

  true_positives = 0;
  false_positives = 0;
  true_negatives = 0;
  false_negatives = 0;

  with open( cfg.dtadir+"/results_train_dev.tsv", "rt" ) as f:

    f.readline();

    for line in f:

      if line and line[-1] == '\n':
        line = line[:-1];

      ( id_, y, score ) = line.split( '\t' );

      y = int(y);
      score = float(score);

      for co_idx in range( 0, len(ntiles_) ):

        co = ntiles_[ co_idx ];

        if score >= co:
          if y == 1:
            stats_by_co[ co_idx ][ "tp" ] += 1;
          else:
            assert y == 0;
            stats_by_co[ co_idx ][ "fp" ] += 1;
        else:
          if y == 0:
            stats_by_co[ co_idx ][ "tn" ] += 1;
          else:
            assert y == 1;
            stats_by_co[ co_idx ][ "fn" ] += 1;

  for co_idx in range( 0, len(ntiles_)-1 ):

    co = ntiles_[ co_idx ];

    if False:
      print( "\n-->", co_idx );

    tp = stats_by_co[ co_idx ][ "tp" ];
    fp = stats_by_co[ co_idx ][ "fp" ];
    tn = stats_by_co[ co_idx ][ "tn" ];
    fn = stats_by_co[ co_idx ][ "fn" ];

    precision = float(tp) / float(tp+fp);
    recall = float(tp) / float(tp+fn);
    fscore = 2.0 * ( ( precision * recall ) / ( precision + recall ) );

    print(
        "{:3d}".format( co_idx ),
        "{:+1.4f}".format( co ),
        "{:1.4f}".format( fscore ),
        "{:1.4f}".format( precision ),
        "{:1.4f}".format( recall ),
        "{:d}".format( tp ),
        "{:d}".format( fp ),
        "{:d}".format( tn ),
        "{:d}".format( fn ),
        sep = ';'
      );

    if False:

      print( "fscore = {:1.4f}".format(fscore) );

      print( "precision = {:1.4f}".format(precision) );
      print( "recall = {:1.4f}".format(recall) );

      print( "true_positives = {:d}".format( tp ) );
      print( "false_positives = {:d}".format( fp ) );
      print( "true_negatives = {:d}".format( tn ) );
      print( "false_negatives = {:d}".format( fn ) );



def main():

  step07();



if __name__ == "__main__":

  import sys;
  main( *sys.argv );
