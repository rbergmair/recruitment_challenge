import sys;
from importlib import import_module;


def main( cmd, *argv ):

  cmd = cmd.split("/")[-1];
  if cmd == "__main__.py" or cmd.endswith( ".zip" ):
    cmd = argv[0];
    argv = argv[1:];

  import_module( "bin_"+cmd ).main( *argv );


if __name__ == "__main__":

  main( *sys.argv );
