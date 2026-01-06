import os
import shutil
from app.utils.shell_utils import shell


def read_log(fname):
    '''Find highest scoring model in log file'''
    with open (fname + "/log.txt", "r") as f:
        lines = f.readlines()
    
    for idx, line in enumerate(lines):
        if "reranking models by 'plddt' metric" in line:
            best_model = lines[idx + 2].strip()
            break
    
    return best_model.split(" ")[2]

def get_best_model(model, fname, file, config):
    '''Get the best model from the output directory, move elsewhere, and rename it'''
    files = [f for f in os.listdir(fname) if f.endswith(".pdb") and model in f and "_relaxed" in f]
    assert len(files) == 1
    shutil.copyfile(f"{config['ColabFoldDir']}{file.replace('.fasta','')}/{files[0]}", f"{config['ColabFoldOutputDir']}/{files[0].split('_')[0]}.pdb")

def main(config):
    # TODO MUST HAVE COLABFOLD IN CURRENT ENV; ENSURE ALIASED AS "colabfold_batch"
    data_dir = f'{config["OutputDirSingles"]}/{config["ColabfoldGene"]}/'

    files = [i for i in os.listdir(data_dir) if i.endswith(".fasta")]
    for idx, file in enumerate(files):
        try:
            if os.path.exists(f"{config['ColabFoldOutputDir']}/{file.split('_')[0]}.pdb"):
                print(f"Skipping {config['ColabFoldOutputDir']}/{file.split('_')[0]}.pdb as output file already exists.")
                continue
            print(f"Processing {file}. Progress: {idx+1}/{len(files)}")
            _  = shell(f"colabfold_batch --templates --amber {data_dir}/{file} {config['ColabFoldDir']}/{file.replace('.fasta','')}/", ret_output=True)
            best_model = read_log(f"{config['ColabFoldDir']}{file.replace('.fasta','')}")
            get_best_model(best_model, f"{config['ColabFoldDir']}{file.replace('.fasta','')}", file, config)
            print(f"Finished colabfold local analysis of {file}")
        except Exception as e:
            print(f"*** ERROR: Could not process {file}. Error message: {e}")
            continue


