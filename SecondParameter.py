import csv

#here is where the code to properly identify the second parameter
#DISTANCE, will be found from probabilities based on training data
'''pseudocode
create gaussian based on the model data:
 

calculate probability:
for every tf:
	for every gene:
		=tf/gene pair take their line numbers and calculate distance
'''
GENEFILE_START_COLUMN = 4 	
GENEFILE_STOP_COLUMN = 5	#don't need this atm
GENEFILE_GENE_POS = 0
GENEFILE_TFVAL_POS = 1

TFFILE_TF_POS = 0
TFFILE_REG_GENES_POS = 1
BIN_SIZE = 500

def readPosTrainingDistances(genomeLength, pairFileName, genesFileName):
	#"returns a list of distances from all TFs to all the genes they regulate given the genome's length, and the names of both the TF/Promoter pair file and the all genes file"
	print("Starting to read in Training Distances")
	posTrainDist = []
	pairFile = csv.reader(open(pairFileName,'rb'))
	for tf in pairFile:				#looking through all TFs
		tfPos = 0
		tfName = tf[TFFILE_TF_POS]
		genesFile = csv.reader(open(genesFileName,'rb'))
		for gene in genesFile:
			if tfName in gene[GENEFILE_GENE_POS]:
				tfPos = int(gene[GENEFILE_START_COLUMN])
		regGenes = tf[TFFILE_REG_GENES_POS]
		regGenesList = []
		regGenesList = regGenes.split()
		posPairDist = []
		for regGene in xrange(len(regGenesList)):	#looping through all genes regulated
			regGeneName = regGenesList[regGene]
			genesFile1 = csv.reader(open(genesFileName,'rb'))
			for gene1 in genesFile1:					#looking for gene regulated by TF in gene file
				if regGeneName in gene1[GENEFILE_GENE_POS]:
					regGenePos=int(gene1[GENEFILE_START_COLUMN])
					posDist = []
					#difference1 = abs(regGenePos-tfPos)
					posDist.append(abs(regGenePos-tfPos))
					posDist.append(abs(posDist[0]-genomeLength))
					posTrainDist.append(min(posDist))


	#neg stuff start				
	enzymeMatrix = []
	negTrainDist = []
	genesFile2 = csv.reader(open(genesFileName,'rb'))
	for gene2 in genesFile2:
		if gene2[GENEFILE_TFVAL_POS] == 'F':
			enzymeMatrix.append(gene2)
	for outerEnzyme in xrange(len(enzymeMatrix)):
		currentRow = enzymeMatrix[outerEnzyme]
		outerPos = currentRow[GENEFILE_START_COLUMN]
		#print(outerPos)
		for innerEnzyme in range(outerEnzyme+1, len(enzymeMatrix)):
			negDist = []
			currentInnerRow = enzymeMatrix[innerEnzyme]
			innerPos = currentInnerRow[GENEFILE_START_COLUMN]
			negDist.append(abs(int(outerPos) - int(innerPos)))
			negDist.append(abs(negDist[0]-genomeLength))
			negTrainDist.append(min(negDist))
	#neg stuff end

	#print(enzymeMatrix)
	#print(negTrainDist)
	print("Normalizing positive training distances")
	posNormTrainDist = normTrainingDistances(genomeLength, posTrainDist)
	print("Normalizing negative training distances")
	negNormTrainDist = normTrainingDistances(genomeLength, negTrainDist)
	return (posNormTrainDist, negNormTrainDist)


def normTrainingDistances(genomeLength, trainingDistances):
	#"counts frequencies for distances in each bin given the length of the genome and the list of 
	#distances between the TFs and the promoters they regulate, then normalizes them into probabilities"
	numberOfBins = (genomeLength/(2*BIN_SIZE))+1
	#print numberOfBins
	binnedDistances = []
	for k in xrange(numberOfBins):
		binnedDistances.append(0)
	totalFreq=0
	for i in xrange(len(trainingDistances)):
		correctBin = (int(trainingDistances[i]/BIN_SIZE))
		#print binnedDistances[correctBin]
		#print correctBin
		binnedDistances[correctBin] += 1 
		totalFreq+=1
	print("Total frequency is: ", totalFreq)
	nonzero=0
	zero=0
	normDist=[]
	pseudocount = .05
	if totalFreq!=0:
		for x in xrange(len(binnedDistances)):
			normDist.append(((binnedDistances[x]+pseudocount)/(totalFreq+pseudocount*numberOfBins)))
			#if(binnedDistances[x]>0):
			#	nonzero+=1
			#else:
			#	zero+=1
	#print(normDist)
	#print("There is this many nonzero values before pseudocounts: ",nonzero)
	#print("zeroes: ",zero)
	return normDist

def secondParamMain(genomeLength, rootFileName):
	#"manages the running of all other functions in second Parameter File"
	genesFileName = str(rootFileName)+"Master.csv"
	pairFileName = str(rootFileName)+"TrainTFPairs.csv"
	testFileName = str(rootFileName)+"TestTFPairs.csv"
	posNegTup = readPosTrainingDistances(genomeLength, pairFileName, genesFileName) 
	outputCSV(posNegTup[0], posNegTup[1], rootFileName)

def testAccuracy(testFileName,genesFileName):
	print("Starting to read in testing Distances")
	posTestDist = []
	testFile = csv.reader(open(testFileName,'rb'))
	for tf in testFile:				#looking through all TFs
		tfPos = 0
		tfName = tf[TFFILE_TF_POS]
		genesFile = csv.reader(open(genesFileName,'rb'))
		for gene in genesFile:
			if tfName in gene[GENEFILE_GENE_POS]:
				tfPos = int(gene[GENEFILE_START_COLUMN])
		regGenes = tf[TFFILE_REG_GENES_POS]
		regGenesList = []
		regGenesList = regGenes.split()
		posPairDist = []
		for regGene in xrange(len(regGenesList)):	#looping through all genes regulated
			regGeneName = regGenesList[regGene]
			genesFile1 = csv.reader(open(genesFileName,'rb'))
			for gene1 in genesFile1:					#looking for gene regulated by TF in gene file
				if regGeneName in gene1[GENEFILE_GENE_POS]:
					regGenePos=int(gene1[GENEFILE_START_COLUMN])
					posDist = []
					#difference1 = abs(regGenePos-tfPos)
					posDist.append(abs(regGenePos-tfPos))
					posDist.append(abs(posDist[0]-genomeLength))
					posTestDist.append(min(posDist))
	trainDistCSV = csv.reader(open("Ecoli_MG1655secondParam.csv",'rb'))
	correctClassifyCount = 0
	totalClassifyCount = 0;
	for testTFDist in xrange(len(posTestDist)):
		testBin = int(posTestDist[testTFDist]/BIN_SIZE)
		#check trainDistCSV @ row testBin
		#totalClassifyCount+=1
		#if row[0]>row[1], correctClassifyCount+=1
		#return correctClassifyCount/totalClassifyCount


def outputCSV(posNormTrainDist, negNormTrainDist, rootFileName):
	#"creates a CSV file from the normalized data. requires the yes and no normalized probability lists"
	print("Starting to write to CSV!")
	secondParamCSV = csv.writer(open(""+rootFileName+"secondParam.csv", "wb"))
	#titleRow = ["Position (500 bp)","P(pair)","P(not pair)"]
	#secondParamCSV.writerow(titleRow)
	 #THERE IS NOTHING IN POSNORMTRAINDIST
	for x in xrange(len(posNormTrainDist)):
		row = []
		#row.append(x)
		row.append(posNormTrainDist[x])
		row.append(negNormTrainDist[x])
		secondParamCSV.writerow(row)


secondParamMain(4639675, "Ecoli_MG1655")