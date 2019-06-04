# -*- coding: utf-8 -*-

"""
1) Edit the "pathtolocal", which should be the same as in LSTrAP_Lite_download.py
2) Copy and paste the desired SRA Run ID into the file "selected_runs" and save it.
3) Run the script.
"""
#PATHS
pathtolocal = '/path/to/local'

output = open(pathtolocal + '/matrix_selected.tsv', "w+") #new matrix file of the selected runs
run_id = open(pathtolocal + '/selected_runs.txt', "r") #ID of the selected runs
full_matrix = open(pathtolocal + '/matrix_raw.tsv', "r") #full matrix file generated from the download script
header_raw = full_matrix.readline()
header = header_raw.rstrip("\n").split("\t")

#Extracts the index of the selected run IDs from the header
run_index = [header.index(x.rstrip("\n")) for x in run_id.readlines()]

#Formats the header of the matrix file and write it to output file
output.write("gene")
for i in run_index:
	output.write("\t" + header[i])
output.write("\n")

#Extract the selected run index from the raw matrix file and writes it to the new matrix file (output)
for a in full_matrix: #for line in raw matrix file, write the gene to output file
	line = a.split("\t")
	output.write(line[0])
	for b in run_index: #writes the corresponding tpm value of the selected run to the new matrix file (output)
		output.write("\t" + line[b].rstrip("\n")) #access the selected run base on the index of the run which is stored in <run_index>
	output.write("\n")

output.close()
run_id.close()
full_matrix.close()