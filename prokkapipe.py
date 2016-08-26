#takes in fasta files from spades/namestripper and outputs .gff files for roary

import os
import argparse
import glob
import subprocess
from multiprocessing import cpu_count

def input_strains(fasta_path):
    for v in glob.glob(os.path.join(fasta_path, '*.fasta')):
        yield v, os.path.splitext(os.path.basename(v))[0]

def pathfinder(outdir):
    if not os.access(outdir, os.F_OK):
        os.mkdir(outdir)

def prokkargs(prokkacall, strain, fasta, outpath, cores):  # arguments for calling prokka
    prok = prokkacall + ['--outdir', outpath + strain,
            '--locustag', strain,
            '--prefix', strain,
            '--cpus', str(cores),
            fasta]

    return prok

def runprokka(prokkacall, strain, fasta, outpath, cores):

    prok = prokkargs(prokkacall, strain, fasta, outpath, cores)
    subprocess.call(prok)

def arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--outpath', default='./prokka/')
    parser.add_argument('-c', '--cpus', type=int, default=cpu_count())
    parser.add_argument('--prokkacall', nargs='+', default=['prokka'])
    parser.add_argument('path', default='./prokka/*-')

    return parser.parse_args()

def process(prokkacall, path, outpath, cpus):
    pathfinder(outpath)

    for fasta, strain in input_strains(path):
        runprokka(prokkacall, strain, fasta, outpath, cpus)

def main():

    args = arguments()
    process(args.prokkacall, args.path, args.outpath, args.cpus)

if __name__ == '__main__':
    main()