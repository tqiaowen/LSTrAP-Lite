# -*- coding: utf-8 -*-

from scipy.stats import pearsonr
import numpy as np

#Edit the "pathtolocal", which should be the same as in LSTrAP_Lite_download.py and LSTrAP_Lite_TrimMatrix.py

#PATHS
pathtolocal = '/path/to/local'
matrix_file = open(pathtolocal + '/matrix_selected.tsv', "r")

"""
pcc_cal(geneID, cutoff = 0.7, n_size = 51)
   Function to calculate the pcc value of query gene against all other genes in the matrix.
   Input: geneID (query gene)
   Arguments cutoff (cutoff for PCC value to be considered); n_size (size of immediate neighbourhood)
   
   The functions takes in a matrix and calculates the PCC value of the query gene against all other genes. 
   Additional parameters such as PCC cutoff value and neighbourhood size can be specified. 
   
   Output: None
   
   Files generated: 1) List of genes pairs and their PCC values sorted according to the PCC value in descending order.
					2) PCC network of the gene pairs from the file described above
"""

def pcc_cal(geneID, cutoff = 0.7, n_size = 51):
	neighbourhood_file = open(pathtolocal  +'/' + geneID.replace('|','_') + '_nbh.txt', 'w+') #creates PCC output file. Replaces possible illegal characters
	dict_val = {} #container to store gene : [tpm values]
	gene_list = [] #records the genes in the matrix
	matrix_file.readline() #skips header of matrix file
	for line in matrix_file: #converts matrix to dictionary where key refers to gene and values refer to the tpm values across the various samples
		content = line.rstrip('\n').split('\t')
		key = content[0]
		values = np.array(content[1:]).astype(np.float)
		gene_list.append(key)
		if key in dict_val:
			dict_val[key].append(values)
		else:
			dict_val[key]=values
	if '' in dict_val:
		dict_val.pop('')
	
	#Calculates PCC values all possible combinations of gene pairs and writes the gene pairs to output_file
	gene_val = [] #container for gene pairs with PCC higher than cutoff defined (default = 0.7)
	counter = 0
	#Calculates PCC value for each gene against query gene
	for item in dict_val:
		pcc_val, p_value = pearsonr(dict_val.get(geneID), dict_val.get(item))
		counter+=1
		if counter % 10000 == 0:
			print('Calculated PCC for ' + str(counter) + ' out of ' + str(len(gene_list)) + " genes")
		if pcc_val >= cutoff:
			gene_val.append([geneID, item, pcc_val])
	sorted_gene_val = sorted(gene_val, key = lambda x: x[2], reverse = True) #sorts genes according to the pcc value
	#If there are more gene pairs than the defined neighbourhood size cutoff, only write the ones included in the cutoff. Else, write everything in sorted_gene_val
	if len(sorted_gene_val) >n_size: 
		for i in range(n_size):
			neighbourhood_file.write(sorted_gene_val[i][0] + "\t" + sorted_gene_val[i][1] + "\t" + str(sorted_gene_val[i][2]) + "\n")
	else:
		for z in sorted_gene_val:
			neighbourhood_file.write(z[0] + "\t" + z[1] + "\t" + str(z[2]) + "\n")
	neighbourhood_file.close()
	print("PCC neighbourhood calculated for: " + geneID + "\n")
	print("Neighbourhood file generated at: " + pathtolocal  +'/' + geneID.replace('|','_') + '_nbh.txt\n')
	
	"""Construction of PCC network"""
	neighbourhood_file = open(pathtolocal  +'/' + geneID.replace('|','_') + '_nbh.txt', 'r') #creates PCC output file. Replaces possible illegal characters
	network_file = open(pathtolocal  +'/' + geneID.replace('|','_') + '_nw.txt', 'w+') #creates PCC network file. Replaces possible illegal characters
	nw_gene_list = [x.split("\t")[1] for x in neighbourhood_file]
	network_size = 0
	for i in range(len(nw_gene_list)):
		network_size+=i
	counter2 = 0
	ngene_val = []
	"""Calculates PCC values for al possible combinations of gene pairs and writes the gene pairs that have PCC val ?= 0.7 to network_file"""
	for gene in range(len(nw_gene_list)):
		for gene2 in range(gene):
			npcc_val, np_value = pearsonr(dict_val.get(nw_gene_list[gene]), dict_val.get(nw_gene_list[gene2]))
			ngene_val.append([nw_gene_list[gene], nw_gene_list[gene2], npcc_val])
			counter2+=1
			if counter2 % 1000 == 0:
				print('Calculated PCC for ' + str(counter2) + ' out of ' + str(network_size) + ' gene pairs')
	nsorted_gene_val = sorted(ngene_val, key = lambda x: x[2], reverse = True) #sorts genes according to the pcc value
	for i in nsorted_gene_val:
		network_file.write(i[0] + "\t" + i[1] + "\t" + str(i[2]) + "\n")
	neighbourhood_file.close()
	network_file.close()
	print("PCC network calculated for all gene pairs\n")
	print("Network file generated at: " + pathtolocal  +'/' + geneID.replace('|','_') + '_nw.txt')

user = input("Enter gene of interest, PCC cutoff (default = 0.7) [optional] and network size (default = 51) [optional]. eg. AT1G01720,0.5,80: ")
print("\n")

#While the user gives an empty input, keeps asking for the user to give a valid input
while user == '':
	user = input("Enter gene of interest and PCC cutoff (default = 0.7) eg. AT1G01720,0.5,80: ")
#Checks if user specified arguments. If the user specified arguments, check for the number of arguments user specified to split the input accordingly. 
#If no arguments are specified, takes the query gene and run the calculation
if ',' in user:
	if len(user.split(',')) == 2:
		x = user.split(",")[0]
		y = float(user.strip('\n').split(",")[1])
		pcc_cal(x,y)
	elif len(user.split(',')) == 3:
		x = user.split(",")[0]
		y = float(user.strip('\n').split(",")[1])
		z = int(user.strip('\n').split(",")[2])
		pcc_cal(x,y,z)
else:
	pcc_cal(user.strip('\n'))

matrix_file.close()

