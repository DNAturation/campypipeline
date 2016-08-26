#takes in fasta files from spades output and alters contig names to allow prokka to run

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
import argparse
import os
import glob



def dictionary(file):

    d={}
    prokkafriendlyd={}  # stores the new fasta name-sequence pairs

    strain = strain_name(file)
    with open(file, 'r') as f:  # opens each assembled genome file
        for record in SeqIO.parse(f, 'fasta'):
            d[record.id] = str(record.seq)
    for i, v in enumerate(sorted(d)):
        prokkafriendlyd[strain + str(i).zfill(5)] = d[v]  # fills in the end with 5 digits
    return prokkafriendlyd

def seqobject(pfd):
    record = ([SeqRecord(Seq(pfd[k], IUPAC.unambiguous_dna), id=k) for k in sorted(pfd)])  # turns the dictionary into a record object for writing to a fasta file
    return record

def pathfinder(outdir):
    if not os.access(outdir, os.F_OK):
        os.mkdir(outdir)

def writer(record, outpath, strain):

    outputhandle = open('{}/{}.fasta'.format(outpath, strain), 'w+')
    SeqIO.write(record, outputhandle, 'fasta')
    outputhandle.close()

def arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--outpath', default='./prokka')
    parser.add_argument('path')

    return parser.parse_args()

def strain_name(st):
    return os.path.splitext(os.path.basename(st))[0]

def process(path, outpath):

    pathfinder(outpath)
    fastafiles = glob.glob(path+'*.fasta')
    for file in fastafiles:
        strain = strain_name(file)
        pfd = dictionary(file)
        record = seqobject(pfd)
        writer(record, outpath, strain)

def main():
    args = arguments()
    process(args.path, args.outpath)


if __name__ == '__main__':
    main()

