#takes in raw reads and outputs reads with primers/controls removed
import argparse
import os
import subprocess
import glob
import multiprocessing

def getfastq(path):
    fastqinput=glob.glob(path+'*.fastq')
    return sorted(fastqinput)

def pathfinder(outpath):
    if not os.access(outpath, os.F_OK):
        os.mkdir(outpath)


def trimargP(forward, reverse, outpath):
    fbase = os.path.splitext(os.path.basename(forward))[0]
    rbase = os.path.splitext(os.path.basename(reverse))[0]
    fv1 = os.path.isfile(os.path.join(outpath, fbase+'_val_1.fastq'))
    fv2 = os.path.isfile(os.path.join(outpath, fbase+'_val_2.fastq'))
    rv1 = os.path.isfile(os.path.join(outpath, rbase+'_val_1.fastq'))
    rv2 = os.path.isfile(os.path.join(outpath, rbase+'_val_2.fastq'))
    if ((fv1 or fv2) and (rv1 or rv2)):
        trims = False
    else:
        trims = ('/home/phac/Bryce/GenomeAssembler/bin/trim_galore/trim_galore',
                 '-o', outpath,
                 '--paired',
                 forward, reverse)
    return trims

def runtrimP(forward, reverse, outpath):
    trims = trimargP(forward, reverse, outpath)
    if trims:
        subprocess.call(trims)
    else:
        print('skipping', os.path.splitext(os.path.basename(forward))[0], 'due to file already existing')

def rename(outpath):
    outlist = glob.glob(outpath + '*.fq')
    for file in outlist:
        strain, extension = os.path.splitext(os.path.basename(file))
        os.rename(file, os.path.join(outpath, strain+'.fastq'))

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cores', default='multiprocessing.cpu_count()')
    parser.add_argument('-o', '--outpath', default='./cleanfastq/')
    parser.add_argument('path')
    return parser.parse_args()

def process(path, outpath, cores):
    fastqinput = getfastq(path)
    pathfinder(outpath)
    pool = multiprocessing.Pool(int(cores))
    for forward, reverse in zip(fastqinput[0::2], fastqinput[1::2]):
        pool.apply_async(runtrimP, args=(forward, reverse, outpath))
    pool.close()
    pool.join()
    rename(outpath)



def main():
    args = arguments()
    process(args.path, args.outpath, args.cores)

if __name__ == '__main__':
    main()
