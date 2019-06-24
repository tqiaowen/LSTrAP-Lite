import os
import time
import ast
import gzip
from scipy.stats import sem

##############################################################################
#                               USER GUIDE                                   #
##############################################################################

#1. Edit the paths under 'Paths to edit'
#2. Run the script.

"""
Notes: 
1) Download_list should be in this format: "run_ID\tlibrary_layout". Please refer to sample data for an example
2) Please refer to https://github.com/tqiaowen/LSTrAP-Lite/docs/tutorial.md for more information
"""

##############################################################################
#                              Paths to edit                                 #
##############################################################################
pathtolocal = '/path/to/local'
download_list = open(pathtolocal+'/sra_runID.txt', 'r').readlines()
kallisto_fasta = pathtolocal + "/CDS_file"
pathtoaspera = 'exagear debian-8 -- /home/rock64/.aspera/connect/bin/ascp'
aspera_ssh_key = '/home/rock64/.aspera/connect/etc/asperaweb_id_dsa.openssh'
pathtokallisto = '/home/rock64/bin/kallisto'

##############################################################################
#                               Other paths                                  #
##############################################################################
curFile = pathtolocal + "/fastq/" 
kallisto_index = pathtolocal + '/index_file'
path_to_output = pathtolocal + '/matrix_raw.tsv'
output_file = open(path_to_output, 'w+') #full matrix file
map_stats = open(pathtolocal + '/mapping_stats.tsv', 'w+') #mapping statistics output
id_file = open(pathtolocal + '/selected_runs.txt', 'w+')
id_file.close()

#creates directories if they do not already exist
if not os.path.exists(curFile):
	os.makedirs(curFile)
if not os.path.exists(pathtolocal + "/logs/"):
	os.makedirs(pathtolocal + "/logs/")

#opens and format log files if necessary
aborted_files = open(pathtolocal + '/logs/error_log.txt', 'a+')
if os.path.getsize(pathtolocal + '/logs/error_log.txt') == 0:
	aborted_files.write('Accession' + '\t' + 'Error message\n')
aborted_files.close()
logfile_path = open(pathtolocal + '/logs/logfile.txt', 'a+')
if os.path.getsize(pathtolocal + '/logs/logfile.txt') == 0:
	logfile_path.write('Run ID\tSize(Mb)\tAvg read length\tstd err\tDownload time(s)\tParse time(s)\tKallisto time(s)\n')
logfile_path.close()

#creates kallisto index
os.system("kallisto index -i " + kallisto_index + " " + kallisto_fasta)
print("Kallisto index created")

"""
aspera_launch(item_name, lib_lay, download_path)
   Attempts download of run through aspera based on 'LIBRARY_LAYOUT' as described in SRA run table.
   Returns ascp download time
"""
def aspera_launch(item_name, lib_lay, download_path):	
	ascp_time = 'N/A'
	if lib_lay == "PAIRED":
		start = time.time()
		os.system(pathtoaspera+ " -QT -l 300m -P33001 -i " + aspera_ssh_key + " era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/" + download_path + "/" + item_name+ "/" + item_name + "_1.fastq.gz " + pathtolocal + "/fastq")
		file_name = item_name + '_1.fastq.gz'
		if file_name in os.listdir(curFile):
			stop = time.time()
			ascp_time = round(stop-start, 2)
           
		else:
			os.system(pathtoaspera+ " -QT -l 300m -P33001 -i " + aspera_ssh_key + " era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/" + download_path + "/" + item_name+ "/" + item_name + ".fastq.gz " + pathtolocal + "/fastq")
			file_name2 = item_name + '.fastq.gz'
			if file_name2 in os.listdir(curFile):
				stop = time.time()
				ascp_time = round(stop-start, 2)
			else:
				raise Exception(accession + ': Aspera download for PAIRED library failed')
				aborted_files.write(accession + '\tAspera download for PAIRED library failed\n')
    
	elif lib_lay == "SINGLE":
		start = time.time()
		os.system(pathtoaspera+ " -QT -l 300m -P33001 -i " + aspera_ssh_key + " era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/" + download_path + "/" + item_name+ "/" + item_name + ".fastq.gz " + pathtolocal + "/fastq")
		file_name = item_name + '.fastq.gz'
		if file_name in os.listdir(curFile):
			stop = time.time()
			ascp_time = round(stop-start, 2)

		else:
			raise Exception(accession + '.fastq.gz not downloaded.')
			aborted_files.write(accession + '_1.fastq.gz not downloaded.')

	return (ascp_time)

#Downloads and maps the RNA-seq data to the CDS using kallisto for each SRA RunID provided in the download_list.
for item in download_list:
	run_id = 'N/A'
	size = 'N/A'
	avg_read = 'N/A'
	ascp_time = 'N/A'
	kal_time = 'N/A'
	processed_reads = 'N/A'
	mapped_reads = 'N/A'
	gzip_time = 'N/A'
	std_err = 'N/A'
	percent_mapped = 'N/A'
	
	accession = item.rstrip().split('\t')[0]
	if "kal_" + accession not in os.listdir(curFile):
		print(item.rstrip('\n'))
		aborted_files = open(pathtolocal + '/logs/error_log.txt', 'a')
		logfile_path = open(pathtolocal + '/logs/logfile.txt', 'a')
		lib_layout = item.rstrip().split('\t')[1].upper()
		run_id = accession
		first_dir = accession[0:6]
		second_dir = ''
		path = ''
		try:
			if len(accession) == 9:
				path = first_dir
				result = aspera_launch(accession, lib_layout, path)
				ascp_time = result
		
			elif len(accession) == 10:
				second_dir = '00' + accession[-1]
				path = first_dir + "/" + second_dir
				result = aspera_launch(accession, lib_layout, path)
				ascp_time = result
		
			elif len(accession) == 11:
				second_dir = '0' + accession[9:]
				path = first_dir + "/" + second_dir
				result = aspera_launch(accession, lib_layout, path)
				ascp_time = result
		
			elif len(accession) == 12:
				second_dir = accession[8:]
				path = first_dir + "/" + second_dir
				result = aspera_launch(accession, lib_layout, path)
				ascp_time = result
		
			else:
				print("Aspera download failed.")
				aborted_files.write(accession + '\t' + 'Aspera download failed.\n')
		
			#Parsing for average read length and Kallisto
			for file in os.listdir(curFile):
				if "fastq.gz" in file:
					print("processing: " + file)
		
					size_bytes = os.path.getsize(curFile+file)
					size = size_bytes//(1024*1024)
					
					fastq_file = gzip.open(curFile+file, 'rb')
					gzip_start = time.time()
					read_count = 0
					len_list = []
					total_len = 0
					for i in range(100):
						readname = fastq_file.readline().rstrip().decode("utf-8")
						sequence = fastq_file.readline().rstrip().decode("utf-8")
						strand_info = fastq_file.readline().rstrip().decode("utf-8")
						quality = fastq_file.readline().rstrip().decode("utf-8")
						read_count += 1
						len_list.append(len(sequence))
					total_len = sum(len_list)
					avg_read = total_len / read_count
					std_err = sem(len_list)
					std_err = round(std_err, 2)
					gzip_stop = time.time()
					gzip_time = round(gzip_stop - gzip_start, 2)
					fastq_file.close()
					
					#kallisto against index
					start_kal = time.time()      
					os.system(pathtokallisto + " quant -i " + kallisto_index + " -t 4 -o " + curFile + "kal_" +  accession + " --single -l 200 -s 20 " + curFile + file)
					stop_kal = time.time()
					kal_time = round(stop_kal - start_kal, 2)
					#print("Kallisto for %s took %s seconds." %(file, stop_kal-start_kal))
		
					try:
						os.remove(curFile + file)
						print(accession + ": Kallisto is completed.\n")
					except:
						pass
						print("Error removing files.\n")
						aborted_files.write (accession + "\tError removing files.\n")
					
					logfile_path.write(run_id+'\t'+ str(size) +'\t'+str(avg_read)+'\t'+str(std_err)+'\t'+str(ascp_time)+'\t'+str(gzip_time)+'\t'+str(kal_time)+'\n') #Percentage of genes mapped\tTotal exon length

		except:
			pass
			print("Error processing " + accession + "\n")	
			aborted_files.write(accession + "\tError processing file\n")
		aborted_files.close()
		logfile_path.close()
	
#Creates expression matrix and mapping statistics log
dicto = {} #stores gene and corresponding tpm values from the experiment 
dict_log = {} #stores average read length from logfile.txt
log_read = open(pathtolocal + '/logs/logfile.txt', 'r')
log_read.readline()
for line in log_read: #extract average read length information in logfile and store in dict_log
	dict_log[line.split('\t')[0]] = line.strip('\n').split('\t')[2]
output_header = 'gene\t'
output_content = ''
map_stats.write('Run ID\tProcessed reads\tMapped reads\t% reads mapped\t% genes mapped\tGene count\tTotal exon length (bp)\tEstimated sequencing depth\n') #formats mapping_stats.tsv
for file in os.listdir(curFile): #go through /fastq/ directory for the kallisto outputs to create mapping_stats.tsv and matrix_raw.tsv
	gene_count = 0 #container for number of genes that  had non-zero tpm values
	gene_len = 0 #container for total exon length
	name = file.split("_")[1] #ID of run
	processed_reads = '' #total reads in experiment
	mapped_reads = 0 #total reads mapped
	percent_mapped = '' #percentage of reads mapped
	CDS_count = 0 #number of genes in genome
	for file2 in os.listdir(curFile+file): #looks through the files in the kallisto directory
		#extracting information from kallisto output file for mapping_stats.tsv
		if 'run_info.json' in file2: 
			print('In directory ' + file)
			kallisto_json = ast.literal_eval(open(curFile+file+'/'+file2, 'r').read())
			processed_reads = str(kallisto_json["n_processed"])
			mapped_reads = kallisto_json["n_pseudoaligned"]
			percent_mapped = str(round((kallisto_json["n_pseudoaligned"] / kallisto_json["n_processed"])*100, 2))
			CDS_count =  kallisto_json["n_targets"]
		#appends corresponding tpm values to genes into the dictionary <dicto>
		elif 'abundance.tsv' in file2:
			output_header += name + '\t'
			content = open(curFile+file+'/'+file2, 'r')
			content.readline()
			for item in content:
				values = item.rstrip().split('\t')
				item = values[0]
				tpm = values[-1]
				gene_len += int(values[1])
				if tpm != '0':
					gene_count += 1
				if item in dicto:
					dicto[item].append(tpm)
				else:
					dicto[item] = [tpm]
	per_gene_mapped = str(round((gene_count/int(CDS_count))*100, 2)) #percentage of genes mapped
	est_depth = str(round((mapped_reads*float(dict_log[name]))/gene_len, 2)) #(total number of mapped reads * average read length) / total length of all the exons
	map_stats.write(name+'\t'+ processed_reads+'\t'+str(mapped_reads)+'\t'+percent_mapped + '\t'+ per_gene_mapped + '\t' + str(CDS_count) + '\t' + str(gene_len) + '\t' + est_depth+ '\n')
map_stats.close()

if '' in dicto:
	dicto.pop('')

#creates full matrix file	
for key, value in dicto.items():
	line = ''
	line += key + '\t'
	for item in value[:-1]:
		line += item + '\t'
	line += value[-1] + '\n'
	output_content += line
output_header += '\n'
output_file.write(output_header)
output_file.write(output_content)
print("Matrix created")
output_file.close()
print("Run complete.")
