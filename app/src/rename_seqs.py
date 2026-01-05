import os
import pandas as pd
from app.utils.genbank_utils import DownloadGenBankFile, parse_genbank

def match_virus_names(gb, df, vmr, in_dir):
    '''Match virus names from VMR and Genbank file to dataframe and rename sequences'''
    for key in gb:
        if key in vmr["Virus GENBANK accession"].values:
            '''IF REF'''
            if key in df.index:
                df.loc[key, "genbank_desc"] = f'{vmr[vmr["Virus GENBANK accession"] == key]["Family"].item()} {vmr[vmr["Virus GENBANK accession"] == key]["Genus"].item()} {vmr[vmr["Virus GENBANK accession"] == key]["Species"].item()}'
            else:
                df.loc[key, "genbank_desc"] = f"UNKNOWN REF"
                print(f"{key} not in dataframe")
        else: 
            ''' IF UCF'''
            if key in df.index:
                df.loc[key, "genbank_desc"] = F"UNCLASSIFIED {gb[key].description}"
            else:
                df.loc[key, "genbank_desc"] = f"UNKNOWN UCF"
                print(f"{key} not in dataframe") 

    return df

def save_output(df, in_dir):
    df["accession"] = df.index
    df["name"] = df.apply(lambda x: f"{x.accession} {x['genbank_desc']}", axis=1)
    df.index = df["name"]
    df.to_csv(f"{in_dir}/data_nona_withnames.csv")

    # genes = ["rdrp", "helicase"] # TODO inhert these
    genes = ["rdrp", "helicase"]
    for gene in genes:
        seqs = df[["name", f"{gene}_domain_seq"]].values.tolist()
        with open(f"{in_dir}/{gene}_seqs.fasta", "w") as f:
            [f.write(f">{i[0]}\n{i[1]}\n") for i in seqs]

if __name__ == "__main__":
    '''Init'''
    in_dir = "./tmp/interpro_parsed/"
    infile = f"{in_dir}/data_nona_withnames.csv"
    gbfile = f"{in_dir}/genbank_sequences.gb"

    '''Collect data'''
    df = pd.read_csv(infile, index_col=0)
    vmr = pd.read_csv("./data/latest_vmr.csv", index_col=0)
    if not os.path.exists(gbfile):
        DownloadGenBankFile(gbfile, df.index.tolist())
    gb = parse_genbank(gbfile)
    
    '''Process'''
    df = match_virus_names(gb, df, vmr, in_dir)
    save_output(df, in_dir)