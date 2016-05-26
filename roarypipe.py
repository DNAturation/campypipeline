#takes a group of .gff files from prokka and outputs

import argparse
import glob
import os
import subprocess
from multiprocessing import cpu_count

def gff(path, temp):
    listofiles = glob.glob(path+'*/*.gff')
    print (listofiles)
    for src in listofiles:

        strain, extension = os.path.splitext(os.path.basename(src))
        dst = temp + strain + '.gff'

        if os.access(dst, os.F_OK):
            continue

        paths = [os.path.abspath(x) for x in (src, dst)]
        os.symlink(*paths)

def pathfinder(out_dir):
    if not os.access(out_dir, os.F_OK):
        os.mkdir(out_dir)


def roaryargs(threads, out_dir, temp):
    listoffiles = glob.glob(temp + '*.gff')
    files = " ".join(str(files) for files in listoffiles)
    roary = 'roary '+'-p '+str(threads)+' -f '+out_dir+' '+files
    # roary = ('roary',
    #          '-p', '{}'.format(str(threads)),
    #          '-f', '{}'.format(out_dir),
    #          files
    #          )
    # yield roary
    return roary

def runroary(threads, out_dir, temp):
    # for roary in roaryargs(threads, out_dir, temp):
    #     subprocess.call(roary)
    subprocess.call(roaryargs(threads, out_dir, temp), shell=True)




def arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--outpath', default='./roaryout/')
    parser.add_argument('-t', '--temp', default='./gffs/')
    parser.add_argument('-p', '--processors', type=int, default=cpu_count())
    parser.add_argument('path')

    return parser.parse_args()

def process(path, outpath, temp, processors):
    pathfinder(outpath)
    pathfinder(temp)

    gff(path, temp)
    runroary(processors, outpath, temp)


def main():
    args = arguments()
    process(args.path, args.outpath, args.temp, args.processors)

    # pathfinder(args.outpath)
    # pathfinder(args.temp)
    #
    # gff(args.path, args.temp)
    # runroary(args.processors, args.outpath, args.temp)

if __name__ == '__main__':
    main()

