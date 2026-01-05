import os, shutil
from app.utils.fasta_utils import read_fa
from app.utils.shell_utils import shell

'''Take GRAViTy ORFs from output, chunk them for InterProScan'''

def clean(fastas):
    '''Remove unprintables, specifically '.0 ~', '|' '''
    clean_fastas = []
    for fasta in fastas:
        clean_fastas.append([fasta[0].replace(".0 ~", "").replace("|", "_"), fasta[1]])
    return clean_fastas

def fasta_split(fasta, n=100) -> list:
    '''Split fasta sequence into chunks of size n'''
    return [fasta[i:i + n] for i in range(0, len(fasta), n)]

def main(config):
    outdir_stem = config["FullDir"]
    in_fname = f"{outdir_stem}/extraced_orfs.fasta"
    if not os.path.exists(outdir_stem):
        os.mkdir(outdir_stem)
    outdir = f"{outdir_stem}/orfs/"
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    if not os.path.exists(f"{outdir_stem}/interpro_xml/"):
        os.mkdir(f"{outdir_stem}/interpro_xml/")
    out_fname = f"{outdir}/extraced_orfs_split_.fasta"

    '''Process'''
    clean_fasta = clean(read_fa(in_fname))
    split_fastas = fasta_split(clean_fasta, n=100)

    '''Tidy, save'''
    for chunk_idx, chunk in enumerate(split_fastas):
        with open(out_fname.replace("_.fasta", f"_{chunk_idx}.fasta"), "w") as f:
            [f.write(f"{i[0]}\n{i[1]}\n") for i in chunk]

if __name__ == '__main__':
    ## TODO BELOW JUST FOR DEV
    '''Init'''
    outdir_stem = "./tmp/"
    fname = f"{outdir_stem}/Subjects.fasta"
    if not os.path.exists(outdir_stem):
        os.mkdir(outdir_stem)
    outdir = f"{outdir_stem}/orfs/"
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    if not os.path.exists(f"{outdir_stem}/interpro_xml/"):
        os.mkdir(f"{outdir_stem}/interpro_xml/")
    in_fname = f"{outdir}/Subjects.fasta"
    out_fname = f"{outdir}/Subjects_cleaned_.fasta"

    shutil.copy(fname, in_fname)

    '''Process'''
    clean_fasta = clean(read_fa(in_fname))
    split_fastas = fasta_split(clean_fasta, n=100)

    '''Tidy, save'''
    for chunk_idx, chunk in enumerate(split_fastas):
        with open(out_fname.replace("_.fasta", f"_{chunk_idx}.fasta"), "w") as f:
            [f.write(f"{i[0]}\n{i[1]}\n") for i in chunk]
    # shell(f"rm -r {outdir_stem}") # Uncomment when cascade set up