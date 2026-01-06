import os
import shutil
import json
import requests
from app.utils.populate_gravity_call import get_default_gravity
from app.src.split_orfs import main as split_orfs_main

def create_exp_dirs(config):
    '''Create experiment directory if it does not exist'''
    config["FullDir"] = f'{config["ExperimentDir"]}/{config["ExperimentName"]}'
    if not os.path.exists(config["FullDir"]):
        os.mkdir(config["FullDir"])

    dirs = {
        "OrfsDir": f'{config["FullDir"]}/orfs',
        "XmlDir": f'{config["FullDir"]}/xml',
        "ParsedXmlDir": f'{config["FullDir"]}/xml_parsed',
        "OutputDir": f'{config["FullDir"]}/processed_output',
        "ColabFoldDir": f'{config["FullDir"]}/colabfold',
        "ColabFoldOutputDir": f'{config["FullDir"]}/colabfold_output',
        "FoldTreeDir": f'{config["FullDir"]}/foldtree'
    }

    for dir_key, dir_path in dirs.items():
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            config[dir_key] = dir_path

    return config


def get_gravity_parameters(config):
    if not config["GravityCustomParameters"] == "NONE":
        try: 
            with open(config["GravityCustomParameters"], "r") as f:
                gravity_params = json.load(f)
            return gravity_params
        except Exception as e:
            print(f"Error loading custom GRAViTy parameters; loading defaults. Error: {e}")

    else:
        gravity_params = get_default_gravity()

        gravity_params["GenomeDescTableFile"] = config["InputData"]
        gravity_params["ExpDir"] = f'{config["FullDir"]}_GRAViTy'
        if not config["GravityGenbankFile"] == "NONE":
            gravity_params["GenomeSeqFile"] = config["GravityGenbankFile"]
        else:
            gravity_params["GenomeSeqFile"] = f'{gravity_params["ExpDir"]}/genbank_sequences.gb'

    config["GravityParamsFile"] = f'{config["FullDir"]}/gravity_params.json'

    with open(config["GravityParamsFile"], "w") as f:
        json.dump(gravity_params, f)  


def call_gravity(config, gravity_params):
    '''Call GRAViTy with given parameters'''   
    response = requests.post(f'{config["GravityBroadcast"]}/new_classification_full/', data=gravity_params)
    print(response)
    if not response.status_code == 200:
        raise Exception(f"Error calling GRAViTy API. Status code: {response.status_code}, error: {response.text}")

def get_gravity_output(config, gravity_params):
    try:
        shutil.copyfile(f'{gravity_params["ExpDir"]}/Mash/Subjects.fasta', f'{config["FullDir"]}/orfs/extraced_orfs.fasta')
    except Exception as e:
        print(f"Error copying extracted ORFs: {e}")

def dump_updated_config(config, config_file):
    with open(f'{config_file}', "w") as f:
        json.dump(config, f)

if __name__ == "__main__":
    config_file = input("Enter path to config file (json): ")
    # config_file = "data/examples/example_univit_config.json"

    with open(config_file, "r") as f:
        config = json.load(f)
    
    create_exp_dirs(config)
    gravity_params = get_gravity_parameters(config)
    call_gravity(config, gravity_params)

    get_gravity_output(config, gravity_params)
    split_orfs_main(config)
    dump_updated_config(config)
    print(f"Pipelien part 1 complete. Please progress to InterProScan stage in documentation.")
