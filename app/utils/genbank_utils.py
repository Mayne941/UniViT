from Bio import Entrez, SeqIO

def DownloadGenBankFile(GenomeSeqFile, SeqIDLists):
    '''Hit GenBank to get data. Needs user to provide email authentication'''
    Entrez.email = "test@test.com"
    try:
        handle = Entrez.efetch(db="nucleotide", id=", ".join([x for x in SeqIDLists]), rettype="gb", retmode="text")
    except Exception as e:
        raise f"Failed to pull Genbank Data from NCBI Entrez with exception: {e}"

    print("Writing contents of genbank object to file")
    with open(GenomeSeqFile, "w") as GenomeSeqFile_handle:
        GenomeSeqFile_handle.write(handle.read())

    handle.close()

def parse_genbank(gbfile):
    '''Parse GenBank file to extract relevant information'''

    GenBankDict = SeqIO.index(gbfile, "genbank")
    CleanGenbankDict = {}
    for i in GenBankDict.items():
        if "u" in str(i[1].seq).lower():
            i[1].seq = i[1].seq.back_transcribe()
        CleanGenbankDict[i[0].split(".")[0]] = i[1]
    
    return CleanGenbankDict

