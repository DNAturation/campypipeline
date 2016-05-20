import os
import argparse
import glob
import subprocess
from multiprocessing import cpu_count

def strain_name(s):
    for v in glob.glob(s+'*prokka.fasta'):
        yield os.path.splitext(os.path.basename(v))[0]

def infiles(path):
    listoinput=glob.glob(path+'*prokka.fasta')
    return listoinput


def pathfinder(outdir):
    if not os.access(outdir, os.F_OK):
        os.mkdir(outdir)

def prokkargs(strain, inlist, outpath, cores):
    for file in inlist:
        prok = ('prokka',
                '--outdir', outpath + strain,
                '--locustag', strain,
                '--prefix', strain,
                '--cpus', str(cores),
                file)


        yield prok

def runprokka(strain, inlist, outpath, cores):
    for prok in prokkargs(strain, inlist, outpath, cores):
        subprocess.call(prok)

def arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--outpath', default='./prokka/')
    parser.add_argument('-c', '--cpus', type=int, default=int(cpu_count()))
    parser.add_argument('path', default='./prokka/*-')

    return parser.parse_args()

def main():
    args=arguments()
    inlist = infiles(args.path)

    pathfinder(args.outpath)


    for strain in strain_name(args.path):
        runprokka(strain, inlist, args.outpath, args.cpus)


if __name__ == '__main__':
    main()