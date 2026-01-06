import os
import shutil
from app.utils.shell_utils import shell

def main(config):
    # TODO MUST HAVE FOLDTREE IN CURRENT ENV
    os.mkdir(f'{config["FoldTreeDir"]}/structs')
    for file in os.listdir(f'{config["ColabFoldOutputDir"]}/'):
        if file.endswith(".pdb"):
            shutil.copyfile(f'{config["ColabFoldOutputDir"]}/{file}', f'{config["FoldTreeDir"]}/structs/{file}')

    shell(f"touch {config['FoldTreeDir']}/identifiers.txt") 
    # TODO Parameterise -s arg?
    shell(f"snakemake --cores 8 --use-conda -s ./workflow/fold_tree --config folder={config['FoldTreeDir']} filter=False foldseek_cores=8 custom_structs=True")
