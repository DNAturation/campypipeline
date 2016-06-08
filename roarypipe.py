#takes a group of .gff files from prokka and performs a pangenome analysis,
# outputs various Rtab files and summaries

import argparse
import glob
import os
import subprocess
import string
from multiprocessing import cpu_count

def gff(path, temp):
    '''grabs list of .gff files from multiple strains output by prokka, symlinks them into a temp folder;
    if symlink folder already exists, tries a new folder'''
    listofiles = glob.glob(path+'*/*.gff')
    listofattempts = ['']
    listofattempts = listofattempts+list(string.ascii_lowercase)
    for x in listofattempts:
        if os.access(temp, os.F_OK):
            if sorted(os.listdir(temp)) == sorted(listofiles):
                print('Set of symlinked files already exists! Has Roary already been run on this data set?')
                return x
        elif os.access(temp[:-1]+x+'/', os.F_OK):
            continue
        else:
            os.mkdir(temp[:-1]+x+'/')
            for src in listofiles:

                strain, extension = os.path.splitext(os.path.basename(src))
                dst = temp[:-1]+x+'/' + strain + '.gff'


                paths = [os.path.abspath(x) for x in (src, dst)]
                os.symlink(*paths)
            return x

def pathfinder(out_dir):
    if not os.access(out_dir, os.F_OK):
        os.mkdir(out_dir)


def roaryargs(threads, out_dir, temp, x):
    '''grabs all symlinked files, and organizes them into a space delimited string for input into roary'''
    listoffiles = glob.glob(temp[:-1]+x+'/' + '*.gff')
    files = " ".join(str(files) for files in listoffiles)
    roary = 'roary '+'-p '+str(threads)+' -f '+out_dir+' '+files

    return roary

def runroary(threads, out_dir, temp, x):

    subprocess.call(roaryargs(threads, out_dir, temp, x), shell=True)




def arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--outpath', default='./roaryout/')
    parser.add_argument('-t', '--temp', default='./gffs/')
    parser.add_argument('-p', '--processors', type=int, default=cpu_count())
    parser.add_argument('path')

    return parser.parse_args()

def process(path, outpath, temp, processors):
    pathfinder(outpath)

    x = gff(path, temp)
    runroary(processors, outpath, temp, x)


def main():
    args = arguments()
    process(args.path, args.outpath, args.temp, args.processors)


if __name__ == '__main__':
    main()

