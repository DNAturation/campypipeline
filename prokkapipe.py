#takes in fasta files from spades/namestripper and outputs .gff files for roary

import os
import argparse
import glob
import subprocess
from multiprocessing import cpu_count

def input_strains(fasta_path):
    for v in glob.glob(fasta_path + '*.fasta'):
        # print ('instrains', v, os.path.splitext(os.path.basename(v))[0])
        yield v, os.path.splitext(os.path.basename(v))[0]

def pathfinder(outdir):
    if not os.access(outdir, os.F_OK):
        os.mkdir(outdir)

def prokkargs(strain, fasta, outpath, cores):
    prok = ('prokka',
            '--outdir', outpath + strain,
            '--locustag', strain,
            '--prefix', strain,
            '--cpus', str(cores),
            fasta)
    # print('prokkargs', prok)

    return prok

def runprokka(strain, fasta, outpath, cores):

    prok = prokkargs(strain, fasta, outpath, cores)
    # print('runprok', prok)
    subprocess.call(prok)

def arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--outpath', default='./prokka/')
    parser.add_argument('-c', '--cpus', type=int, default=cpu_count())
    parser.add_argument('path', default='./prokka/*-')

    return parser.parse_args()

def process(path, outpath, cpus):
    pathfinder(outpath)
    # print('process', path, outpath)

    for fasta, strain in input_strains(path):
        # print ('meh', strain, fasta, outpath)
        runprokka(strain, fasta, outpath, cpus)

def main():

    args = arguments()
    # print ('args', args)
    process(args.path, args.outpath, args.cpus)
    # pathfinder(args.outpath)
    # print(args)
    #
    # for fasta, strain in input_strains(args.path):
    #     runprokka(strain, fasta, args.outpath, args.cpus)

if __name__ == '__main__':
    main()