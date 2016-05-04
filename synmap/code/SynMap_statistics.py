#!/data/apps/python/3.2.1/bin/python
import re, sys

merged_file = sys.argv[1]
print("SynMap Merged DAGChainer Results file is ", merged_file)

## initiate sets to hold the organism 1 and organism 2 scaffold names
scafSetOrg1 = set()
scafSetOrg2 = set()

##-----------------------
## Get scaffolds from file
with open(merged_file) as f:
	for line in f:
		if '||' in line:
			line = line.rstrip('\n')
			wordList = line.split()
			org1scaf = wordList[0]
			scafSetOrg1.add(org1scaf)
			org2scaf = wordList[4]
			scafSetOrg2.add(org2scaf)
			#print(org1scaf + ' ' + org2scaf)
f.close

numOrg1scaf = len(scafSetOrg1)
numOrg2scaf = len(scafSetOrg2)

print('Organism 1 has ' + str(numOrg1scaf) + ' scaffolds placed in at least one syntenic block')
print('Organism 2 has ' + str(numOrg2scaf) + ' scaffolds placed in at least one syntenic block')