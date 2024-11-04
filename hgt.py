# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 20:28:17 2023

@author: Μάριος Ανδρικόπουλος
"""

import re
import statistics as stat
from Bio import SeqIO
from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
from ete3 import NCBITaxa
import time


class Hit:
    def __init__(self, organism):
        self.id = id
        self.organism
        
        
class Organism:
    def __init__(self, name, taxonomy):
        self.name = name
        self.taxonomy = taxonomy
        
def get_taxonomy(species_name):
    ncbi = NCBITaxa()
    taxid = ncbi.get_name_translator([species_name])
    
    if taxid:
        taxid = taxid[species_name][0]
        lineage = ncbi.get_lineage(taxid)
        names = ncbi.get_taxid_translator(lineage)
        taxonomy = [names[taxid] for taxid in lineage]
        return taxonomy
    else:
        return None

def parse_blast_xml(blast_results):
    print("\tParsing BLAST results...")
    with open(blast_results,"r") as blast_results:
        records = NCBIXML.parse(blast_results)
        results = list()
        for record in records:
            alignment_length = record.query_length
            for alignment in record.alignments:
                alignment_id = alignment.hit_def
                identity_list = []
                coverage_list = []
                protein_accession = re.findall("\|([^\|]*)", alignment.title)[2]
                hit_def = alignment.hit_def.replace("TPA_exp: ", "")
                parts = hit_def.split(" ")
                species = " ".join(parts[:2])
                if species == "synthetic construct":
                    continue
                species_ori = species
                # species = re.search("\[([^\[\]]*)\]", alignment.title).group(1)
                taxonomy = (get_taxonomy(species))
                # while taxonomy is None and len(species)>2:
                #     species = " ".join(species.split(" ")[:2])
                #     taxonomy = (get_taxonomy(species))
                if taxonomy is not None:
                    identity_list = list()
                    e_values = list()
                    coverage_list = list()
                    sorted_hsps = sorted(alignment.hsps, key=lambda hsp: hsp.query_start)
                    merged_hsp = sorted_hsps[0]
                    for hsp in sorted_hsps[1:]:
                        # Check if the current HSP overlaps with the merged HSP
                        if hsp.query_start <= merged_hsp.query_end:
                            # Merge the HSPs if they overlap
                            merged_hsp.query_end = max(merged_hsp.query_end, hsp.query_end)
                            merged_hsp.sbjct_end = max(merged_hsp.sbjct_end, hsp.sbjct_end)
                            merged_hsp.align_length = merged_hsp.query_end - merged_hsp.query_start + 1
                        else:
                            # Calculate identity and coverage for the merged HSP
                            identity = merged_hsp.identities / merged_hsp.align_length*100
                            coverage = merged_hsp.align_length / alignment_length*100
                            identity_list.append(identity)
                            coverage_list.append(coverage)
                            e_values.append(merged_hsp.expect)
            
                            # Set the merged HSP to the current HSP
                            merged_hsp = hsp
        
                    # Calculate identity and coverage for the last merged HSP
                    identity = merged_hsp.identities / merged_hsp.align_length*100
                    coverage = merged_hsp.align_length / alignment_length*100
                    identity_list.append(identity)
                    coverage_list.append(coverage)
                    e_values.append(merged_hsp.expect)
            
                    # Calculate summary statistics for identity and coverage
                    avg_identity = stat.mean(identity_list)
                    median_identity = stat.median(identity_list)
                    total_coverage = sum(coverage_list)
                    e_value_means = stat.mean(e_values)
            
                    
                    res_set = (taxonomy, int(avg_identity), e_value_means, protein_accession, species_ori, int(total_coverage))
                    results.append(res_set)
                    
    return results 

def is_continuous(numbers):
    if not numbers:
        return False  # Empty list is not continuous
    sorted_numbers = sorted(numbers)
    for i in range(len(sorted_numbers) - 1):
        if sorted_numbers[i] + 1 != sorted_numbers[i + 1]:
            return False  # Non-continuous numbers found
    return True

def check_for_order(results):
    sorted_by_id = results
    max_id = sorted_by_id[0][1]
    if max_id < 30:
        return None
    min_id = sorted_by_id[-1][1]
    top_hit = None
    top_genus = None
    non_fungi = list()
    top_match = False
    all_match = False
    metarhizia_check = list()
    metarhizia_top = True
    other_metarhizia = False
    brunneum_check = False
    offset = 0
    for j in range(len(sorted_by_id)):
        i = sorted_by_id[j][6]
        if top_hit is None and sorted_by_id[j][0][i] != "Metarhizium":
            try:
                top_hit = sorted_by_id[j][0][i-2]
                top_genus = sorted_by_id[j][0][i]
            except:
                continue
        if sorted_by_id[j][0][i] == "Metarhizium":
            metarhizia_check.append(j)
            if sorted_by_id[j][0][i+1].find("brunneum")<0:
                other_metarhizia = True
            else:
                brunneum_check = True
            if len(metarhizia_check) == 1 and metarhizia_check[0] != 0:
                metarhizia_top = False
        if len(metarhizia_check) == 0:
            offset = 0
        else:
            offset = metarhizia_check[-1]
        try:
            if sorted_by_id[j][0][i-2] == "Hypocreales" and j<=4 + offset and j > offset:
                top_match = True
    
            if sorted_by_id[j][0][i-2] == "Hypocreales" and j > offset:
                all_match = True
        
            if sorted_by_id[j][0][4] !=  "Fungi" and sorted_by_id[j][1] > 30:
                non_fungi.append(j)
        except:
            continue
    return top_match, all_match, non_fungi, top_hit, top_genus, sorted_by_id, metarhizia_top, is_continuous(metarhizia_check), metarhizia_check, other_metarhizia, brunneum_check

def align_tabs(input):
    with open(input, 'r') as input_file:
        # Read the lines from the input file
        lines = input_file.readlines()

    # Initialize a list to store the aligned lines
    aligned_lines = []

    # Determine the maximum number of tab-separated values in any line
    max_num_values = max(len(line.split('\t')) for line in lines)

    # Iterate through the lines and align the values
    all_values = list()
    for line in lines:
        # Split the line into tab-separated values
        values = line.rstrip('\n').split('\t')
        all_values.append(values)
    max_length = list()
    for i in range(max_num_values):
        all_sub = list()
        for val in all_values:
            all_sub.append(val[i])
        lengths = [len(sub) for sub in all_sub]
        max_length.append(max(lengths))

    aligned_values = []
    for values in all_values:
        aligned_lines = list()
        for i in range(len(values)):
            values[i] = values[i] + " "*(max_length[i] - len(values[i]))
            aligned_lines.append(values[i])
        aligned_values.append(aligned_lines)

            
    aligned_lines = []
    # Join the aligned values with tabs and add the line to the aligned_lines list
    for aligned_value in aligned_values:
        aligned_line = '\t'.join(aligned_value)
        aligned_lines.append(aligned_line)

    # Open the output file for writing
    with open(input, 'w') as output_file:
        # Write the aligned lines to the output file
        output_file.writelines('\n'.join(aligned_lines))

    # Print a message to indicate that the alignment is complete
    print("Tab-separated values alignment completed.")

    
        
fasta_input = open("v275not_metarrhizium.fasta", "r")
output_file = open("test.txt", "a")

records = list(SeqIO.parse(fasta_input, "fasta"))
fasta_input.close()
for record in records:
    print(f"Working with {record.id}")
    # print("\tBlasting...")
    # result_handle = NCBIWWW.qblast("blastp", "nr", record.seq, hitlist_size = 100, expect=1)
    
    # with open("blast_results.xml", "w") as save_file:
    #     save_file.write(result_handle.read())
    #     result_handle.close()
    # print("\tDone!")
    try:
        results = parse_blast_xml(f"{record.id}.xml")
    except ValueError:
        with open('blast_results.xml', 'r') as file:
            file_contents = file.read()
        modified_contents = file_contents.replace("CREATE_VIEW", '')
        with open('blast_results.xml', 'w') as file:
            file.write(modified_contents)
        print("\tFixed BLAST XML...")
        results = parse_blast_xml("blast_results.xml")
    except FileNotFoundError:
        continue
    results_filtered = list()
    
    for j in range(len(results)):
        i=-1
        while re.search("\s", results[j][0][i]):
            i-=1
        results[j] = results[j] + (i,)
        if results[j][1] > 0:
            results_filtered.append(results[j])
    if len(results_filtered)<1:
        print("\tLess than 3 significant hits!")
        output_file.write(f"{record.id}\n")
        output_file.write("\tLess than 3 significant hits!\n")
        
        with open(f"{record.id}.results", "w") as result_file:
            string_res = ""
            for res in results:
                string_res += f"Order: {res[0][res[6]-2]}\tSpecies: {res[4]}\tID: {res[3]}\tIdentity: {res[1]}\tCoverage: {res[5]}\n"
            result_file.write(string_res)
        continue
    
    results_filtered = sorted(results_filtered, key=lambda tup: tup[1], reverse=True)
    ver = check_for_order(results_filtered)
    output_file.write(f"{record.id}\n")
    string = "\t"
    if ver is not None:
        if (not ver[6]) or (not ver[7]):
            string += "####METARHIZIUM REPORT####\n\t"
        if not ver[6]:
            string += "[!!!] Metarhizium not top result.\n\t"
        if not ver[9] and ver[10]:
            string += "[!!!] Only in M. brunneum.\n\t"
        if not ver[10]:
            string += "[!!!] Not in M. brunneum.\n\t"
        if not ver[7]:
            pass
            # string += "[!]   Metarhizium hits not clustered together.\n\t"
        if (not ver[1]) or (not ver[0]):
            string += "####HYPOCREALES REPORT####\n\t"
        if (not ver[0]) and (ver[1]):
            pass
            # string += f"[!!]  Hypocreales (excluding Metarhizia) not in top 5 results. Top result in {ver[3]}: {ver[4]}\n\t"
        if not ver[1]:
            string += f"[!!!] Hypocreales (excluding Metarhizia) not in any results. Top result in {ver[3]}: {ver[4]}\n\t"
        if len(ver[2])>0:
            string += "####NON-FUNGI REPORT####\n\t"
            string += "[!!!] Significant non-Fungi results.\n"
        print(string)
    
    if True:
        string = string[:-1]
        # output_file.write(string)
        with open(f"{record.id}.results", "w") as result_file:
            string_res = ""
            for v in ver[5]:
                if v[0][-1] == "synthetic construct":
                    continue
                string_res += f"Order: {v[0][v[6]-2]}\tSpecies: {v[4]}\tID: {v[3]}\tIdentity: {v[1]}\tCoverage: {v[5]}\n"
            result_file.write(string_res)
        align_tabs(f"{record.id}.results")
output_file.close()