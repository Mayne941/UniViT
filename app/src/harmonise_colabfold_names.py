import os
from app.utils.fasta_utils import read_fa

def main(config):
    data_dir = f'{config["OutputDirSingles"]}/{config["ColabfoldGene"]}/'
    
    files = [i.replace(".fasta","") for i in os.listdir(data_dir) if i.endswith(".fasta")]

    for file in files:
        accession = file.split("_")[0]
        if not os.path.exists(f"{config['ColabFoldOutputDir']}/{accession}.pdb"):
            print(f"Skipping renaming of {config['ColabFoldOutputDir']}/{accession} as no PDB file found in output directory.")
            continue

        header = read_fa(f"{data_dir}/{file}.fasta")[0][0].replace(">","").replace(" ","_").replace("/","")
        os.rename(f"{config['ColabFoldOutputDir']}/{accession}.pdb", f"{config['ColabFoldOutputDir']}/{header}.pbd")