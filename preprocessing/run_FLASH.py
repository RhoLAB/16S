import sys, glob, os, argparse

def makeDirForm(path) :
	if path[-1] != "/" :
		path += "/"
	return path

# main

arg_parser = argparse.ArgumentParser(version="1.0", \
		description="Run FLASH for raw MiSeq fastq file(s) automatically")

arg_parser.add_argument("-M",      metavar="#",   action="store", dest="M", default=300, type=int, help="Maximum overlap length, default 300")
arg_parser.add_argument("-m",      metavar="#",   action="store", dest="m", default=20, type=int,  help="Minimum overlap length, default 20")
arg_parser.add_argument("-p",      metavar="#",   action="store", dest="p", default=33, type=int,  help="Phred quality starting value, default 33")
arg_parser.add_argument("-t",      metavar="#",   action="store", dest="t", default=1, type=int,   help="The number of threads, default 1")
arg_parser.add_argument("-inDir",  metavar="DIR", action="store", dest="inDir",  help="input directory where involves input files, required", required=True)
arg_parser.add_argument("-outDir", metavar="DIR", action="store", dest="outDir", help="output directoty, required", required=True)

args = arg_parser.parse_args()

args.inDir  = makeDirForm(args.inDir)
args.outDir = makeDirForm(args.outDir)

forwards  = glob.glob(args.inDir + "*_1.fastq")
backwards = glob.glob(args.inDir + "*_2.fastq")

if len(forwards) != len(backwards) :
	print "paried reads does not match! (please check the inputs)"
	exit(-1)

for read in forwards :
	in_prefix = read[:-8]
	if in_prefix + "_2.fastq" not in backwards :
		print "paired reads does not match! (please check the inputs)"
		print in_prefix + "_2.fastq file is missing"
	else :
		prefix = in_prefix.split('/')[-1]
		cmd = "/home/hjgwak/programs/FLASH-1.2.11/flash -M %d -m %d -p %d -o %s -d %s -t %d -q %s %s" % (args.M, args.m, args.p, prefix, args.outDir, args.t, read, in_prefix + "_2.fastq")
		os.system(cmd)

		backwards.remove(in_prefix + "_2.fastq")

if len(backwards) != 0 :
	for read in backwards :
		in_prefix = read[:-8]
		print "paired reads does not match! (please check the inputs)"
		print in_prefix + "_1.fastq file is missing"
