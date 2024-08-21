#!/usr/bin/python
import os
import sys
import re
import csv
import argparse

### Example Command
# python merge_mnbc_taxonomy.py --mnbc_results_infile /home/AGR.GC.CA/muirheadk/mnbc_tools/barcode01.txt --taxonomy_file /home/AGR.GC.CA/muirheadk/mnbc_tools/taxonomyBafull.txt --output_dir /home/AGR.GC.CA/muirheadk/mnbc_tools/output

parser = argparse.ArgumentParser()

mnbc_results_infile = None
taxonomy_file = None
output_dir = None

parser.add_argument('--mnbc_results_infile', action='store', dest='mnbc_results_infile',
                    help='input MNBC results file.')
parser.add_argument('--taxonomy_file', action='store', dest='taxonomy_file',
                    help='The reference MNBC taxonomy file.')
parser.add_argument('--output_dir', action='store', dest='output_dir',
                    help='output directory as input. (i.e. $HOME)')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')

results = parser.parse_args()

mnbc_results_infile = results.mnbc_results_infile
taxonomy_file = results.taxonomy_file
output_dir = results.output_dir

if(mnbc_results_infile == None):
    print('\n')
    print('error: please use the --mnbc_results_infile option to specify the input fasta file path list as input')
    print('mnbc_results_infile =' + ' ' + str(mnbc_results_infile))
    print('\n')
    parser.print_help()
    sys.exit(1)
if(taxonomy_file == None):
    print('\n')
    print('error: please use the --taxonomy_file the reference MNBC taxonomy file as input')
    print('taxonomy_file =' + ' ' + str(taxonomy_file))
    print('\n')
    parser.print_help()
    sys.exit(1)
if(output_dir == None):
    print('\n')
    print('error: please use the --output_dir option to specify the output directory as input')
    print('output_dir =' + ' ' + str(output_dir))
    print('\n')
    parser.print_help()
    sys.exit(1)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# RefSeq assembly ID      taxid.species   taxid.genus     taxid.family    taxid.order     taxid.class     taxid.phylum    taxid.superkingdom      Organism name
#GCF_000146165.2 70863   22      267890  135622  1236    1224    2       Shewanella oneidensis MR-1 strain=MR-1
i = 0
refseq_id_dict = {}
taxid_species_dict = {}
taxonomy_input_file = open(taxonomy_file, "r")
csv_reader = csv.reader(taxonomy_input_file, delimiter='\t')
for row in csv_reader:
    if(i != 0):
        print(row)
        (refseq_assembly_id,taxid_species,taxid_genus,taxid_family,taxid_order,taxid_class,taxid_phylum,taxid_superkingdom,organism_name) = row
        refseq_id_dict[refseq_assembly_id] = [refseq_assembly_id,taxid_species,taxid_genus,taxid_family,taxid_order,taxid_class,taxid_phylum,taxid_superkingdom,organism_name]
        #taxid_species_dict[taxid_species] = organism_name
        
        if(not(taxid_species in taxid_species_dict)):
            taxid_species_dict[taxid_species] = []
            taxid_species_dict[taxid_species].append(" / ".join([refseq_assembly_id,organism_name]))
        else:
            taxid_species_dict[taxid_species].append(" / ".join([refseq_assembly_id,organism_name]))
            #sys.exit()
    i += 1

#sys.exit()

basename = os.path.basename(mnbc_results_infile)

filename = os.path.splitext(basename)[0]

csv_writer_file_handle = open(os.path.join(output_dir, filename + ".tsv"), "w+")
csv_writer = csv.writer(csv_writer_file_handle, delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE)
csv_writer.writerow(["Read","Genome","Species","Genus","Family","Order","Class","Phylum","Superkingdom","ref_seq_taxonomy"])

#Read    Genome  Species Genus   Family  Order   Class   Phylum  Superkingdom
#d207972b-0a98-42fd-b4c3-d3e6f791d00b    null    251701  286     135621  72274   1236    1224    2
#95d02c14-4a30-4e97-8f52-b8ec53094bb7    GCF_018739385.1 1405    1386    186817  1385    91061   1239    2
i = 0
mnbc_results_input_file = open(mnbc_results_infile, "r")
csv_reader = csv.reader(mnbc_results_input_file, delimiter='\t')
for row in csv_reader:
    if(row == []):
        continue
    if(i != 0):
        print(row)
        (read,genome_id,tax_species,tax_genus,tax_family,tax_order,tax_class,tax_phylum,tax_superkingdom) = row
        if(genome_id == "null"):
            #print(row)
            #sys.exit()
            if(tax_species in taxid_species_dict):

                #print(row)
                #sys.exit()

                taxonomy_species = ";".join(taxid_species_dict[tax_species])
                csv_writer.writerow([read,genome_id,tax_species,tax_genus,tax_family,tax_order,tax_class,tax_phylum,tax_superkingdom,taxonomy_species])
        if(genome_id in refseq_id_dict):
            (refseq_assembly_id,taxid_species,taxid_genus,taxid_family,taxid_order,taxid_class,taxid_phylum,taxid_superkingdom,organism_name) = refseq_id_dict[genome_id]
            csv_writer.writerow([read,genome_id,tax_species,tax_genus,tax_family,tax_order,tax_class,tax_phylum,tax_superkingdom," / ".join([refseq_assembly_id,organism_name])])
    i += 1


