import os
from app.utils.shell_utils import shell

def align(in_dir, out_dir, gene):
    '''Align sequences'''
    shell(f"mafft --auto --thread 8 {in_dir}/{gene}_seqs.fasta > {out_dir}/{gene}_seqs_aligned.fasta")
    print(f"Finished aligning for {gene}")

def build_tree(in_dir, out_dir, gene):
    '''Build tree from aligned sequences'''
    shell(f"fasttree {out_dir}/{gene}_seqs_aligned.fasta > {out_dir}/{gene}_fasttree.nwk")
    print(f"Finished building tree for {gene}")

def main(config):
    for gene in config["HallmarkGenes"]:
        align(config["ParsedXmlDir"], config["OutputDir"], gene)
        build_tree(config["ParsedXmlDir"], config["OutputDir"], gene)


if __name__ == "__main__":
    '''Init'''
    in_dir = "./tmp/interpro_parsed/"
    out_dir = "./tmp/processed_output/"
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    # genes = ["rdrp", "helicase"]
    genes = ["rdrp"]
    for gene in genes:
        align(in_dir, out_dir, gene)
        build_tree(in_dir, out_dir, gene)
