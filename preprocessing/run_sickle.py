import sys, os, glob, argparse
sys.path.append("/home/hjgwak/scripts/")
from common import *

# main

arg_parser = argparse.ArgumentParser()

sickle_mode = arg_parser.add_mutually_exclusive_group(required=True)
sickle_mode.add_argument("-pe", action="store_const", const="pe", dest="mode", help="select mode of sickle, paired-end")
sickle_mode.add_argument("-se", action="store_const", const="se", dest="mode", help="select mode of sickle, single-end")
arg_parser.add_argument("-q", metavar="#", dest="quality", default="20",  help="sequence quality cutoff, default 20")
arg_parser.add_argument("-l", metavar="#", dest="length",  default="150", help="sequence length cutoff, default 150")
input_mode = arg_parser.add_mutually_exclusive_group(required=True)
input_mode.add_argument("-list",   metavar="FILE", dest="i_list", help="input file list")
input_mode.add_argument("-inDir",  metavar="DIR",  dest="i_dir", help="input file directory, input files will be detected automatically")
arg_parser.add_argument("-outDir", metavar="DIR",  dest="o_dir", required=True, help="output directory, required")

args = arg_parser.parse_args()

ilist = []
if args.i_list != None :
	f = open(args.i_list, 'r')
	ilist = [line.rstrip('\r\n') for line in f.readlines()]
	f.close()

if args.mode == "pe" :
	if len(ilist) == 0 :
		forwards  = glob.glob(args.i_dir + "*_1.fastq")
		backwards = glob.glob(args.i_dir + "*_2.fastq")
	else :
		forwards  = []
		backwards = []
		for item in ilist :
			if item[-7] == "1" :
				forwards.append(item)
			elif item[-7] == "2" :
				backwards.append(item)
			else :
				print >> sys.stderr, "input list is incorrect!"
				exit(-1)

	for fastq in forwards :
		backward = fastq[:-8] + "_2.fastq"
		if backward in backwards :
			backwards.remove(backward)

			o_forward  = args.o_dir + fastq.split('/')[-1][:-8] + "_trimmed_1.fastq"
			o_backward = args.o_dir + backward.split('/')[-1][:-8] + "_trimmed_2.fastq"
			single = fastq[:-8] + "_single.fastq"
			cmd = "/home/hjgwak/programs/sickle-master/sickle pe -f %s -r %s -o %s -p %s -t sanger -s %s -q %s -l %s" % (fastq, backward, o_forward, o_backward, single, args.quality, args.length)
			print cmd
			os.system(cmd)
		else :
			print >> sys.stderr, backward + " is missing."

	for fastq in backwards :
		forwards = fastq[:-8] + "_1.fastq"
		print >> sys.stderr, forward + " is missing."

elif args.mode == "se" :
	if len(ilist) == 0 :
		fastq_list = glob.glob(arg.i_dir + "*.fastq")
	else  :
		fastq_list = ilist

	for fastq in fastq_list :
		o_fastq = args.o_dir + fastq.split('/')[-1]
		cmd = "/home/hjgwak/programs/sickle-master/sickle se -f %s -t sanger -o %s -q %s -l %s" % (fastq, o_fastq, args.quality, args.length)
		print cmd
		os.system(cmd)
else :
	print "mode of sickle should be given!"
	exit(-1)
