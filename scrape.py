import requests
import csv
import os
import sys

# Check if the correct number of arguments were provided
if len(sys.argv) != 2:
    print("Usage: python code.py <input_file_name>")
    sys.exit()

# Read the input file containing the list of ChEMBL IDs
input_file_name = sys.argv[1]
with open(input_file_name, 'r') as f:
    chembl_ids = [line.strip() for line in f.readlines()]

# Create the output directory
output_dir = os.path.dirname(os.path.abspath(input_file_name))
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Create an empty list to store all retrieved data
all_data = []

# Loop through the ChEMBL IDs
for chembl_id in chembl_ids:
    try:
        # Retrieve data from ChEMBL API with pagination
        page = 0
        page_size = 100
        num_molecules = 0
        while True:
            url = f'https://www.ebi.ac.uk/chembl/api/data/molecule?target_chembl_id={chembl_id}&max_phase=4&molecular_weight__lte=600&ro5_violations=0&format=json&limit={page_size}&offset={page*page_size}'
            response = requests.get(url)
            data = response.json()

            # Check if data is retrieved successfully
            if 'molecules' in data:
                molecules = data['molecules']
                if not molecules:
                    break
                num_molecules += len(molecules)
                print(f'Retrieved {len(molecules)} molecules for ChEMBL ID: {chembl_id}, Page: {page+1}')
                
                # Append the retrieved data to the all_data list
                all_data.extend(molecules)
                
                page += 1

            else:
                print(f'Failed to retrieve data for ChEMBL ID: {chembl_id}\n')
                break

    except requests.exceptions.RequestException as re:
        print(f'Failed to retrieve data for ChEMBL ID: {chembl_id}, Request Exception: {re}\n')
    except ValueError as ve:
        print(f'Failed to retrieve data for ChEMBL ID: {chembl_id}, JSON Parsing Error: {ve}\n')

# Save all retrieved data as a single CSV file
output_file = 'data.csv'
output_file_path = os.path.join(output_dir, output_file)
with open(output_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ChEMBL ID', 'Name', 'Max Phase', 'Molecular Formula', 'Molecular Weight', 'SMILES'])
    # Write the retrieved data to the CSV file
    for molecule in all_data:
        chembl_id = molecule['molecule_chembl_id']
        name = molecule.get('molecule_name', 'N/A')
        max_phase = molecule['max_phase']
        molecular_formula = molecule['molecule_properties'].get('full_molformula', 'N/A') if 'molecule_properties' in molecule and molecule['molecule_properties'] is not None else 'N/A'
        molecular_weight = molecule['molecule_properties'].get('full_mw', 'N/A') if 'molecule_properties' in molecule and molecule['molecule_properties'] is not None else 'N/A'
        smiles = molecule['molecule_structures']['canonical_smiles'] if molecule['molecule_structures'] is not None and 'canonical_smiles'

# Save the ChEMBL ID, Name, and number of retrieved SMILES to a text file in the same directory
# Specify the output file name and path
output_file_path = os.path.join(output_dir, 'stats.txt')

# Open the output txt file in write mode
with open(output_file_path, 'w') as txtfile:
    txtfile.write(f"ChEMBL ID\tOutput File\tNumber of Retrieved SMILES\n")
    # Iterate through the rows in the CSV file we created earlier
    with open(output_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # Skip the header row
        next(reader)
        # Count the number of rows in the CSV file
        num_rows = sum(1 for row in reader)
        # Write the statistics to the text file
        txtfile.write(f"{chembl_id}\t{output_file}\t{num_rows}\n")
