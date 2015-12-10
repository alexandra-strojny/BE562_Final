import csv

def validGene(gene, fileName):
	myFile = csv.reader(open(fileName+'Master.csv', 'rb'))
	for row in myFile:
		if gene in row[0]:
			return True
	return False


def readCSVFile(fileName):
	myFile = csv.reader(open(fileName+'OldTFPairs.csv', 'rb'))
	tfNum = 0
	for row in myFile:
		tfNum+=1
	TFPairs = []
	for i in xrange(tfNum):
		TFPairs+=[[0]*2]
	myFile2 = csv.reader(open(fileName+'OldTFPairs.csv', 'rb'))
	geneCount = 0
	for row in myFile2:
		tfString = row[0]
		slashCount = 0
		tfPiece = ""
		index = 0
		for c in tfString:
			if (slashCount % 2 == 0 and c == '/'):
				if (tfString[index+1] == '/'):
					slashCount += 1
					tfPiece += " "
			elif c == '/':
				slashCount += 1
			elif c == ' ':
				continue
			else:
				tfPiece += c
			index+=1

		geneString = row[1]
		slashCount = 0
		genePiece = ""
		geneVector = []
		for c in geneString:
			if (slashCount % 2 == 0 and c == '/'):
				slashCount += 1
				geneVector.append(genePiece)
				genePiece = ""
			elif c == '/':
				slashCount += 1
			elif c == ' ':
				continue
			else:
				genePiece += c
		geneVector.append(genePiece)
		index = 0
		finalgeneString = ""
		removeG = []
		for gene in geneVector:
			geneLower = gene[0].lower() + gene[1:]
			if 'sup' in gene or 'sub' in gene or 'SUP' in gene or 'SUB' in gene:
				removeG.append(gene)
			elif validGene(gene[:5]+ " ", fileName) or validGene(geneLower[:5]+ " ", fileName):
				finalgeneString += gene[:5] + " "
			elif validGene(gene[:4] + " ", fileName) or validGene(geneLower[:4] + " ", fileName):
				finalgeneString += gene[:4] + " "
			elif validGene(gene[:3] + " ", fileName) or validGene(geneLower[:3] + " ", fileName):
				finalgeneString += gene[:3] + " "
			else:
				removeG.append(gene)

		for element in removeG:
			geneVector.remove(element)
		newGeneVector = []
		for i in geneVector:
			if i not in newGeneVector:
				newGeneVector.append(i)

		if(len(newGeneVector) > 0):
			TFPairs[geneCount][0] = tfPiece
			TFPairs[geneCount][1] = finalgeneString
			geneCount += 1
	return TFPairs
			
def createTFPairsFile(fileName):
	TFPairs = readCSVFile(fileName)
	cFile = csv.writer(open(fileName+"TFPairs.csv", 'wb'))
	for i in xrange(len(TFPairs)):
		if TFPairs[i][0] != 0 and TFPairs[i][1] != 0:
			cFile.writerow(TFPairs[i])

