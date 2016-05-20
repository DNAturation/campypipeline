from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
import re
import argparse
import os


def dictionary(path):
    d={}
    prokkafriendlyd={}
    # pattern = '\/([^\/])+$'
    # strain = path[[m.start() for m in re.finditer(pattern, path)]:]
    strain = strain_name(path)
    with open(path, 'r') as f:
        for record in SeqIO.parse(f, 'fasta'):
            d[record.id] = str(record.seq)
    for i, v in enumerate(sorted(d)):
        prokkafriendlyd[strain + str(i).zfill(5)] = d[v]
    return prokkafriendlyd

def seqobject(pfd):
    record = ([SeqRecord(Seq(pfd[k], IUPAC.unambiguous_dna), id=k) for k in sorted(pfd)])
    return record

def pathfinder(outdir, strain):
    if not os.access(outdir, os.F_OK):
        os.mkdir(outdir)

def writer(record, outpath, strain):

    outputhandle = open(outpath+'/'+strain+'prokka.fasta', 'w+')
    SeqIO.write(record, outputhandle, 'fasta')
    outputhandle.close()

def arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--outpath', default='./prokka')
    parser.add_argument('path')

    return parser.parse_args()

def strain_name(s):
    return os.path.splitext(os.path.basename(s))[0]

def main():
    args = arguments()
    # pattern = '\/([^\/])+$'

    # strain = args.path[[m.start() for m in re.finditer(pattern, args.path)]:]
    strain = strain_name(args.path)

    pathfinder(args.outpath, strain)
    pfd = dictionary(args.path)
    record = seqobject(pfd)
    writer(record, args.outpath, strain)

if __name__ == '__main__':
    main()
