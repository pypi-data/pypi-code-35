#!/usr/bin/env python3

"""
The input expected is a standards-compliant GFF3 file.  

  http://www.sequenceontology.org/gff3.shtml

Example of a gene with GO annotation:

  AAGK01000005	.	gene	161052	164192	.	+	.	ID=0ACE4B1023C0E198886936CD6BE3869B;locus_tag=TpMuguga_03g00084
  AAGK01000005	.	mRNA	161052	164192	.	+	.	ID=99A7DA3C31446D989D46A5B0C8EC5C0E;Parent=0ACE4B1023C0E198886936CD6BE3869B;locus_tag=TpMuguga_03g00084
  AAGK01000005	.	CDS	161337	162111	.	+	0	ID=470AEE91631AFCE9DBFD1CF9BA0E7365;Parent=99A7DA3C31446D989D46A5B0C8EC5C0E
  AAGK01000005	.	CDS	162179	163696	.	+	0	ID=470AEE91631AFCE9DBFD1CF9BA0E7365;Parent=99A7DA3C31446D989D46A5B0C8EC5C0E
  AAGK01000005	.	CDS	163868	164178	.	+	0	ID=470AEE91631AFCE9DBFD1CF9BA0E7365;Parent=99A7DA3C31446D989D46A5B0C8EC5C0E
  AAGK01000005	.	exon	163868	164192	.	+	.	ID=B1A06E24F7020FC4E92B7F2F1099D059;Parent=99A7DA3C31446D989D46A5B0C8EC5C0E
  AAGK01000005	.	exon	162179	163696	.	+	.	ID=BBBED213F1613EEBE471FA356BC818E4;Parent=99A7DA3C31446D989D46A5B0C8EC5C0E
  AAGK01000005	.	exon	161052	162111	.	+	.	ID=BD61FC870CA44840B1817F831519608A;Parent=99A7DA3C31446D989D46A5B0C8EC5C0E
  AAGK01000005	.	polypeptide	161052	164192	.	+	.	ID=99A7DA3C31446D989D46A5B0C8EC5C0E;Parent=99A7DA3C31446D989D46A5B0C8EC5C0E;gene_symbol=gcs-1;product_name=Glutamate-cysteine ligase;Ontology_term=GO:0004357,GO:0006750;Dbxref=EC:6.3.2.2

Note that if locus_tag features aren't defined on the mRNAs, the gene.id is used instead.

  
OUTPUT: 

From: https://pods.iplantcollaborative.org/wiki/display/DEapps/GoSeq

The input file is a tab-separated list of transcript IDs, differential expression status (0|1) (this script will do all 0s), transcript length and GO:IDs. Multiple GO:IDs are pipes separated (|). Differential expression status is indicated by either 0 or 1 where 0 means not differentially expressed, 1 is differentially expressed.

For example, a line in the input file will look like:

ENSG00000183798    0    3831    GO:0005575|GO:0005576|GO:0005578

Where there is no GO annotated to the transcript, the GO field can be left blank.

Formal documentation:

https://bioconductor.org/packages/devel/bioc/vignettes/goseq/inst/doc/goseq.pdf
  
"""

import argparse
import os
import re
import sys

from biocode import gff


def main():
    parser = argparse.ArgumentParser( description="Converts GFF3 files to use as input to R's goseq tool")

    ## output file to be written
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Path to an input file to be read' )
    parser.add_argument('-o', '--output_file', type=str, required=True, help='Path to an output file to be created' )
    args = parser.parse_args()

    (assemblies, features) = gff.get_gff3_features(args.input_file)
    ofh = open(args.output_file, 'wt')
     
    for assembly_id in assemblies:
        for gene in assemblies[assembly_id].genes():
            for mRNA in gene.mRNAs():

                mRNA_loc = mRNA.location()
                mRNA_length = mRNA_loc.fmax - mRNA_loc.fmin
                
                if mRNA.locus_tag:
                    display_id = mRNA.locus_tag
                else:
                    display_id = gene.id
                
                for polypeptide in mRNA.polypeptides():
                    go_ids = list()

                    for go_annot in polypeptide.annotation.go_annotations:
                        go_id = "GO:{0}".format(go_annot.go_id)
                        go_ids.append(go_id)

                    ofh.write("{0}\t{1}\t{2}\t{3}\n".format(display_id, 0, mRNA_length, "|".join(go_ids)))
                        
    print("INFO: Conversion complete.", file=sys.stderr)

if __name__ == '__main__':
    main()







