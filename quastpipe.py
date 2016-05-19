import argparse
import os
import subprocess
import glob

def inputfasta(path):
    listoffasta=glob.glob(path+'*.fasta')
    return listoffasta

def pathfinder(Output_Dir):
    if not os.access('./' + Output_Dir, os.F_OK):
        os.mkdir(Output_Dir)


def straingetter(listoffasta, path):
    for filename in listoffasta:
        strainname = filename[len(path):]
        yield strainname


def quast_arguments(inputlist, strain, out_dir, threads):
    for fasta in inputlist:
        for strainname in strain:
            quast = ('/home/cintiq/Desktop/quast-4.0/quast.py',
                 '-o', '{}/{}'.format(out_dir, strainname),
                 '-t', '{}'.format(threads),
                 fasta)
            yield quast

def run_quast(inputlist, strain, out_dir, threads):
    for quast in quast_arguments(inputlist, strain, out_dir, threads):
        subprocess.call(quast)



def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--outpath', default='quastout')
    parser.add_argument('-t', '--threads', type=int, default=2)
    parser.add_argument('path')
    return parser.parse_args()



def main():
    args = arguments()
    pathfinder(args.outpath)
    infa = inputfasta(args.path)
    strain_name = straingetter(infa, args.path)
    run_quast(infa, strain_name, args.outpath, args.threads)

if __name__ == '__main__':
    main()