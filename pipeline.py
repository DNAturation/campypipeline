#!/usr/bin/python3
import os
import trimgalorepipe
import argparse
import spadespipe
import namestripper
import prokkapipe
import roarypipe
import quastpipe
import mistpipe
from multiprocessing import cpu_count


def run_trimgalore(path, outpath):
    trimgalorepipe.process(path, outpath)

def run_kraken():
    '''Formats Kraken args and runs kraken'''

    pass


def run_spades(spadesin, spadesout, spadesfastaout, threads):
    spadespipe.process(spadesin, spadesout, spadesfastaout, threads)

def run_mist(path, outpath, testtype, alleles, cores):
    mistpipe.process(path, outpath, testtype, alleles, cores)

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
    parser.add_argument('--trimout', default='cleanfastQs/', help='directory of trimmed fastQs')
    parser.add_argument('-c', '--cores', type=int, default=cpu_count())
    parser.add_argument('--spadesout', default='temprawout/', help='output directory for all files')
    parser.add_argument('-f', '--fasta', default='fasta/', nargs='+', help='output directory for fastas')
    parser.add_argument('--quastout', default='quastout/')
    parser.add_argument('--namestripperout', default='prokka/')
    parser.add_argument('--prokkaout', default='prokka/')
    parser.add_argument('--roaryout', default='roaryout/')
    parser.add_argument('--roarysym', default='gffs/')
    parser.add_argument('--mistout', default='mistout/')
    parser.add_argument('-m', '--marker', help='path to and name of .markers file being run')
    parser.add_argument('-a', '--alleles', help='folder for alleles files')
    return parser.parse_args()


def main():
    args = arguments()
    run_trimgalore(args.trimin, args.trimout)
    run_spades(args.trimout, args.spadesout, args.fasta, str(args.cores))
    run_quast(args.fasta, args.quastout, str(args.cores))
    run_mist(args.fasta, args.mistout, args.marker, args.alleles, args.cores)
    run_prokka(args.fasta, args.namestripperout, args.prokkaout, str(args.cores))
    run_roary(args.prokkaout, args.roaryout, args.roarysym, str(args.cores))


if __name__ == '__main__':
    main()



