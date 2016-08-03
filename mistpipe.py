#takes in a list of fasta files from spades (maybe quast) and runs blast on them,
# identifying the strains they came from (MLST)

import argparse
import os
import glob
import subprocess
import multiprocessing
import shutil
import csv
import re
import json

def getfasta(path):
    fastalist = []
    blurgh = glob.glob(path+'*.fasta')
    for file in blurgh:
        fastalist.append(file)
    return fastalist


def pathfinder(outpath):
    if not os.access(outpath, os.F_OK):
        os.mkdir(outpath)
    if not os.access(outpath+'temp/', os.F_OK):
        os.mkdir(outpath+'temp/')


def mistargs(fastalist, outpath, testtypename, testtype, alleles):
    for file in fastalist:
        strain, extension = os.path.splitext(os.path.basename(file))
        if not os.path.isfile(outpath+strain+testtypename+'.json'):
            # missed=('/home/cintiq/Desktop/campylobacterjejuni/mist/bin/Release/MIST.exe', '-b',
            missed=('mist', '-b',
                    '-j', outpath+strain+testtypename+'.json',
                    '-a', alleles,
                    '-t', testtype,
                    '-T', outpath+'temp/'+strain+'/',
                    file)
            yield missed, strain
        else:
            print('skipping strain '+strain+' due to .json file for this test already existing')

def testnamegetter(testtype):
    with open(testtype, 'r') as f:
        try: #try accessing markers file as .json file first
            data = json.load(f)
            for genome, keys in data.items():
                for key in keys:
                    if re.match('T(est)?\.?[-\._ ]?Name.*', key, flags=re.IGNORECASE):
                        return keys[key]

        except KeyError: #if access as .json file fails, try to access as csv file
            reader=csv.reader(f, delimiter='\t')
            next(reader, None)
            for x in reader:
                testname=x[1]
                return testname

def runmist(missed, outpath, strain):
    if not os.access(outpath+'temp/'+strain+'/', os.F_OK):
        os.mkdir(outpath+'temp/'+strain+'/')
    subprocess.call(missed)
    shutil.rmtree(outpath+'temp/'+strain+'/')






def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--outpath', default='./mistout/')
    parser.add_argument('-a', '--alleles', default='alleles/')
    parser.add_argument('-t', '--testtype', required=True, help='path to and type of test/markers file, ex. CGF119')
    parser.add_argument('-c', '--cores', default=multiprocessing.cpu_count(), help='number of cores to run on')
    parser.add_argument('path', nargs='+')
    return parser.parse_args()


def process(path, outpath, testtype, alleles, cores):
    listlist = getfasta(path)
    testtypename=testnamegetter(testtype)
    pool = multiprocessing.Pool(int(cores))
    pathfinder(outpath)
    margs = mistargs(listlist, outpath, testtypename, testtype, alleles)
    for missed, strain in margs:
        pool.apply_async(runmist, args=(missed, outpath, strain))
    pool.close()
    pool.join()


def main():
    args = arguments()
    process(args.path, args.outpath, args.testtype, args.alleles, args.cores)

if __name__ == '__main__':
    main()