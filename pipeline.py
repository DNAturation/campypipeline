#!/usr/bin/python3
import os
import subprocess
import trimgalorepipe
import argparse
import spadespipe
import namestripper
import prokkapipe
import roarypipe
import quastpipe
from multiprocessing import cpu_count


def run_trimgalore(path, outpath, UP):
    trimgalorepipe.process(path, outpath, UP)

def run_kraken():
    '''Formats Kraken args and runs kraken'''

    pass


def run_spades(spadesin, spadesout, spadesfastaout, threads):
    spadespipe.process(spadesin, spadesout, spadesfastaout, threads)

# def run_mist():
#     MISTCommand = "mist {mistinput1} {mistinput2}".format(???)
#     subprocess.call (MISTCommand, stdin=None, stdout=None, stderr=None, shell=True, timeout=None)
#     pass

def run_quast(path, outpath, threads):
    quastpipe.process(path, outpath, threads)

def run_prokka(nin, nout, prokout, threads):
    namestripper.process(nin, nout)
    prokkapipe.process(nout, prokout, threads)

def run_panseq():
    pass

def run_roary(path, outpath, temp, processors):
    roarypipe.process(path, outpath, temp, processors)


def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('trimin', help='raw fastq reads')
    parser.add_argument('-To', '--trimout', default='./cleanfastQs/', help='directory of trimmed fastQs')
    parser.add_argument('-t', '--threads', type=int, default=cpu_count())
    parser.add_argument('-SPo', '--spadesout', default='./temprawout', help='output directory for all files')
    parser.add_argument('-f', '--fasta', default='./fasta/', help='output directory for fastas')
    parser.add_argument('-Qo', '--quastout', default='./quastout/')
    parser.add_argument('-NSo', '--namestripperout', default='./prokka/')
    parser.add_argument('-Po', '--prokkaout', default='./prokka/')
    parser.add_argument('-Ro', '--roaryout', default='./roaryout/')
    parser.add_argument('-Rs', '--roarysym', default='./gffs/')
    parser.add_argument('-UP', '--unpaired', action='store_true')
    return parser.parse_args()


def main():
    args = arguments()
    run_trimgalore(args.trimin, args.trimout, args.unpaired)
    run_spades(args.trimout, args.spadesout, args.fasta, str(args.threads))
    run_quast(args.fasta, args.quastout, str(args.threads))
    run_prokka(args.fasta, args.namestripperout, args.prokkaout, str(args.threads))
    run_roary(args.prokkaout, args.roaryout, args.roarysym, str(args.threads))


if __name__ == '__main__':
    main()



