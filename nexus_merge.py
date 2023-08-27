# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 14:34:30 2023

@author: Μάριος Ανδρικόπουλος
"""

from Bio.Nexus import Nexus
from Bio import SeqIO
import glob
import argparse
import subprocess
import os


perl_rename_path = "/".join(os.path.realpath(__file__).split("/")[:-1]) + "/cool_rename.pl"
parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", type=str, default="../MITO/NEX/MITO.nex")
parser.add_argument("-i", "--input", type=str, default="../MITO/NEX/*cor.nex")
parser.add_argument("-t", "--translate",type=bool, default=False)
args = parser.parse_args()

out=str(args.output)
inp = str(args.input)
trn = bool(args.translate)


f_out=out.replace('nex', 'fasta')

file_list=glob.glob(inp)


nexi = list()
for fname in file_list:
    print(f"Working with {fname}:")
    output_file = fname
    if trn:
        output_file = fname.replace(".nex", "_ren.nex")
        command = ["perl", perl_rename_path, "-i", fname, "-o", output_file]
        try:
            subprocess.run(command, check=True)
            print("Rename succesful")
        except subprocess.CalledProcessError as e:
            print("Error running Perl script:", e)
    print(fname)
    
    nexi.append((fname,Nexus.Nexus(output_file)))
    

combined = Nexus.combine(nexi)
combined.write_nexus_data(out, interleave=False)
combined.export_fasta(f_out)



