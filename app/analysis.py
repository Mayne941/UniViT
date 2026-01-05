import os
import shutil
import json

if __name__ == "__main__":
    config_file = input("Enter path to config file (json): ")
    # config_file = "data/examples/example_univit_config.json"

    with open(config_file, "r") as f:
        config = json.load(f)

    # parse_xml > tmp/interpro_parsed/
    # split_seqs > tmp/processed_output
    # align_and_tree > tmp/processed_output
    # call_colabfold > tmp/processed_output