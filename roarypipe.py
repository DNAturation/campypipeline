#takes a group of .gff files from prokka and performs a pangenome analysis,
# outputs various Rtab files and summaries

import argparse
import glob
import os
import subprocess
import string
from multiprocessing import cpu_count
import shutil

def gff(path, temp):
    '''
    grabs list of .gff files from multiple strains output by prokka, symlinks them into a temp folder;
    if symlink folder already exists, tries a new folder. Added because this generally is an intermediate step that may
    not be checked and emptied like the others
    '''
    listofiles = glob.glob(os.path.join(path, '*/*.gff'))
    filenames = [os.path.basename(file) for file in listofiles]
    listofattempts = ['']+list(string.ascii_lowercase)
    for copyletter in listofattempts:
        if os.path.isdir(os.path.dirname(temp)) and (sorted(os.listdir(temp)) == sorted(filenames)):
            print('Set of symlinked files already exists! Has Roary already been run on this data set?')
            return copyletter
        elif os.path.isdir(os.path.dirname(temp)+copyletter):
            if copyletter == 'z':
                print('Error: unable to find empty directory. Please make sure to remove all directories with the same name as the one given to the temp option(default gffs)')
                raise Exception('No free directories')
            else:
                continue
        else:
            os.mkdir(os.path.dirname(temp)+copyletter)
            for src in listofiles:
                strain, extension = os.path.splitext(os.path.basename(src))
                dst = os.path.join(os.path.dirname(temp)+copyletter, strain+'.gff')


                paths = [os.path.abspath(x) for x in (src, dst)]
                os.symlink(*paths)
            return copyletter

def pathfinder(out_dir):
    if not os.access(out_dir, os.F_OK):
        os.mkdir(out_dir)


def roaryargs(roarycall, threads, out_dir, temp, copyletter):
    '''grabs all symlinked files, and organizes them into a space delimited string for input into roary'''
    files = glob.glob(os.path.join(temp+copyletter, '*.gff'))
    roaryargs = roarycall + ['-p', str(threads),
                '-f', out_dir] + files

    return roaryargs

def runroary(roarycall, threads, out_dir, temp, copyletter):

    subprocess.call(roaryargs(roarycall, threads, out_dir, temp, copyletter))


def arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--outpath', default='roaryout/')
    parser.add_argument('-t', '--temp', default='gffs/')
    parser.add_argument('-p', '--processors', type=int, default=cpu_count())
    parser.add_argument('--roarycall', nargs='+', default=['roary'])
    parser.add_argument('path')

    return parser.parse_args()

def process(roarycall, path, outpath, temp, processors):
    pathfinder(outpath)

    copyletter = gff(path, temp)
    runroary(roarycall, processors, outpath, temp, copyletter)


def main():
    args = arguments()
    process(args.roarycall, args.path, args.outpath, args.temp, args.processors)


if __name__ == '__main__':
    main()

