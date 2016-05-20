import os
import subprocess
import argparse

#name of the folder that stuff gets saved to
#PROJECTNAME =
#SEQUENCES = input(print("Please specify the files to assemble"))

#command for kraken, write classified output files from specified input files
#KrakenCommand = "kraken --only-classified-output --classified-out ./{name}/Kraken/".format(name=PROJECTNAME)


def arguments():
    '''Takes args from the user and parses them'''
    parser = argparse.ArgumentParser
    parser.add_argument()
    return parser.parse_args()
    pass


#somehow need to stick version numbers run into each of these?
def run_kraken():
    '''Formats Kraken args and runs kraken'''
    KrakenCommand = "kraken --db DBNAME --classified-out OUTPUTNAME {INPUTFILE}".format(INPUTFILE=input())
    subprocess.call(KrakenCommand, stdin=None, stdout=None, stderr=None, shell=True, timeout=None)
    pass


def run_spades():
    FILENAME1 = "*1_001\.fastq"
    FILENAME2 = "*2_001\.fastq"
    SPAdesCommand = "spades.py {INPUTFILE}".format(INPUTFILE=FILENAME1 +FILENAME2)
    subprocess.call(SPAdesCommand, stdin=None, stdout=None, stderr=None, shell=True, timeout=None)
        FASTASTORAGEDIRECTORY =
        #STRAIN=?(*_S[0-9]+_L001_[R, L][1-2]_001\.fastq)
        STRAINNAME=FILENAME1[0:-21]
        os.rename(contigs.fasta, os.path.expanduser(~)/FASTASTORAGEDIRECTORY/STRAINNAME)

    pass

def run_mist():
    MISTCommand = "mist {mistinput1} {mistinput2}".format(???)
    subprocess.call (MISTCommand, stdin=None, stdout=None, stderr=None, shell=True, timeout=None)
    pass

def run_quast():
    #quast not installed?
    pass

def run_prokka():
    prokkaCommand = "prokka {prokkacontigs}".format()
    subprocess.call (prokkaCommand, stdin=None, stdout=None, stderr=None, shell=True, timeout=None)
    pass

def run_panseq():
    #not installed?
    pass

def run_roary():
    roaryCommand = "roary {options} {roaryinput}".format(options=? roaryinput=?)
    subprocess.call (roaryCommand, stdin=None, stdout=None, stderr=None, shell=True, timeout=None)
    pass

run_kraken() INPUTFILE=input()

run_spades()

