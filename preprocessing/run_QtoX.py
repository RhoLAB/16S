import sys, os, glob

def makeDirForm(path) :
	if path[-1] != "/" :
		path += '/'
	return path

# main

if len(sys.argv) < 5 :
	print "python run_QtoX.py [-Q #] [-n] [-suffix str] [-list str] [-inDir str] [-outDir str]"
	print "       -Q\t:\toffset of Phred quality score (default 33)"
	print "       -n\t:\tremaining sequences which involve N"
	print "       -suffix\t:\tsuffix of input files, default .fastq"
	print "       -list\t:\tTo give specific input list (default auto detect)"
	print "       -inDir\t:\tThe directory which involve input files, required"
	print "       -outDir\t:\tOutput directory, required"
	exit(-1)

Q = "33"
if "-Q" in sys.argv :
	Q = sys.argv[sys.argv.index("-Q") + 1]
n = ""
if "-n" in sys.argv :
	n = "-n"
suffix = ".fastq"
if "-suffix" in sys.argv :
	suffix = sys.argv[sys.argv.index("-suffix") + 1]

ilist = []
if "-list" in sys.argv :
	f = open(sys.argv[sys.argv.index("-list") + 1], 'r')
	ilist = [line.rstrip('\r\n') for line in f.readlines()]
	f.close()
elif "-inDir" in sys.argv :
	input_dir = makeDirForm(sys.argv[sys.argv.index("-inDir") + 1])
	ilist = glob.glob(input_dir + "*" + suffix)
else :
	print "Either input list or input directory should be given"
	exit(-1)

output_dir = makeDirForm(sys.argv[sys.argv.index("-outDir") + 1])
for fastq in ilist :
	file_name = fastq.split('/')[-1].replace(suffix, ".fasta")
	cmd = "/home/hjgwak/programs/fastx/fastq_to_fasta -i %s -o %s -Q %s %s" % (fastq, output_dir + file_name, Q, n)
	print cmd
	os.system(cmd)
