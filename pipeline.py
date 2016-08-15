#!/usr/bin/python3
# takes in a directory of paired end fastQs and runs through spades, quast, 
# prokka, roary, and MIST. This pipeline is designed to run on Kashyyyk, and so
# some arguments may have to be changed in each module for calling their 
# programs as they may not be in the same location
import os
import trimgalorepipe
import argparse
import time
import spadespipe
import namestripper
import prokkapipe
import roarypipe
import quastpipe
import mistpipe
from multiprocessing import cpu_count


def run_trimgalore(path, outpath, cores):
    trimgalorepipe.process(path, outpath, cores)

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
    # subparsers = parser.add_subparsers(dest='subfunction')
    parser.add_argument('trimin', help='raw fastq reads')
    parser.add_argument('--trimout', default='cleanfastQs/', help='directory of trimmed fastQs')


    parser.add_argument('--spadesout', default='spadesout/', help='output directory for all files')
    parser.add_argument('-f', '--fasta', default='fasta/', nargs='+', help='output directory for fastas')
    parser.add_argument('--spades-sc', default=False, action='store_const', const='--sc', help='flag for single-cell data')
    parser.add_argument('--spades-rna', default=False, action='store_const', const='--rna', help='flag for running on RNA')
    parser.add_argument('--spades-iontorrent', default=False, action='store_const', const='--iontorrent', help='flag for running on iontorrent data, can take in BAM files')
    parser.add_argument('--spades-only-error-correction', default=False, action='store_const', const='--only-error-correction', help='flag for running error correction only')
    parser.add_argument('--spades-only-assembler', default=False, action='store_const', const='--only-assembler', help='runs only the assembly module')


    parser.add_argument('--quastout', default='quastout/')
    
    parser.add_argument('--namestripperout', default='prokka/')
    parser.add_argument('--prokkaout', default='prokka/')
    
    parser.add_argument('--roaryout', default='roaryout/')
    parser.add_argument('--roarysym', default='gffs/')
    
    parser.add_argument('--mistout', default='mistout/')
    parser.add_argument('-m', '--marker', help='path to and name of .markers file being run')
    parser.add_argument('-a', '--alleles', help='folder for alleles files')
    
    parser.add_argument('--assembled', action='store_false', help='flag to set if the inputs are already assembled; skips trimgalore and spades')
    parser.add_argument('-c', '--cores', type=int, default=cpu_count())


    # config_parser = subparsers.add_parser('config')
    # config_parser.add_argument('--trimgalore', help='path to program')
    # config_parser.add_argument('--spades', help='path to program')
    # config_parser.add_argument('--quast')
    # config_parser.add_argument('--prokka')
    # config_parser.add_argument('--roary')
    # config_parser.add_argument('--mist')
    return parser.parse_args()


def main():
    startp = time.clock()
    startt = time.time()
    args = arguments()
    # if subparser:
        # pass
        #configstuff
    # else:
    if args.assembled:
        print('Trimming reads')
        run_trimgalore(args.trimin, args.trimout, args.cores)
        print('Assembling genomes')
        run_spades(args.trimout, args.spadesout, args.fasta, str(args.cores))
    print('Generating quality report')
    run_quast(args.fasta, args.quastout, str(args.cores))
    print('Running MIST')
    run_mist([args.fasta], args.mistout, args.marker, args.alleles, args.cores)
    print('Annotating genes')
    run_prokka(args.fasta, args.namestripperout, args.prokkaout, str(args.cores))
    print('Creating pangenome')
    run_roary(args.prokkaout, args.roaryout, args.roarysym, str(args.cores))
    print('Pipeline ran for {} seconds (process time), {} seconds in real-time'.format(time.clock()-startp, time.time()-startt))


if __name__ == '__main__':
    main()



