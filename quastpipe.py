#organize fasta files from spades and output organized fasta files


import argparse
import os
import subprocess
import glob
from multiprocessing import cpu_count

def inputfasta(path):
    listoffasta=glob.glob(path+'*.fasta')
    return listoffasta

def pathfinder(Output_Dir):
    if not os.access(Output_Dir, os.F_OK):
        os.mkdir(Output_Dir)


def straingetter(listoffasta, path):
    for filename in listoffasta:
        strainname = filename[len(path):-6]
        yield strainname


def quast_arguments(quastcall, inputlist, strain, out_dir, threads):
    for fasta in inputlist:
        for strainname in strain:
            quast = quastcall + ['-o', '{}/{}'.format(out_dir, strainname),
                 '-t', '{}'.format(threads),
                 fasta]
            yield quast

def run_quast(quastcall, inputlist, strain, out_dir, threads):
    for quast in quast_arguments(quastcall, inputlist, strain, out_dir, threads):
        subprocess.call(quast)



def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--outpath', default='./quastout')
    parser.add_argument('-t', '--threads', type=int, default=cpu_count())
    parser.add_argument('--quastcall', nargs='+', default=['quast'])
    parser.add_argument('path')
    return parser.parse_args()

def process(quastcall, path, outpath, threads):
    pathfinder(outpath)
    infa = inputfasta(path)
    strain_name = straingetter(infa, path)
    run_quast(quastcall, infa, strain_name, outpath, threads)


def main():
    args = arguments()
    process(args.quastcall, args.path, args.outpath, args.threads)

if __name__ == '__main__':
    main()