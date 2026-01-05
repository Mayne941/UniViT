import os
from app.utils.fasta_utils import read_fa


def make_single_seqs(gene, singles_dir, in_dir):
    '''Make single sequence files'''
    if not os.path.exists(f"{singles_dir}/{gene}"):
        os.mkdir(f"{singles_dir}/{gene}")
    for fa in read_fa(f"{in_dir}/{gene}_seqs.fasta"):
            with open(f"{singles_dir}/{gene}/{fa[0].split(' ')[0].replace('>', '')}.fasta", "w") as f:
                f.write(f"{fa[0]}\n{fa[1]}\n")


def split_unclassified(in_dir, gene, just_classified_dir, just_unclassified_dir):
    '''Make big file for just class/unclasified'''
    classified, unclassified = [], []
    for fa in read_fa(f"{in_dir}/{gene}_seqs.fasta"):
        if "UNCLASSIFIED" in fa[0]:
            unclassified.append(fa)
        else:
            classified.append(fa)

    with open(f"{just_unclassified_dir}/{gene}_just_unclassified.fasta", "w") as f:
        for fa in unclassified:
            f.write(f"{fa[0]}\n{fa[1]}\n")

    with open(f"{just_classified_dir}/{gene}_just_classified.fasta", "w") as f:
        for fa in classified:
            f.write(f"{fa[0]}\n{fa[1]}\n")

def main(config):
    singles_dir = f"{config['OutputDir']}/singles/"
    if not os.path.exists(singles_dir):
        os.mkdir(singles_dir)
    just_classified_dir = f"{config['OutputDir']}/just_classified/"
    if not os.path.exists(just_classified_dir):
        os.mkdir(just_classified_dir)
    just_unclassified_dir = f"{config['OutputDir']}/just_unclassified/"
    if not os.path.exists(just_unclassified_dir):
        os.mkdir(just_unclassified_dir)

    '''Process'''
    for gene in config["HallmarkGenes"]:
        make_single_seqs(gene, singles_dir, config["ParsedXmlDir"])
        split_unclassified(config["ParsedXmlDir"], gene, just_classified_dir, just_unclassified_dir)


if __name__ == "__main__":
    '''Init''' # TODO dev only
    genes = ["rdrp", "helicase"]
    in_dir = "./tmp/interpro_parsed/"
    out_dir = "./tmp/processed_output/"
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    
    singles_dir = f"{out_dir}/singles/"
    if not os.path.exists(singles_dir):
        os.mkdir(singles_dir)
    just_classified_dir = f"{out_dir}/just_classified/"
    if not os.path.exists(just_classified_dir):
        os.mkdir(just_classified_dir)
    just_unclassified_dir = f"{out_dir}/just_unclassified/"
    if not os.path.exists(just_unclassified_dir):
        os.mkdir(just_unclassified_dir)

    '''Process'''
    for gene in genes:
        make_single_seqs(gene, singles_dir, in_dir)
        split_unclassified(in_dir, gene, just_classified_dir, just_unclassified_dir)
