#!/data/apps/python/3.2.1/bin/python
import re, sys

##-----------------------------------
## Authored: Meg Staton
## Date: 5/4/16
## Description: Parses DAGChainer output, generating statistics
##	DAGChainer file should be provided as first command line argument
##-----------------------------------


##-----------------------
## Functions
##-----------------------


##-----------------------
## processBlock 
## Input: a list of lines from DAGChainer that define a syntenic block
## Output: the name of each scaffold and the overall start stop coords
##         for each
def processBlock(blockLineList):
	#print('Received ' + str(len(blockLineList)) + ' lines')

	org1Start = -1
	org1End = -1

	org2Start = -1
	org2End = -1

	for line in blockLineList:
		wordList = line.split()

		# process information for organism 1
		org1desc = wordList[1]
		descList = org1desc.split('||')

		org1scaf = descList[0]
		tmp_start = int(descList[1])
		tmp_end = int(descList[2])

		if org1Start < 0:
			org1Start = tmp_start
		elif tmp_start < org1Start:
			org1Start = tmp_start

		if org1End < 0:
			org1End = tmp_end
		elif tmp_end > org1End:
			org1End = tmp_end

		# process information for organism 2
		org2desc = wordList[5]
		descList = org2desc.split('||')

		org2scaf = descList[0]
		tmp_start = int(descList[1])
		tmp_end = int(descList[2])

		if org2Start < 0:
			org2Start = tmp_start
		elif tmp_start < org2Start:
			org2Start = tmp_start

		if org2End < 0:
			org2End = tmp_end
		elif tmp_end > org2End:
			org2End = tmp_end

	#print('org1 scaffold: ' + org1scaf)
	#print('start: ' + str(org1Start))
	#print('end: ' + str(org1End))
	#print('---')
	#print('org2 scaffold: ' + org2scaf)
	#print('start: ' + str(org2Start))
	#print('end: ' + str(org2End))
	#print('---')

	return org1scaf, org1Start, org1End, org2scaf, org2Start, org2End

##-----------------------
## Body
##-----------------------
merged_file = sys.argv[1]
print("SynMap Merged DAGChainer Results file is ", merged_file)


### initiate sets to hold the organism 1 and organism 2 scaffold names
scafSetOrg1 = set()
scafSetOrg2 = set()

org1TotalDist = 0
org2TotalDist = 0

##-----------------------
## Iterate file and pull out each syntenic block as a list of lines
blockLineList = []
with open(merged_file) as f:
	for line in f:
		if line.startswith('#'):
			if len(blockLineList) > 0:
				org1scaf, org1Start, org1End, org2scaf, org2Start, org2End = processBlock(blockLineList)
				scafSetOrg1.add(org1scaf)
				scafSetOrg2.add(org2scaf)
				org1TotalDist = org1TotalDist + (org1End - org1Start)
				org2TotalDist = org2TotalDist + (org2End - org2Start)
			del blockLineList[:]
		else:
			blockLineList.append(line)

	#process last block from file
	org1scaf, org1Start, org1End, org2scaf, org2Start, org2End = processBlock(blockLineList)
	scafSetOrg1.add(org1scaf)
	scafSetOrg2.add(org2scaf)
	org1TotalDist = org1TotalDist + (org1End - org1Start)
	org2TotalDist = org2TotalDist + (org2End - org2Start)

f.close

##-----------------------
## Print results
numOrg1scaf = len(scafSetOrg1)
numOrg2scaf = len(scafSetOrg2)

print('Organism 1 has ' + str(numOrg1scaf) + ' scaffolds placed in at least one syntenic block')
print('Total syntenic block length is ' + str(org1TotalDist))
print('Organism 2 has ' + str(numOrg2scaf) + ' scaffolds placed in at least one syntenic block')
print('Total syntenic block length is ' + str(org2TotalDist))
