import os
import json
import requests
from app.utils.populate_gravity_call import get_default_gravity
from app.utils.shell_utils import shell

def create_exp_dir(config):
    '''Create experiment directory if it does not exist'''
    exp_dir = f'{config["ExperimentDir"]}/{config["ExperimentName"]}'
    if not os.path.exists(exp_dir):
        os.mkdir(exp_dir)


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
        gravity_params["ExpDir"] = f'{config["ExperimentDir"]}/{config["ExperimentName"]}_GRAViTy'
        if not config["GravityGenbankFile"] == "NONE":
            gravity_params["GenomeSeqFile"] = config["GravityGenbankFile"]
        else:
            gravity_params["GenomeSeqFile"] = f'{gravity_params["ExpDir"]}/genbank_sequences.gb'

    config["GravityParamsFile"] = f'{config["ExperimentDir"]}/{config["ExperimentName"]}/gravity_params.json'

    with open(config["GravityParamsFile"], "w") as f:
        json.dump(gravity_params, f)  


def call_gravity(config, gravity_params):
    '''Call GRAViTy with given parameters'''   
    response = requests.post(f'{config["GravityBroadcast"]}/new_classification_full/', data=gravity_params)
    print(response)
    if not response.status_code == 200:
        raise Exception(f"Error calling GRAViTy API. Status code: {response.status_code}, error: {response.text}")


if __name__ == "__main__":
    config_file = input("Enter path to config file (json): ")
    # config_file = "data/examples/example_univit_config.json"

    with open(config_file, "r") as f:
        config = json.load(f)
    
    create_exp_dir(config)
    gravity_params = get_gravity_parameters(config)
    call_gravity(config, gravity_params)