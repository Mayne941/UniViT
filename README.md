# UniViT
## Description
A universal virus taxonomy pipeline combining hallmark gene alignment, structural comparisons with ColabFold and genomic analysis with GRAViTy-V2.

First described in: 

Mayne, R., Smith, DB., Brown, K., *et al.* (2026) Comprehensive hallmark gene sequence, genomic and structural analysis of Picornavirales viruses clarifies new and existing taxa. *biorXiv preprint* XX DOI TO FOLLOW XX

*N.b. 1. This software is currently in an alpha state. This means that setup, runtime and output may be buggy and are liable to change as development progresses. It is nontrivial for users without bioinformatics expertise to install UniViT and its dependencies in its current state, and consequently it is not recommended to pull or install this software unless the user fully understands the instructions and is prepared to interact with the codebase. Full developer support and user guidance will be provided as the software evolves.*

*N.b. 2. UniViT is designed to work on high-end personal computers. It is highly unlikely to work efficiently, if at all, on a PC with <32 Gb RAM or a CUDA-enabled discrete GPU.*

## Usage Guidelines
### Setup
**UniViT was designed for Debian-based Linux. Instructions assume running Ubuntu >22.04. Modifications will be required for other flavours of Linux and Darwin. Running UniViT in native Windows will require technical wizardry.**
1. Install Anaconda/Miniconda, Curl and Docker are installed. Defer to documentation for each tool for instructions.
1. Create conda environment. ```$ conda create -n univit python=3.10```
1. Activate conda environment. ```$ conda activate univit```
1. Install pip libraries. ```$ pip install -U -r requirements.txt```
1. Install following libraries via conda (flag '-c bioconda'): mafft (>=7.525), fasttree (>=2.2.0)
1. Install GRAViTy-V2, ColabFold Local, Fold_Tree from source. Defer to documentation for each tool for instructions.
1. (Optional) Pull InterProScan Docker container and your choice of database.

### Run pipeline

1. Activate conda environment. ```$ conda activate univit```
1. Create a GRAViTy-V2 VMR-like document. Defer to GRAViTy-V2 documentation. Must contain at least these fields:
    * "Virus name(s)" -- This is the name for each sequence that will propagate through all experiments. New/unclassified sequences should be prefixed with "UNCLASSIFIED".
    * "Virus GENBANK accession" -- This will be used to label all sequences and pull from NCBI, if user sequences are not provided.
1. Create a UniViT command config file (blank example is included in ./data/examples/example_univit_config.json). At least the following fields must be edited:
    * "ExperimentName" -- a new folder with this name will be generated ({ExperimentDir}/{ExperimentName}) and all output will be saved here.
    * "InputData" -- path to input GRAViTy-V2 VMR-like document.
    * "HallmarkGenes" -- list of (lowercase) strings for each hallmark gene to create a phylogeny from; names MUST correspond with their designation from InterPro Scan as these are used to parse matching domains from output. 
1. Start a GRAViTy-V2 server. Default config expects this to broadcast on ```http://127.0.0.1:8000``` .
1. Call the UniVit entrypoint and point to the UniViT command config file when prompted. This will run GRAViTy-V2, as well as extract ORFs from each sequence for downstream processing. ```$ python3 -m app.preprocess```
1. EITHER run ({ExperimentDir}/orfs/extracted_orfs.fasta) through InterProScan using local OR web UI. By default UniViT splits your input ORFs into batches, i.e. individual fasta files with length == 100.
    * If running InterProScan locally, your command will look something like this. ```$ docker run --rm -w $PWD -v $PATH-TO-INTERPRO-DATABASE -input $PATH-TO-ORFS-FASTA -b $PATH-TO-EXP-DIR/xml -f XML```. This step can be automated by making a shell call in app/entrypoint.py. N.b. be mindful to call iteratively or concatenate input if you have >1 input fasta files! 
    * If using the web UI, use the UniViT helper function to split ORFS into fasta files with length == 100 sequences. Download XML files for each response and place in {ExperimentDir}/xml 
1. Call the next UniVit script. ```$ python3 -m app.analysis``` 


## To do list 
1. Automate interpro call; deprecate requirement for splitting sequences into runs of 100.
1. Move output to experiment folder
1. More filtering in the rename bit to remove genome completeness, "MAG:" etc.
1. API call for GRAViTy-V2
1. Script calling all functions.
1. Wrap in API.
1. Create example data.
1. Create github wiki.

## Change log
### Version 0
1. Init

## Disclaimer
The material embodied in this software is provided to you "as-is", “with all faults”, and without warranty of any kind, express, implied or otherwise, including without limitation, any warranty of fitness for a particular purpose, warranty of non-infringement, or warranties of any kind concerning the safety, suitability, lack of viruses, inaccuracies, or other harmful components of this software. There are inherent dangers in the use of any software, and you are solely responsible for determining whether this software is compatible with your equipment and other software installed on your equipment. You are convert_fasta_to_genbankalso solely responsible for the protection of your equipment and backup of your data, and the developers/providers will not be liable for any damages you may suffer in connection with using, modifying, or distributing this software. Without limiting the foregoing, the developers/providers make no warranty that: the software will meet your requirements; the software will be uninterrupted, timely, secure, or error-free; the results that may be obtained from the use of the software will be effective, accurate, or reliable; the quality of the software will meet your expectations; any errors in the software will be identified or corrected.

Software and its documentation made available here could include technical or other mistakes, inaccuracies, or typographical errors. The developers/providers may make changes to the software or documentation made available here may be out of date, and the developers/providers make no commitment to update such materials.

The developers/providers assume no responsibility for errors or omissions in the software or documentation available from here.

In no event shall the developers/providers be liable to you or anyone else for any direct, special, incidental, indirect, or consequential damages of any kind, or any damages whatsoever, including without limitation, loss of data, loss of profit, loss of use, savings or revenue, or the claims of third parties, whether or not the developers/providers have been advised of the possibility of such damages and loss, however caused, and on any theory of liability, arising out of or in connection with the possession, use, or performance of this software.

The use of this software is done at your own discretion and risk and with agreement that you will be solely responsible for any damage to your computer system, or networked devices, or loss of data that results from such activities. No advice or information, whether oral or written, obtained by you from the developers/providers shall create any warranty for the software.