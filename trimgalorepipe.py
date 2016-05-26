#takes in raw reads and outputs reads with primers/controls removed
import argparse
import os
import subprocess
import glob

def getfastq(path):
    fastqinput=glob.glob(path+'*.fastq')
    return fastqinput

def pathfinder(outpath):
    if not os.access(outpath, os.F_OK):
        os.mkdir(outpath)

def trimargU(fastqinput, outpath):
    for file in fastqinput:
        trims = ('trim_galore',
                 '-o', outpath,
                 file)

        yield trims

def runtrimU(fastqinput, outpath):
    for trims in trimargU(fastqinput, outpath):
        subprocess.call(trims)

def trimargP(fastqinput, outpath):
    for forward, reverse in zip(fastqinput[0::2], fastqinput[1::2]):
        trims = ('trim_galore',
                 '-o', outpath,
                 '--paired',
                 forward, reverse)
        yield trims

def runtrimP(fastqinput, outpath):
    for trims in trimargP(fastqinput, outpath):
        subprocess.call(trims)

def rename(outpath):
    outlist = glob.glob(outpath + '*.fq')
    for file in outlist:
        strain, extension = os.path.splitext(os.path.basename(file))
        os.rename(file, outpath+strain+'.fastq')

def arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', '--unpaired', action='store_true')
    parser.add_argument('-o', '--outpath', default='./cleanfastq/')
    parser.add_argument('path')
    return parser.parse_args()

def process(path, outpath, UP):
    fastqinput = getfastq(path)
    pathfinder(outpath)
    if UP == True:
        runtrimU(fastqinput, outpath)
    else:
        runtrimP(fastqinput, outpath)
    rename(outpath)



def main():
    args = arguments()
    process(args.path, args.outpath, args.unpaired)

if __name__ == '__main__':
    main()