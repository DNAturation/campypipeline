#!/usr/bin/python3
# takes in a directory of paired end fastQs and runs through spades, quast, 
# prokka, roary, and MIST. This pipeline is designed to run on Kashyyyk, and so
# some arguments may have to be changed in each module for calling their 
# programs as they may not be in the same location
import os
import argparse
import time
import json
import trimgalorepipe
import spadespipe
import namestripper
import prokkapipe
import roarypipe
import quastpipe
import mistpipe
import mistdistrept
from multiprocessing import cpu_count


def run_trimgalore(trimcall, path, outpath, cores):
    trimgalorepipe.process(trimcall, path, outpath, cores)


def run_spades(spadescall, spadesin, spadesout, spadesfastaout, threads):
    spadespipe.process(spadescall, spadesin, spadesout, spadesfastaout, threads)


def run_mist(mistcall, path, outpath, testtype, alleles, reportfile, cores):
    mistpipe.process(mistcall, path, outpath, testtype, alleles, cores)
    mistdistrept.process(outpath, outpath, reportfile, testtype, cores)


def run_quast(quastcall, path, outpath, threads):
    quastpipe.process(quastcall, path, outpath, threads)


def run_prokka(prokkacall, nin, nout, prokout, threads):
    namestripper.process(nin, nout)
    prokkapipe.process(prokkacall, nout, prokout, threads)


def run_roary(roarycall, path, outpath, temp, processors):
    roarypipe.process(roarycall, path, outpath, temp, processors)


def configdefault():
    '''
    Creates default configuration file if one is not found. These settings are the locations of the programs on
    Kashyyyk, which this was developed using
    '''
    if not os.path.isfile('pipelineconfig.json'):
        print('Creating default configs file')
        configdefaults={
                        'trimgalore':['/home/phac/Bryce/GenomeAssembler/bin/trim_galore/trim_galore'],
                        'spades':['spades.py'],
                        'prokka':['prokka'],
                        'quast':['quast'],
                        'roary':['roary'],
                        'mist':['/home/phac/kye/assemblies_for_ed/Release/MIST.exe']
                        }
        with open('pipelineconfig.json', 'w') as f:
            json.dump(configdefaults, f)


def configreader():
    '''Reads the config file and returns all the file paths for the other programs.'''
    with open('pipelineconfig.json', 'r') as f:
        configs=json.load(f)
        trimcall=configs['trimgalore']
        spadescall=configs['spades']
        prokkacall=configs['prokka']
        quastcall=configs['quast']
        roarycall=configs['roary']
        mistcall=configs['mist']
    return trimcall, spadescall, prokkacall, quastcall, roarycall, mistcall


def configwriter(trim, spades, prokka, quast, roary, mist):
    '''
    each of the arguments comes in a list, and default value is None. The for loop access the list
    elements, and the if statement checks if the list is None, meaning nothing was input, so it
    defaults to the original. Else, replace it. It is in list to allow for if an interpreter needs
    to be called before the program
    '''
    with open('pipelineconfig.json', 'r') as f:
        defaults = json.load(f)

    configs=dict()

    for key in trim:
        if key:
            configs['trimgalore']= trim
        else:
            configs['trimgalore']=defaults['trimgalore']

    for key in spades:
        if key:
            configs['spades']= spades
        else:
            configs['spades']=defaults['spades']

    for key in prokka:
        if key:
            configs['prokka']= prokka
        else:
            configs['prokka']=defaults['prokka']

    for key in quast:
        if key:
            configs['quast']= quast
        else:
            configs['quast']=defaults['quast']

    for key in roary:
        if key:
            configs['roary']= roary
        else:
            configs['roary']=defaults['roary']

    for key in mist:
        if key:
            configs['mist']= mist
        else:
            configs['mist']=defaults['mist']

    with open('pipelineconfig.json', 'w') as g:
        json.dump(configs, g)


def arguments():
    parser = argparse.ArgumentParser(description='takes in commands of "run" for running through the pipeline, or "config" for setting up the run commands for the programs')
    subparsers = parser.add_subparsers(dest='subfunction')
    run_parser = subparsers.add_parser('run', description='For running through the pipeline. Requires markers file and alleles file for MIST, and directory of input files.')
    run_parser.add_argument('trimin', help='raw fastq reads')
    run_parser.add_argument('--trimout', default='cleanfastQs/', help='directory of trimmed fastQs')

    run_parser.add_argument('--spadesout', default='spadesout/', help='output directory for all files')
    run_parser.add_argument('-f', '--fasta', default='fasta/', help='output directory for fastas')
    run_parser.add_argument('--spades-sc', default=False, action='store_const', const='--sc', help='flag for single-cell data')
    run_parser.add_argument('--spades-rna', default=False, action='store_const', const='--rna', help='flag for running on RNA')
    run_parser.add_argument('--spades-iontorrent', default=False, action='store_const', const='--iontorrent', help='flag for running on iontorrent data, can take in BAM files')
    run_parser.add_argument('--spades-only-error-correction', default=False, action='store_const', const='--only-error-correction', help='flag for running error correction only')
    run_parser.add_argument('--spades-only-assembler', default=False, action='store_const', const='--only-assembler', help='runs only the assembly module')

    run_parser.add_argument('--quastout', default='quastout/')

    run_parser.add_argument('--namestripperout', default='prokka/')
    run_parser.add_argument('--prokkaout', default='prokka/')

    run_parser.add_argument('--roaryout', default='roaryout/')
    run_parser.add_argument('--roarysym', default='gffs/')

    run_parser.add_argument('--mistout', default='mistout/')
    run_parser.add_argument('-m', '--marker', help='path to and name of .markers file being run')
    run_parser.add_argument('-a', '--alleles', help='folder for alleles files')
    run_parser.add_argument('--report', default='mistreport.json', help='name of the report file')

    run_parser.add_argument('--assembled', action='store_false', help='flag to set if the inputs are already assembled; skips trimgalore and spades. If using this flag, please also use -f to set input path of fastas')
    run_parser.add_argument('-c', '--cores', type=int, default=cpu_count())


    config_parser = subparsers.add_parser('config', description='Configure the pipeline, telling it how to call/where to find all its required programs',
                                          help='(ex1. mist)\n (ex2. usr/bin/roary)\n (ex3. python spades.py')

    config_parser.add_argument('--trimgalore', help='How to call trimgalore', default=[None], nargs='+')
    config_parser.add_argument('--spades', help='How to call spades', default=[None], nargs='+')
    config_parser.add_argument('--quast', help='How to call quast', default=[None], nargs='+')
    config_parser.add_argument('--prokka', help='How to call prokka', default=[None], nargs='+')
    config_parser.add_argument('--roary', help='How to call roary', default=[None], nargs='+')
    config_parser.add_argument('--mist', help='How to call MIST', default=[None], nargs='+')


    return parser.parse_args()


def main():
    startt = time.time()
    configdefault() #automatically tries to create default config file if non are present
    args = arguments()
    if args.subfunction == 'config':
        configwriter(args.trimgalore, args.spades, args.prokka, args.quast, args.roary, args.mist)
    elif args.subfunction == 'run':
        trimcall, spadescall, prokkacall, quastcall, roarycall, mistcall = configreader()
        if args.assembled:
            print('Trimming reads')
            run_trimgalore(trimcall, args.trimin, args.trimout, args.cores)
            print('Assembling genomes')
            run_spades(spadescall, args.trimout, args.spadesout, args.fasta, str(args.cores))
        print('Generating quality report')
        run_quast(quastcall, args.fasta, args.quastout, str(args.cores))
        print('Running MIST')
        run_mist(mistcall, [args.fasta], args.mistout, args.marker, args.alleles, args.report, args.cores)
        print('Annotating genes')
        run_prokka(prokkacall, args.fasta, args.namestripperout, args.prokkaout, str(args.cores))
        print('Creating pangenome')
        run_roary(roarycall, args.prokkaout, args.roaryout, args.roarysym, str(args.cores))
        print('Pipeline ran for {} seconds'.format(time.time()-startt))


if __name__ == '__main__':
    main()



