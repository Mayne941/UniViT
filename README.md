Current pipeline:

0. conda activate gvc
1. Make GRAViTy-V2 compatible VMR with accessions and virus names as minimum fields (put "UNCLASSIFIED" in relevant virus names)
2. Run GRAViTy-V2 to pull sequences, make ORFs and estimate phylogeny
3. Extract ORFs, chunk into fastas  (app.src.split_orfs) > tmp/orfs
5. Run ORFs on InterPro, download xml files > tmp/interpro_xml
6. Run InterPro result parser (app.src.parse_interpro) > tmp/interpro_parsed
7. Join original virus names to InterPro output (app.src.rename_seqs) > tmp/interpro_parsed/
8. Split seqs into classified/unclassified, and RdRps to single sequences for input to ColabFold (app.src.split_seqs) > ./tmp/processed_output

-> GRAViTy refined run (use tmp/interpro_parsed/data_nona_withnames.csv)
-> ColabFold (split RdRp sequences, XXX)
-> Conventional alignments (app.src.align_and_tree) ./tmp/processed_output

9. Copy output from each analysis to output folder. Remove spaces from fasta headers

TODO 
1. Download & automate interpro; adapt script to remove 100 seq split thing
2. Move output to experiment folder
3. More filtering in the rename bit to remove genome completeness, "MAG:" etc.