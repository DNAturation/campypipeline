import os
import subprocess
import argparse

#name of the folder that stuff gets saved to
PROJECTNAME = input(print("Please name the folder"))
SEQUENCES = input(print("Please specify the files to assemble"))

#command for kraken, write classified output files from specified input files
#KrakenCommand = "kraken --only-classified-output --classified-out ./{name}/Kraken/".format(name=PROJECTNAME)
KrakenCommand = "kraken --classified-out output {INPUTFILE}"/ format(INPUTFILE=SEQUENCES)
#command to specify path for kraken to write files to
PROJECTPATH = "export KRAKEN_DB_PATH='home/user/{name}/Kraken/'". format(name=PROJECTNAME)
#command to make path for kraken to write files to
KRAKENDIR = "mkdir ~/{name}/Kraken/". format(name=PROJECTNAME)

subprocess.call(KRAKENDIR)
subprocess.call(PROJECTPATH)
subprocess.call(KrakenCommand, stdin=None, stdout=None, stderr=subprocess.STDOUT, shell=True, timeout=None)



