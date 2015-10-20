import sys;
from importlib import import_module;
import so1rb.cfg;


def main( cmd, *argv ):

  cmd = cmd.split("/")[-1];
  if cmd == "__main__.py" or cmd.endswith( ".zip" ):
    cmd = argv[0];
    so1rb.cfg.dtadir = argv[1];
    argv = argv[2:];

  import_module( "bin_"+cmd ).main( *argv );


if __name__ == "__main__":

  main( *sys.argv );
