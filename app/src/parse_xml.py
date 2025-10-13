import xml.etree.ElementTree as ET
import pickle as p
import pandas as pd
import re, os

TEMPFILE = "tmp.p"

def parse_xml(file_path, idx):
    '''Parse InterProScan XML output for RdRp and Helicase domains'''
    if idx == 0:
        data = {}
    else:
        data = p.load(open(TEMPFILE, "rb"))

    tree = ET.parse(file_path)
    root = tree.getroot()
    for child_0 in root:
        tmp = {"id": None, "seq": None, "rdrp": [], "helicase": []}
        for c1i, child_1 in enumerate(child_0):
            if re.findall(r"sequence", child_1.tag):
                '''Sequence has actual protein to extract'''
                tmp["seq"] = child_1.text
                try:
                    tmp["id"] = re.findall(r"[A-Z]{1,2}[0-9]{5,6}|[A-Z]{2}_[0-9]{6}|SRR[0-9]{7,8}|[a-zA-Z]{4,6}[0-9]{6,9}", child_0[c1i+1].attrib["id"])[0]
                except: 
                    # tmp["id"] = "unknown"
                    tmp["id"] = child_0[c1i+1].attrib["name"]
                    print(f"Unknown ID in {file_path} for {child_0[c1i+1].attrib}")
            
                if not tmp["id"] in data.keys():
                    data[tmp["id"]] = {"rdrp_name": None, "rdrp_start": None, "rdrp_end": None, "helicase_name": None, "helicase_start": None, "helicase_end": None, "rdrp_domain_seq": None,  "helicase_domain_seq": None}

            elif re.findall(r"matches", child_1.tag):
                '''Matches has loci and domain names'''
                if not child_1.text == None:
                    for child_2 in child_1:
                        match_type = ""
                        '''HMMER3 MATCHES'''
                        if re.findall(r'hmmer3-match', child_2.tag):
                            for c3i, child_3 in enumerate(child_2):
                                if re.findall(r'signature', child_3.tag) and not "signature-library-release" in child_3.tag: #  [(i.tag, i.attrib, i.text) for i in child_3]#
                                    for c4i, child_4 in enumerate(child_3):                                        
                                        if "desc" in child_4.attrib.keys():      
                                            if re.findall(r'polymerase', child_4.attrib["desc"].lower()):# and not re.findall(r'superfamily', child_4.attrib["desc"].lower()):
                                                match_type = "rdrp"
                                            elif re.findall(r'rdrp', child_4.attrib["desc"].lower()):
                                                match_type = "rdrp"
                                            elif re.findall(r'helicase', child_4.attrib["desc"].lower()):
                                                match_type = "helicase"
                                            if not match_type == "":
                                                if match_type == "rdrp":
                                                    data[tmp["id"]]["rdrp_name"] = child_4.attrib["desc"]
                                                    data[tmp["id"]]["rdrp_start"] = child_2[c3i+2][0].attrib["start"]
                                                    data[tmp["id"]]["rdrp_end"] = child_2[c3i+2][0].attrib["end"]
                                                    data[tmp["id"]]["rdrp_domain_seq"] = tmp["seq"][int(data[tmp["id"]]["rdrp_start"]):int(data[tmp["id"]]["rdrp_end"])]
                                                elif match_type == "helicase":  
                                                    data[tmp["id"]]["helicase_name"] = child_4.attrib["desc"]
                                                    data[tmp["id"]]["helicase_start"] = child_2[c3i+2][0].attrib["start"]
                                                    data[tmp["id"]]["helicase_end"] = child_2[c3i+2][0].attrib["end"]
                                                    data[tmp["id"]]["helicase_domain_seq"] = tmp["seq"][int(data[tmp["id"]]["helicase_start"]):int(data[tmp["id"]]["helicase_end"])]
    p.dump(data, open(TEMPFILE, "wb"))


def prepare_output(out_dir):
    data = p.load(open(TEMPFILE, "rb"))
    df = pd.DataFrame.from_dict(data, orient="index")
    breakpoint()
    df_allfields = df.dropna()
    df_allfields.to_csv(f"{out_dir}/data_nona.csv")

    df_missing = df[~df.index.isin(df_allfields.index)]
    df_missing.to_csv(f"{out_dir}/data_missing.csv")
    print(f"WARNING: missing {[i for i in df_missing.index]} due to one or more missing protein domains")

    df_allfields["acc"] = df_allfields.index
    rdrp = df_allfields[["acc","rdrp_domain_seq"]].values.tolist()
    helicase = df_allfields[["acc","helicase_domain_seq"]].values.tolist()

    with open(f"{out_dir}/rdrp_seqs.fasta", "w") as f:
        [f.write(f">{i[0]}\n{i[1]}\n") for i in rdrp]
    with open(f"{out_dir}/helicase_seqs.fasta", "w") as f:
        [f.write(f">{i[0]}\n{i[1]}\n") for i in helicase]


if __name__ == "__main__":
    '''Init'''
    in_dir = "./tmp/interpro_xml/"
    out_dir = "./tmp/interpro_parsed/"
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    files = os.listdir(in_dir)

    '''Process'''
    for idx, fpath in enumerate(files):
        parse_xml(f"{in_dir}/{fpath}", idx)
    prepare_output(out_dir)

    '''Tidy'''
    os.remove(TEMPFILE)
    
