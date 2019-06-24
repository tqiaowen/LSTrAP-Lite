# Tutorial
Welcome to the tutorial on how to use the LSTrAP-Lite source code!
We will use the sample data provided to demonstrate how to modify the code to build your own co-expression networks.

## Selecting the files to download
  * Go to [NCBI SRA](https://www.ncbi.nlm.nih.gov/sra)
  * Search for the files that you want to download, select only RNA sources and send results to RunSelector. <br> 
    Eg. <i>Artemisia annua</i><br>
    ![SRA search](images/search.png "NCBI SRA search")
  * Download the RunInfo Table
    ![RunInfo Table](images/SRAruntable.png "SRA RunInfo Table")

## Modifying the paths

![paths](images/paths.PNG "Paths to edit")

In the section "Paths to edit" found in LSTrAP-Lite_download.py, there are a few paths that needs to be modified for the script to work.
  * <b>pathtolocal</b> refers to the directory that your will be working in to download and process the files.
  * <b>download_list</b> refers to the file that contains the SRA run ID and the respective library format of the files that you want to download. Click [here](/sample_data/sra_runID.txt) for an example. These information can be found in the SRA run ta
  
