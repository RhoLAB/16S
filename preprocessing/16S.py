import sys, argparse, os

def makeDirForm(path) :
	if path[-1] != '/' :
		path += '/'
	return path

# main

arg_parser = argparse.ArgumentParser(description=\
		"""QC pipeline for 16S amplicon sequence data
Output:
		[Prefix]/
		[Prefix]/data/            : soft link files for raw input data
		[Prefix]/flash/           : merged reads
		[Prefix]/sickle/          : quality trimmed merged reads
		[Prefix]/fasta/           : converted fasta from sickle outputs
		[Prefix]/forward.size.txt : file size of forward reads
		[Prefix]/forward.cnt.txt  : the number of forward reads
		[Prefix]/backward.cnt.txt : the number of backward reads
		[Prefix]/flash.cnt.txt    : the number of merged reads
		[Prefix]/flash.log        : log file of FLASH
		[Prefix]/flash.err        : error file of FLASH
		[Prefix]/sickle.cnt.txt   : the number of quality trimmed reads
		[Prefix]/sickle.log       : log file of sickle
		[Prefix]/sickle.err       : error file of sickle
		[Prefix]/q2a.log          : log file of fastq_to_fasta
		[Prefix]/q2a.err          : error file of fastq_to_fasta
		[Prefix]/summary.txt      : total summary of QC
		""", formatter_class=argparse.RawTextHelpFormatter)

arg_parser.add_argument("-q", dest="quiet", action="store_true", default=False, help="do not print any infomation in stdout. default: False")
arg_parser.add_argument("-t", metavar="#", dest="threads", default=1, type=int, help="number of threads for pipeline")
v_region = arg_parser.add_mutually_exclusive_group(required=True)
v_region.add_argument("-V1V2",  action="store_const", dest="length", const=260, help="hypervariable region of input is V1V2, set length cutoff for sickle 260")
v_region.add_argument("-V3V4",  action="store_const", dest="length", const=380, help="hypervariable region of input is V3V4, set length cutoff for sickle 380")
arg_parser.add_argument("-p", metavar="prefix", dest="prefix", required=True, help="prefix of temporary outputs, required")
arg_parser.add_argument("inDir", metavar="inDir", help="raw data directory")

args = arg_parser.parse_args()

args.inDir = makeDirForm(args.inDir)

counter = "/home/hjgwak/scripts/fastq/count.py"
flash   = "/home/hjgwak/scripts/preprocessing/run_FLASH.py"
sickle  = "/home/hjgwak/scripts/preprocessing/run_sickle.py"
q2x     = "/home/hjgwak/scripts/preprocessing/run_QtoX.py"
summary = "/home/hjgwak/scripts/preprocessing/summary.py"

mkdir = "mkdir -p" if args.quiet else "mkdir -pv "

os.system(mkdir + "%s/"        % args.prefix)
os.system(mkdir + "%s/data/"   % args.prefix)
os.system(mkdir + "%s/flash/"  % args.prefix)
os.system(mkdir + "%s/sickle/" % args.prefix)
os.system(mkdir + "%s/fasta/"  % args.prefix)

os.system("ln -s %s/* %s/data/" % (args.inDir, args.prefix))
os.chdir(args.prefix)

os.system("ls -alhv %s*_1* | gawk '{print $9\"\\t\"$5}' > forward.size.txt" % args.inDir)
os.system("python %s data/*_1* > forward.cnt.txt &"  % counter)
os.system("python %s data/*_2* > backward.cnt.txt &" % counter)

os.system("python %s -t %d -inDir data/ -outDir flash/ 1> flash.log 2> flash.err" % (flash, args.threads))
os.system("ls -alhv flash/*extendedFrags* | gawk '{print $9}' > flash.list.txt")
os.system("python %s flash/*extendedFrags* > flash.cnt.txt &" % counter)

os.system("python %s -se -l %d -list flash.list.txt -outDir sickle/ 1> sickle.log 2> sickle.err" % (sickle, args.length))
os.system("python %s sickle/* > sickle.cnt.txt &" % counter)

os.system("python %s -suffix .extendedFrags.fastq -inDir sickle/ -outDir fasta/ 1> q2a.log 2> q2a.err" % q2x)

os.system("python %s forward.cnt.txt backward.cnt.txt flash.cnt.txt sickle.cnt.txt forward.size.txt > summary.txt" % summary)
