## Scraping drug-like molecules in SMILES format for a specific target from ChEMBL Database

## The background

**The problem:** you have a molecule of interest (a protein, perhaps) and you want to collect drug-like molecules that target it. ChEMBL (https://www.ebi.ac.uk/chembl/) is a curated database for drug-like molecules. You go in there, you look up your molecule of interest, and now you have to manually download 7.000 drugs. 

This is a script to query the ChEMBL database and retrieve all small molecules that correspond to a set of CHEMBL IDs, in SMILES string format. 
The input is a txt file containing the CHEMBL IDs that you want to use as targets and retrieve molecules for. 
The outputs are:
- a CSV file, named **data.csv**, containing the retrieved data from the ChEMBL API in a tabular format with the following columns:\
**ChEMBL ID**, **Name**, **Max Phase**, **Molecular Formula**, **Molecular Weight**, and **SMILES**.\
Each row in the CSV file represents a molecule, with values populated for each column based on the retrieved data.
- a text file, named **stats.txt**, containing a brief statistical summary for the retrieved data in a tab-separated format with the following columns:\
**ChEMBL ID**, **Output File**, and **Number of Retrieved SMILES**. \
The **ChEMBL ID** column contains the ChEMBL ID for which data was retrieved, the **Output File** column contains the name of the CSV file where the data was saved (data.csv in this case), and the **Number of Retrieved SMILES** column contains the total number of retrieved SMILES (i.e., the total number of rows) in the **data.csv** file. The values for each column will be separated by tabs ('\t') in the text file.

## To run this script you must have:
- Python installed on your system and added to your system's PATH environment variable.
- the `scrape.py` file in the current directory.
- a text file called `input.txt` in the same directory as the `scrape.py` file. Alternatively, you can specify the full path to the `input.txt` file in the command line. The `input.txt` file contains the ChEMBL IDs (targets) that you wish to retrieve molecules for. 


**Correct formatting for the input.txt file:**
It should contain a list of ChEMBL IDs, with one ID per line. Each line should contain a single ChEMBL ID, and there should be no extra characters or spaces in the file.
For example:

CHEMBL12345\
CHEMBL67890\
CHEMBL54321

## Adjusting other query parameters

**By default, the parameters are:**\
Molecular weight <=600\
R05 violations = 0\
Max phase = 4

For the moment, you can adjust the filters for the ChEMBL results (molecular weight, RO5 violations, maximum phase etc) by changing the values of the variables in the url (eg max_phase=3 to get molecules that got to the 3rd trial phase). In a future commit, the parameters will be determined by the user in the input.txt file. 
https://github.com/IoDiakou/Scraping-data-using-the-ChEMBL-database-API/blob/96f7b06b7bcedd72d61cbe552908fe052097863c/scrape.py#L32

## Command line use
You can use the script via the command line, as such:
```
python scrape.py input.txt
```

Alternatively, if you have the `input.txt` file in a **different directory** than the `scrape.py` file:
```
python scrape.py /path/to/input.txt
```
Where '/path/to/input.txt' should be replaced with the **actual full path** to the `input.txt` file on your system.

## Future additions:
- extend error handling
- dry up some code parts
- incorporate API throttling
