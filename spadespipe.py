#takes in a directory of fastq files that have had their adapters trimmed by trimgalore and
# runs spades on them, outputting fasta files

import argparse
import os
import subprocess
import glob
import shutil
from multiprocessing import cpu_count

def inputfastqs(path):
    '''grabs fastq files from input path and sorts them into forward and reverse pair tuples'''
    listoffastq=glob.glob(os.path.join(path, '*'))
    pairs = []
    for i, v in enumerate(listoffastq):
        for match in range(i+1, len(listoffastq)):
            compare = list(zip(v, listoffastq[match]))
            for pos, cv in enumerate(compare):
                if cv[0] == cv[1]:
                    continue
                elif cv[0] in '12' and compare[pos-1][0] == 'R':
                    pairs.append((v, listoffastq[match], path))
                else:
                    break
    return[t for t in pairs]


def namer(fast1):
    '''gets strain names'''
    strain, extension = os.path.splitext(os.path.basename(fast1))
    Strain_Name = strain[:-6]
    return Strain_Name


def pathfinder(Output_Dir):
    if not os.access(Output_Dir, os.F_OK):
        os.mkdir(Output_Dir)


def fastapath(fasta):
    if not os.access(fasta, os.F_OK):
        os.mkdir(fasta)


def get_strain_names(file):
    '''retrieves strain names from the paired tuples'''
    return (namer(x[0]) for x in file)


def format_spades_args(spadescall, strain_names, file_pairs, output_dir, fastaout, threads):
    '''creates arguments for calling spades, list of tuples'''
    for strain, pair in zip(strain_names, file_pairs):
        spades = spadescall + ['-o', '{}/{}'.format(output_dir, strain),
               '-1', pair[0],
               '-2', pair[1],
               '--careful',
               '--threads', threads]

        src = os.path.join(output_dir, strain, 'contigs.fasta')
        dst = os.path.join(fastaout, strain+'.fasta')

        yield spades, src, dst

def run_spades(spadescall, strain_names, file_pairs, output_dir, fastaout, threads):
    '''
    runs spades on the provided arguments from spades args; if fasta file for strain
    already exists, skips the file
    '''
    for spades, src, dst in format_spades_args(spadescall, strain_names, file_pairs, output_dir, fastaout, str(threads)):
        if not os.path.isfile(dst):

            subprocess.call(spades)
            shutil.copy(src, dst)
        else:
            print(dst+' already exists! Skipping strain.')

def arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--outpath', default='spadesout/', help='output directory for all files')
    parser.add_argument('-f', '--fastaout', default='fasta/', help='output directory for fastas')
    parser.add_argument('-t', '--threads', type=int, default=cpu_count())
    parser.add_argument('--spadescall', nargs='+', default=['spades.py'])
    parser.add_argument('path', help='directory of fastqs for input')

    return parser.parse_args()

def process(spadescall, path, outpath, fastaout, threads):
    if not os.access(path, os.F_OK):
        print ('Error: FastQ directory not found')
    pathfinder(outpath)
    fastapath(fastaout)
    file_pairs = inputfastqs(path)
    names = get_strain_names(file_pairs)
    run_spades(spadescall, names, file_pairs, outpath, fastaout, threads)


def main():

    args = arguments()
    process(args.spadescall, args.path, args.outpath, args.fastaout, args.threads)


if __name__ == '__main__':
    main()