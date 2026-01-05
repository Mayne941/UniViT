# UniViT pipeline
## Description
A universal virus taxonomy pipeline combining hallmark gene alignment, structural comparisons with ColabFold and genomic analysis with GRAViTy-V2.

First described in: 

Mayne, R., Smith, DB., Brown, K., *et al.* (2026) Comprehensive hallmark gene sequence, genomic and structural analysis of Picornavirales viruses clarifies new and existing taxa. *biorXiv preprint* XX DOI TO FOLLOW XX

**N.b. Pipeline is currently in an alpha state. This means that setup, runtime and output are incomplete and prone to change. 

## Usage Guidelines
Current pipeline:

0. conda activate gvc
1. Make GRAViTy-V2 compatible VMR with accessions and virus names as minimum fields (put "UNCLASSIFIED" in relevant virus names)
2. Run GRAViTy-V2 to pull sequences, make ORFs and estimate phylogeny
3. Extract ORFs, chunk into fastas  (app.src.split_orfs) > tmp/orfs
5. Run ORFs on InterPro, download xml files > tmp/interpro_xml
6. Run InterPro result parser (app.src.parse_xml) > tmp/interpro_parsed
7. Join original virus names to InterPro output (app.src.rename_seqs) > tmp/interpro_parsed/
8. Split seqs into classified/unclassified, and RdRps to single sequences for input to ColabFold (app.src.split_seqs) > ./tmp/processed_output

-> GRAViTy just RdRp PPHMMs
* Copy all rdrps to gravity folder
* Run genbank converter
* Run sequence detail getter
* Start run, with similarity scheme = P
-> GRAViTy refined run (use tmp/interpro_parsed/data_nona_withnames.csv)
* Use VMR-like document from just RdRp PPHMM run
* Full GRAViTy run
-> ColabFold (split RdRp sequences, XXX)
* Transfer seqs to alphafold dir
* Run colabfold (automate)
* Rename pdb seqs with fasta headers (rename_fasta)
-> Conventional alignments (app.src.align_and_tree) ./tmp/processed_output

9. Copy output from each analysis to output folder. Remove spaces from fasta headers

TODO 
1. Download & automate interpro; adapt script to remove 100 seq split thing
2. Move output to experiment folder
3. More filtering in the rename bit to remove genome completeness, "MAG:" etc.

## Change log
### Version 0
1. Initial push

## Disclaimer
The material embodied in this software is provided to you "as-is", “with all faults”, and without warranty of any kind, express, implied or otherwise, including without limitation, any warranty of fitness for a particular purpose, warranty of non-infringement, or warranties of any kind concerning the safety, suitability, lack of viruses, inaccuracies, or other harmful components of this software. There are inherent dangers in the use of any software, and you are solely responsible for determining whether this software is compatible with your equipment and other software installed on your equipment. You are convert_fasta_to_genbankalso solely responsible for the protection of your equipment and backup of your data, and the developers/providers will not be liable for any damages you may suffer in connection with using, modifying, or distributing this software. Without limiting the foregoing, the developers/providers make no warranty that: the software will meet your requirements; the software will be uninterrupted, timely, secure, or error-free; the results that may be obtained from the use of the software will be effective, accurate, or reliable; the quality of the software will meet your expectations; any errors in the software will be identified or corrected.

Software and its documentation made available here could include technical or other mistakes, inaccuracies, or typographical errors. The developers/providers may make changes to the software or documentation made available here may be out of date, and the developers/providers make no commitment to update such materials.

The developers/providers assume no responsibility for errors or omissions in the software or documentation available from here.

In no event shall the developers/providers be liable to you or anyone else for any direct, special, incidental, indirect, or consequential damages of any kind, or any damages whatsoever, including without limitation, loss of data, loss of profit, loss of use, savings or revenue, or the claims of third parties, whether or not the developers/providers have been advised of the possibility of such damages and loss, however caused, and on any theory of liability, arising out of or in connection with the possession, use, or performance of this software.

The use of this software is done at your own discretion and risk and with agreement that you will be solely responsible for any damage to your computer system, or networked devices, or loss of data that results from such activities. No advice or information, whether oral or written, obtained by you from the developers/providers shall create any warranty for the software.