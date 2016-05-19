import argparse
import os
import subprocess
import glob

def inputfastqs(path):
    listoffastq=glob.glob(path+'*.fastq')
    pairs = []
    for i, v in enumerate(listoffastq):
        for match in range(i+1, len(lsitoffastq)):
            compare = list(zip(v, listoffastq[match]))
            for pos, cv in enumerate(compare):
                if cv[0] == cv[1]:
                    continue
                elif cv[0] in '12' and compare[pos-1][0] == 'R':
                    pairs.append((v, listoffastq[match]))
                else:
                    break

    return [sorted(t) for t in pairs]



def namer(fast1, fast2): #gets strain names
    endposition = 0
    for i, v in enumerate(fast1):
        if fast1[i] == fast2[i]:
            endposition = i
            continue
        else:
            break
    Strain_Name = fast1[:endposition-6]
    return Strain_Name

def pathfinder(Output_Dir):
    if not os.access('./' + Output_Dir, os.F_OK):
        os.mkdir(Output_Dir)


def fastapath():
    if not os.access('./fasta/', os.F_OK):
        os.mkdir('fasta/')


def get_strain_names(file_pairs): #returns a list of strain names
    return [namer(*pair) for pair in file_pairs]

def format_spades_args(strain_names, file_pairs, Output_Dir): # return a list of lists]
    for i in file_pairs:
        strain1 = file_pairs[i][0]
        strain2 = file_pairs[i][1]
        subprocess.call('spades.py -o OPL -1 STRAIN1 -2 STRAIN2 --careful --threads 32'.replace('OPL', Output_Dir)\
                        .replace('STRAIN1', strain1)\
                        .replace('STRAIN2', strain2))
        subprocess.call('mv OPL/contigs.fasta /fasta/STRAINNAME.fasta'.replace('OPL', Output_Dir)\
                        .replace('STRAINNAME', strain_names))


def run_spades():
    pass

def arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs=1)
    parser.add_argument('-o', '--outpath', required=False, default='./temprawout')

    return parser.parse_args()


def main():

    args = arguments()
    pathfinder(args.out)
    fastapath()
    file_pairs = inputfastqs(args.path)
    names = get_strain_names(file_pairs)

    format_spades_args(names, file_pairs, args.outpath)
    run_spades()

if __name__ == '__main__':
    main()