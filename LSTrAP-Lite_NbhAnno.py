import os

# Formats and creates dictionary based on mercator results
mer_file = open("/path/to/mercator.results.txt", "r")
mer_file.readline()
mer_dict = {}
for i in mer_file:
	if "pwa" in i.split("\t")[2]:
		gene =  i.split("\t")[2][1:-1].upper()
		desc = [i.strip("\n").split("\t")[-2][1:-1].split("(original description: ")[1][:-1], i.strip("\n").split("\t")[-2][1:-1].split(" (original description:")[0], i.split("\t")[0][1:-1], i.split("\t")[1][1:-1]]
		mer_dict[gene] = desc
mer_file.close()

#For annotating a single file
file_in = "/path/to/nbh.txt"
nbh_file = open(file_in, "r")
out = open(file_in.split(".txt")[0] + "_anno.txt", "w+")
for x in nbh_file:
	gene2 = x.split("\t")[1].split("cds_")[1].split("_")[0]
	out.write(x.split("\t")[0] + "\t" + x.split("\t")[1] + "\t" + x.strip("\n").split("\t")[-1]+ "\t" + mer_dict[gene2][0] +  "\t" + mer_dict[gene2][2] + "\t" + mer_dict[gene2][3]+  "\t" +  mer_dict[gene2][1]  + "\n")
nbh_file.close()
out.close()
			
#For files multiple files stored in a directory.
curdir = "/path/to/dir/"
for i in os.listdir(curdir):
	if "_nbh.txt" in i:
		if "anno" not in i:
			nbh_file = open(curdir + i, "r")
			out = open(curdir + i.split(".txt")[0] + "_anno.txt", "w+")
			for x in nbh_file:
				gene2 = x.split("\t")[1].split("cds_")[1].split("_")[0]
				out.write(x.split("\t")[0] + "\t" + x.split("\t")[1] + "\t" + x.strip("\n").split("\t")[-1]+ "\t" + mer_dict[gene2][0] +  "\t" + mer_dict[gene2][2] + "\t" + mer_dict[gene2][3]+  "\t" +  mer_dict[gene2][1]  + "\n")
			nbh_file.close()
			out.close()
