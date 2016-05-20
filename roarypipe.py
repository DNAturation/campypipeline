import argparse
import glob
import os
import subprocess
from multiprocessing import cpu_count

def gff(path, temp):
    listofiles = glob.iglob(path+'*/*.gff')
    for src in listofiles:

        strain, b = os.path.splitext(os.path.basename(src))
        dst = temp + strain + '.gff'

        if os.access(dst, os.F_OK):
            continue

        paths = [os.path.abspath(x) for x in (src, dst)]
        os.symlink(*paths)

def pathfinder(out_dir):
    if not os.access(out_dir, os.F_OK):
        os.mkdir(out_dir)


def roaryargs(threads, out_dir, temp):
    for infiles in glob.iglob(temp + '*.gff'):
        roary = ('roary',
                '-p', str(threads),
                 '-f', out_dir,
                 infiles)
        yield roary

def runroary(threads, out_dir, temp):
    for roary in roaryargs(threads, out_dir, temp):
        subprocess.call(roary)




def arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--outpath', default='roaryout/')
    parser.add_argument('-t', '--temp', default='gffs/')
    parser.add_argument('-p', '--processors', type=int, default=cpu_count())
    parser.add_argument('path')

    return parser.parse_args()

def main():
    args = arguments()

    pathfinder(args.outpath)
    pathfinder(args.temp)

    gff(args.path, args.temp)
    runroary(args.processors, args.outpath, args.temp)

if __name__ == '__main__':
    main()

