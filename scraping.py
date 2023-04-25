import requests
import csv

# List of ChEMBL IDs of viral proteases
chembl_ids = ['CHEMBL2033', 'CHEMBL4297']

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
                
                # Save the retrieved data to a CSV file
                with open('viral_protease_inhibitors.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)

                    # Write the data rows to the CSV
                    for molecule in molecules:
                        chembl_id = molecule['molecule_chembl_id']
                        name = molecule.get('molecule_name', 'N/A')
                        max_phase = molecule['max_phase']
                        molecular_formula = molecule['molecule_properties']['full_molformula'] if 'molecule_properties' in molecule and molecule['molecule_properties'] is not None and 'full_molformula' in molecule['molecule_properties'] else 'N/A'
                        molecular_weight = molecule['molecule_properties']['full_mw'] if 'molecule_properties' in molecule and molecule['molecule_properties'] is not None and 'full_mw' in molecule['molecule_properties'] else 'N/A'
                        smiles = molecule['molecule_structures']['canonical_smiles'] if molecule['molecule_structures'] is not None and 'canonical_smiles' in molecule['molecule_structures'] else 'N/A'
                        writer.writerow([chembl_id, name, max_phase, molecular_formula, molecular_weight, smiles])
                
                page += 1

            else:
                print(f'Failed to retrieve data for ChEMBL ID: {chembl_id}\n')
                break

    except requests.exceptions.RequestException as re:
        print(f'Failed to retrieve data for ChEMBL ID: {chembl_id}, Request Exception: {re}\n')
    except ValueError as ve:
        print(f'Failed to retrieve data for ChEMBL ID: {chembl_id}, JSON Parsing Error: {ve}\n')

# Save the ChEMBL ID, Name, and number of retrieved SMILES to a text file
with open('viral_protease_stats.txt', 'a') as stats_file:
    for chembl_id in chembl_ids:
        stats_file.write(f'ChEMBL ID: {chembl_id}, Number of Retrieved Molecules: {num_molecules}\n')
