import json
from app.src.parse_xml import main as parse_xml_main
from app.src.split_seqs import main as split_seqs_main
from app.src.align_and_tree import main as align_and_tree_main
from app.src.call_colabfold import main as call_colabfold_main

if __name__ == "__main__":
    config_file = input("Enter path to config file (json): ")
    # config_file = "data/examples/example_univit_config.json"

    with open(config_file, "r") as f:
        config = json.load(f)

    parse_xml_main(config)
    split_seqs_main(config)
    align_and_tree_main(config)
    call_colabfold_main(config)