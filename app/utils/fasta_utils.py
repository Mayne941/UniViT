import numpy as np

def read_fa(fpath) -> list:
    '''Read fasta file to list of lists in format [[>name, seq], [...]]'''
    seqs = []
    try:
        with open(fpath, "r") as f:
            for l in f:
                if l[0] == ">":
                    seqs.append(f"~~{l}")
                else:
                    seqs.append(l.replace("\n", ""))
    except:
        '''Current release of ViralConsensus will sometimes dump binary into the output file - this is a temp fix'''
        print(
            f"*** WARNING: Encoding on your input fasta file ({fpath}) is messed up. Attempting to rescue it...")
        seqs = []  # RESET SEQS as it doesn't get wiped by transition to exception
        bases = ["A", "T", "C", "G", "N", "-"]
        with open(fpath, "r", encoding="ISO-8859-1") as f:
            for l in f.readlines():
                if l[0] not in bases:
                    seqs.append(f"~~{l}")
                else:
                    seqs.append(l)

        for i in range(len(seqs)):
            if seqs[i][0] == "~~":
                continue
            else:
                seqs[i] = "".join([j for j in seqs[i] if j in bases])

    seqs_split = [i.split("\n") for i in "".join(seqs).split("~~")]
    return [i for i in seqs_split if not i == [""]]

