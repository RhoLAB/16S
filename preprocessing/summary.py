import sys, argparse

def readTable(file_name, cut = 0, skip = 0) :
	tablef = open(file_name, 'r')

	for i in range(skip) :
		tablef.readline()

	table = {}
	for line in tablef.readlines() :
		cols = line.rstrip('\r\n').split('\t')

		sample = cols[0].split('/')[-1].split('.')[0]
		if cut != 0 : sample = sample[:-cut]
		table[sample] = cols[1]

	tablef.close()

	return table

# main

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("forward",  metavar="forward.cnt.txt",  help="forward reads count file")
arg_parser.add_argument("backward", metavar="backward.cnt.txt", help="backward reads count file")
arg_parser.add_argument("flash",    metavar="flash.cnt.txt",    help="merged reads count file")
arg_parser.add_argument("sickle",   metavar="sickle.cnt.txt",   help="trimmed reads count file")
arg_parser.add_argument("size",     metavar="forward.size.txt", help="reads size file")

args = arg_parser.parse_args()

summary = {}

forward  = readTable(args.forward, cut = 2)
backward = readTable(args.backward, cut = 2)
flash    = readTable(args.flash)
sickle   = readTable(args.sickle)
size     = readTable(args.size, cut = 2)

for sample in forward :
	print "\t".join([sample, forward[sample], backward[sample], flash[sample], sickle[sample], size[sample] + " * 2"])

