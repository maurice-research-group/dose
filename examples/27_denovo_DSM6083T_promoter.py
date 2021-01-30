'''
Example 27: De novo origins of Pseudomonas balearica DSM 6083T 
promoters.

Reference: Usman, S, Chua, JW, Ardhanari-Shanmugam, KD, Thong-Ek C, B, 
V, Shahrukh, K, Woo, JH, Kwek, BZN, Ling, MHT. 2019. Pseudomonas 
balearica DSM 6083T promoters can potentially originate from random 
sequences. MOJ Proteomics & Bioinformatics 8(2): 66‒70.

In this simulation,
    - 1 population of 100 organisms
    - each organism will have 1 chromosome of only 4 bases (A, T, G, C)
    - entire population will be deployed in one eco-cell (0, 0, 0)
    - 10% background point mutation on chromosome (PMID 14616055, 
    27185891)
    - no organism movement throughout the simulation
    - fitness is calculated as average pairwise alignment of organism 
    chromosome to known sequences
    - the lowest dectile of the organisms (by fitness) will be removed 
    if there are more than 50% population remaining after removal; or 
    else, a random selection of 10 organisms will be removed.
    - a random selection of remaining organisms after removal will be 
    replicated to top up the population to 100 organisms
    - 100 generations to be simulated
'''
# needed to run this example without prior
# installation of DOSE into Python site-packages
try: 
	import run_examples_without_installation
except ImportError: pass

import copy
import random

# Example codes starts from here
import dose

from Bio import Align
aligner = Align.PairwiseAligner()
aligner.mode = str('global')

known_sequences = ["GTATAGGGTGTGACGCCTGCCCGGTGCCGGAAGGTTAATTGATGGGGTTA",
                   "TCTTTTGATGTAATCCAATACATTTCCCCCAGATTGTCGAAGTGTTGAGC",
                   "CCTGGTTGTCGAGCAGGAAATAGGCGAGGTAGATCACCGCCAGCATGAAG",
                   "CTGGCTTTGCATCGCCATGCCTTCGCCAATCTGATCCCGACTGGACTTTT",
                   "CCTCTCGACGGTTTCCAGCAGCGGAACGAGCAGTGATAATGCCGGCGTTT",
                   "TTTTCTTGCCTGTTGCAAGTGAAACTTGCGCAAGTTTATTAGGCTCTAAA",
                   "GCATGCCCATGCTGGACAGAGGTCTGAAGCAACGTATGGTCGGGGCGCTG",
                   "GGTGGTTCTTGAGTATTCGAGCCAGCTATGGGGCTACCTTGAGTCAAACC",
                   "TAGGCGCTCCTTGACTAGAAAAATATTCTAGAACTATATTCCAGCCGGCC",
                   "CGGTTGCCAGTAAGCGAGGCGCAGCCGGCTAGCATGCTGTAGCTCAGGCC",
                   "GCGCCAGGCTCTGAAAGGGAACGGCGATGCGCTTTATCATGGCCCGAATT",
                   "TGAAGAAAGGGATGGATAGATTGGGGGTACGATTTACATTCATGTTAGCC",
                   "TTATGCTGCAGTTTGCTGCGGCCGGTATGTGCAGTATACAGCACAGATTT",
                   "GATTGTTGGTGTCGATCAGGCGATTCCAATAGATGCCCTGCGGGACTTCC",
                   "GCGAGATTGGGCTTTGGAACTCCGGAATCGCCTGTCGAATCAGTAGCGGC",
                   "GGTCCATCTTGTCCTGGAAGGCGTGCAGCACCGGCATGATCGAATCGAAG",
                   "TTTTTCTCAAAACATTAGTGCTGCAAAGCAATAATCGAGGGCCGCATGAG",
                   "CGGGGCATGACAAACATGCCGGGGGTCGTTAACATGCGCCCCCGAGTCCC",
                   "GGCGATTGTAGAGAAGCCAAGGGTGCAGGTCAATTTCCAACCGGCACGTC",
                   "CACCGCCTGGGCTGACAAGAAGCAGCTGGCAGCGTATATCCAGCGCATCG",
                   "TCGTGGCTGGCCAGCACCAGCCCGGACAGCAGAATCAGCAGCACGCCGTA",
                   "GGTCACGTTTGGCGGTGGAAGGGCGCAAATTGGCGAAATTGACGTTAATC",
                   "GGCTGACGGTGGAAGGGTGTCCTGTTACGTATGTTCACCGGCATTCCACC",
                   "GCGATCCGGTTTTCCAGAATTGGCAGCAACCTGTTAAAAATCAAATACTT",
                   "AAGGTGACGATCAGCTGGAGTTTGCCAGCTATCCTGCCGCCCAACTCGAG",
                   "GCTCGTAATGGTGGCTGATCTCGGCGCGACGCTCGAGAATCGACTCGATG",
                   "GCGTTTTTACGCGTGCCCAGGCGGCCCGTGAACATTTCAGCAAAATACTG",
                   "TTTTGTTGTTGAGCAAAAAATTGCTTCGGAAATATATGAGAATCTGTCAT",
                   "ACTGGAACTGGAAGTCACGCGCCTTCTGCTTGAATTCCAGTTCGAGGCGC",
                   "GTGCCGCCTCAAGTTGAATTGAGACGGTCATGGATAAGTTGGCGAAAGCG",
                   "ATGCTTGATGCGGTAACCCAGCGCCTCGGCATAGTTGACGTCAGCGGTGG",
                   "CTGTATGGAAGGGCCATCGCTCAAACGGATAAAAGGTACTCCGGGGATAA",
                   "TATTGTGGGCAGCTCGCATGCCTTCCATGTATATGAATCACCCACTGAGA",
                   "CGGCCCAGGATTTGTTGCGGCCGAAGAAGCGGGTCATGATGCTGAGCATG",
                   "CGGGATTATTTGCTACCCAATGGAAGATGGGATTTCGAATTTAGGGGGCG",
                   "GTTACAACACGTGCCATAGGTATATGAATCCTTGTCGAATCGACATATAC",
                   "GGCATGTGCCAGCTCAGGTACTGGCCCAGTACCTTGGCGCTCATCCAGGC",
                   "ATGATCTGAAGATGACAAAAATGTAATCTTCCAATCAATTTTGTCGTAGG",
                   "TGATGGACTTCGAGATGGTCACCATCCGGGAAGATGTCAGTCTGGAAGTG",
                   "AGTTGTTGGTGCCGAAGAGGGTGAGTTCAGCTAATTCCTCAAAGAAGCTC",
                   "GGACGGCCAGTTGAAGGTCCCGACATTGCCCGGGTAGATCAGCGAGCCCT",
                   "GTGACGGCGGTTTGAGCTGATTGGGGGTTTCGGGTAGACTACGCTCCCGT",
                   "GGTTGGAGGTGTTGGTGCAGCTGGTGATTGCGGCGATGATCACCGCGCCG",
                   "TCTCTGATTGCTGCAGCTGTGTGCATAGGGATAATGCCTCGCTTTTCCAT",
                   "CCCATTTTGATAAAGAGGCAGATTCCTTGTCAGATTGGGAAGATGTAACG",
                   "TATTTTCGCAAGAACCGCACTGCATTGACTAAAAAGTAAGTGCAGCAATC",
                   "GAATTGAGCTGGCGCCGTTACTCGCGGAACAGATTCTCCCGGCACTGGCA",
                   "GCCTGACTTGTTGATCAGCGTGGTCATACCGGCCTACAACTACGCGAAGA",
                   "TTCTTGATCACGCTGTCTTCCCTCGGATCGATGATCAGGCGGCCCGTGCA",
                   "ATGGCCTTTGGCTCTCCGTGCGCGTTAGCGATAGTCGCTGTAACCGTCGA",
                   "TCCAATCCTTGACGGAGTCGAGCGGAGCCGTGAGTACAACCGCCCACCAC",
                   "CGATTGCCGGGGACATGGCCGCCCAGCTGTACGATCTGACCAAGCTGGCG",
                   "GCACATGACTCAACGTCCGCTTATTTCAATAACATTCAAGCACTGAGGAC",
                   "GAACTTGTGGAAGCCGGAGAACTGCGCGACATCCTTCGTGAATCGGAAGC",
                   "GCGGGTGGGATAGACGCAAGTTATAGAGACCAAATATTCTGGCAGTGGTG",
                   "TAATTTTGGCTGTATGAGAGCACGGCTAATAGAGTCGCTAAATACATCAA",
                   "GGCAATTGCCTGCTTGACCTGCGTCGCGGTGTATTCAGCGACTTCGAGAC",
                   "TAATTGTGAGTGAAGGAAAGCTTTCGAGTGAAACTGATATCGCGGGTGGG",
                   "ATGATCTGACGTACCGCGGTGATGCCGTCCATCATCGGCATCTCGTAATC",
                   "CAATTGATCGAAGGCGCTGAGCTGAACGACATGATCCGTCAGAGTCGCGC",
                   "GAGATGGCAAAGGCACAAGAAAATCTCAAAAAAATGCAGGAGCAAATGAG",
                   "CGATTTTTTGGGCGATTTCTGAAGCGCTTTAAGCTTACAAAAATGTAATC",
                   "GTGCTTGGGGGTTCGACAAAGCGACCTGAGCTGCTATGATGCGCGCCGCT",
                   "GAGTTTTGGAGTCTTTTGTCGGTCTGCGTGATAAGTCAGTCTTGGCAAAT",
                   "ACGTTGTAGTCAACCACTCGTTTGACAGCTACAAGAACCTTCATGGATTC",
                   "TTGTGACAGAAAATATATGTCCACCACGGTAGTGTCTTGTTGAAACTTTC",
                   "CTACTGATATGATGGGCACCTCGCGATCGCGAGGTGGAATTACAATTTGC",
                   "ACTTGATTTGAACAGGTTCAAGCCATGCTGATTATCCCCGCTATCGATCT",
                   "GCAGGTTGGCTGCCACACTGATGAGCCGCGAAAGTGAATATGCTAAGAAG",
                   "GCCTGCCTGTTGCGATACGGAGTCGCTGGCCGCTTATCCTTACGGGTTAC",
                   "GCAACTTGTAGTCTTCACCACGGGACTTGAATACTTCGATCACCTGAGCA",
                   "GACTGCGAGGTTGGCGGAGCCATTGCCGAACCGATATGGTCCTATGCGCG",
                   "CATGGAAATGGAGACCGGAATGTCGAGGATCACATCCAGGTTCGGCCCTT",
                   "GCATGAGTGATGGCTTTCTAGAAGGCAGAGAAATTGAATGTCCTTTGCAT",
                   "AACAGAATTGGTTGTTCCTGGTAGTGATATATTTTATCCGCCAACAGAAA",
                   "CTCAATGTTGGCACCTTCGAACGGCTCGACCCGATAGAACAGCGTCTCCT",
                   "GGCGACGGGTTACTGATACATGACCAGAACGCGTTAGATTTGGACCGCGA",
                   "CGACCCAAGGAAGTGACATGGCCGAGAATCTGATTGAAATCCGCGACCTC",
                   "CGGGCTCAGCAGTTGCCAGTGAAATGCCGGCGGCTAGGATTTGTGTCTCT",
                   "GCGAAGCGTTTTAATACGGCCGGGGGTGAGACCGTAAATTTCTTTCAGCT",
                   "GACTTGGCGGCCAGCTGCGGTGGTGAGGGGATGATCGGTGCCGCCCAGAC",
                   "CGTTGCAAGTGAAGGGAAGTCGCGCATTGTAAAGCAAGAACCCGCCTGGG",
                   "CAGCTTGTCGGCATCAGGATGAGGTTCGGTAGAAACGACCTCACCGACCA",
                   "TGATGGACACGCGACAGGCCCCGGCGCGCGAGAATCTCGTCTGGCTTGGC",
                   "GGGTGTGACGCCTGCCCGGTGCCGGAAGGTTAATTGATGGGGTTAGCGCA",
                   "CGGCTGGAATGCCTGATATTTCGCGTCTTTATCATCGGATTCAGGGGTAA",
                   "TGTTGGCGGCCGGGTGGCTGAGGCTCAGGTAAAAGGTCAGGTAGATCAGG",
                   "AACGGCTTCTGGAAGACATCTGGCACGCCCTGGATAACACTCCGAAACAG",
                   "TGGCGTGATGCCATGAAGCCGGTCTGGAAGAAATTCGAAGGCGAAATCGG",
                   "ATCGACCGGGCATTGCCAAAGCGCCAGAGACCTGTATAAATAGCCAGCCC",
                   "TTCTTTGTTTTTTCTTGCTCTAATTTGAGTTCAGTGTATTTGTTTAGAGT",
                   "TGGTGCAGCTTGTGGTGCTTCAGTGGCTGCGGAGTCTACTAGGGTGATTT",
                   "ACCCCTAGCCTTGGCACATGCAGCGGGACCTGGATAAGCTTGTCGAAGTA",
                   "ACCAAATATTCTGGCAGTGGTGGTCGAAGATCGATAGCTTCTGGTTGTGG",
                   "AGCTGTTTGGCGGTCGCCAGCTCACCGAGGAAATTCAGCGTCGCTACGGG",
                   "TGATGTTTTTTTTAATTCTAGCTCTGGTGGAGAGTTGATTTTCCCAAATT",
                   "CTTTGAATAGTTGATCATTTCGCTTGGGTAAGCGGATAATGCCCAGCATC",
                   "CTGAATTGTCCGATGAACGGTGTCTTCAATCTCATCCCTGAGCAGCGACC",
                   "GCGAGAGCTTTATCGACAAGTTCGTCGAGCTGCATAACGTCGACTACCAG",
                   "CAGGTTGTCGCAGCCAGAGGAGGCGGAGATGTACTTCAACCGCTCGCTGC",
                   "TGTAATGCGTTTACAGTCCGTTGGAACCCTTGAGTATGCTCACCCAAGCT",
                   "GGCCGGGTTTGCCGTCATAGCGATAGCCGTTCTCCAGAATCAGGTAACGA",
                   "CGGTGAGTTCAGAGTGCTCCGGCGAAACATAAAATCGGTTCAGGCCGTCG",
                   "GAATGCTTGCCGCTTGGCGCGCCCGGGGGTAGGGTTGCCTGCCCCGGCTT",
                   "TACCTTCCAGGTTGGATTGATTCGCGGGGCCCCAGAGAATCAGACGCGCG",
                   "GCCACGAGGTTCTTGGCGATTTCGGCTGCGTTGTCATAGTCACTGTCGGC",
                   "TACTCCGGTGTATTGTCGTCGGGCGACTCGGTGATCAATTCGGTCAAGAG",
                   "TCACCGTTTGATCGACGGCAAAGAGGCGGTAACCTTCCTGGTCACCATGA",
                   "GTCTCTGTTCTTTTATACAGTGCCTGGGATTATATACAGTGCATGCGGGT",
                   "TCTTTTTTGTCAGCCATGCCCGGGTTGCGCATAATGGCCAGTCGCTTGCA",
                   "TATCGAGATGTATTGGTTATCACCTTCAGTAAGCGATGATTAATAAATCC",
                   "CCTGCTCCGGGTTGTAGCGATAAACACTCACTTGCAACATATCGGTGACC",
                   "CCCGCGCCGCTTGAAGCGCCGACTCAAGGCCGTCGATAATGCCAAGTTTT",
                   "GGATGAGTGGTGACAAAGCTTGTGGTTGTGCGAATAGCGTTGCGCCGTCG",
                   "AGTTGTTGCGCGATGCGCTGATACAGCAACAGATTGGTCATGGTCCCTGC",
                   "ACGACGGTATTTGGACACCCTCAACCATTGTTGTTAAAGTCCCGTCGCCA",
                   "ACTTGGTTCCCGCCAGCAAGGCACCGAGATCCAATGAATAGACGACGCTG",
                   "AGTTGCCTTTGCCTATATATACGGGCACCTCGAATAACGCGAGGTTTTCA",
                   "GAGCCGTCGCCTTGCCGATGACGGAGCGGTGCGATAGAACGCCAGCCTTC",
                   "GCGGATTATTGATATCCAGCGAGTCGTGGTAGAAGGCGGAAAGTGCACCC",
                   "TTTGTTATGTGATTAAATGCCAAAACTGCCTATTTAAAAAATACCTTTGT",
                   "ATTTCGAAGAGCGATTAATTAATGAAGGTTATAAGCCAGACATCACCAAT",
                   "ACCGCTGGTTGGGTGGCATGCTGACCAACTACAAGACCATTCGTGCTTCG",
                   "TGCTGGTTTGCGACGATCCGCCTGGAGGGTACAAAAAAGCGCTCCTTATG",
                   "CAGTTTTGAACGATGTGCAGATGCCTGGTTTTACTCCAGGCTCCAGGCCT",
                   "TTGAGAAAGTTGAACAGCGCACCGGGCCGCTCGGGAAACTCGAAGCGCAG",
                   "AGAAGATGATGAAGAAGGTCACCGGCAAAGGCGGTATGACCAAAATGATG",
                   "GAGATATTGCATGACACTCTCCTTTGCAGCGCGCGATTATCCGCAGCGCG",
                   "AAGCCTGTTTGCCTGTACTGAAAATTGTGTACAGTGATGGCCAAATGATG",
                   "TGGTTGGTGAACACGCAGATGCTGCCGGCGATGTTCAGGGCGGTTTCGGC",
                   "GCTTTGCCAGGCCCCAGCAGCGTGACGCCGATATTGCCGATACCGGCAAA",
                   "AAACTTTTTGATATTGGCCTTGCTGGTCGAAAAATAGCCGACTAGACTGC",
                   "GTCCGTATTGGCCAGGTGATTGATCAGCGCCCGATAGAACTCCGACTTGC",
                   "TTATATGGTTGGAATGAGTCGTTTCCTCTCAAATTAGCCTATCGACGAAA",
                   "GCGCTGATCGACAGCCAGGGTCCGACCAATCCAATGCGCATCGTCGCGGT",
                   "CCGCTTGTAGCCGGTCAGGTTGTCGTGCATATGCTGCATGACCTGCTCCT",
                   "AGGCTTTGCGAGAGGAACTGTCAGTGAACTACAACCGTAGCAAGGGACTT",
                   "CTGCTGGAGAAGCATGAGTTGGCGGCCGGTATCCTTGGCATGATCAATGG",
                   "TTTGTCATACATTGCCGCTTGGTCCGGCAAAAAATACATTCCGTCTCTCA",
                   "CTACCGGATAGTTGAACCGGTGGGGCCCTGCTCCTATACTCGCCGCGCTT",
                   "CCAGTCATCGATTTGATGTCACGCTGGAGGTCGATCTCATTGAGGAGCTG",
                   "CTCGAGCAGTTGGTCGCCAAACTAGGCGTAAAGGTCGAATTGCTGCATAC",
                   "CGTTGGGTGAAAAATAGAGAAGGCTGTTATATAAGTAAATAAGCGAATTT",
                   "AATACCCGCTTTGAACTGGCGGGTCGATTTAGGCGAGAATGCGCGGCTTT",
                   "CACGTGCGTGACGGTCTTGATCTCAAGCGCATGATGATCACCGTCTGGCT",
                   "CGGCGGTCTGGATGGTCATGTGGATGCAGCCGAGGATCTTGGCGCCCTTG",
                   "GTCTTGCCGACCCCGGTGGGGCCGATCATCAGAATGTTCTTCGGGGTGAC",
                   "CTTCTTGAGGTCGGTGTTGGTTCCGTAGATAACCTGTCCAAGCCGATCTT",
                   "TCGTTAGTTGAACTTCAAGTTATTCGGCCATCGGTCGATTTCCTGAACAG",
                   "TCGAAAGAATGGACAGAGCTTCGCTTACGCGGTTCATCATCCAGCCACGC",
                   "GTTGGACGTGGCGATGATGATGGTGTTGGTGAAATCCACCACCCGGCCCT",
                   "GATTACGTTGACGCCTTGCACCATTTAGCCAAAATCAGAAGAAAATTTGC",
                   "GCCGCGAGTCTTCACGATGAAAGATTACGAACAGGAAGATCCGATCCCCC",
                   "GTGCGATCTGGAAAGGCGCCAGCGCATCCGGCCAGAGAATCCCGCGCTCG",
                   "AGCTTCTTTGATCTTAGTAAAAGGCTCTGGAAAGTGCCGCCATAGTGGGT",
                   "CAATGTCATCAATTCGAATCTTCTGACTGCTCTTTATCTTGTCAGCTGGC",
                   "CAGAAGCGTTTTTAAGTGTGAGCGTGTTAGCCAGAATTTTAGAAGTAATC",
                   "TTTCCGGGTGATAGACCTCGTCCCGGTAGACGAACATGATGATGTCGGCG",
                   "CGCCAGTTGGGTGGGCATCGCTGGCAACTGATATTCAGCCGGCGCAAGCT",
                   "CGGGCATTGAAGGCCTTGCAGAACTCCATGATATTGACACCATGCTGACC",
                   "TTTGTTTTTAGAAAAAGAGCTGGCGATGGTCAGTTCGCAGCGTGATCGAG",
                   "CCACGTGAATGCCGATGATCCGGAAGCCGTATTGTTCGTCAGTCAGCTGG",
                   "TTTTGATAGACGGAGCATTCCCGGCTTTGCATTTTAAATTTTTGGAAGGT",
                   "CGCTGGAAACGCGCCTGGTCGGGCTGGAGGATGATGAAACCTCCGGGCTG",
                   "AGTTCCTGACATCCCTCCTAGATAGTTATTATGCTCACTCGCTAGCTCTG",
                   "CCGGTAATGGAAGTCGAAATCACCCTCCTGCTGGTAATAGCCCACTCCGG",
                   "AGAGCATCTTGTCGAAGCGTGCCTTCTCGACGTTGAGAATCTTGCCCTTG",
                   "CAGTTTGGAGACGTCGAGGATCTCGTTGATCAGATTCAGCAGCTCGTTGC",
                   "GCACAGACGTTTTAAATGCTGGCTGGCGGCTTGGTAGATCTCCCCGAAAT",
                   "ACTTGAGCGTTGAACATGACGTTCTCCGTAAGCATATAGTCCATCCCAAT",
                   "GATTTCGCTTGCAACCCCAACAGGATATTTATCCTTCCAGAAGTTATCGG",
                   "GGGTTGGTAAATGAGTGCAGTACTCCGGGGAAACTCACCAGTGTCAAATC",
                   "GGCATGCTTGGCAGTGATGTGCGGGAGAATATCCTGGGCGTCGCCGAAGT",
                   "ATGAATTGTCGTTGACACCTCCAGGCGATCCTCCTAACCTCGCCCGGACA",
                   "TGGCGCTTGAAGCCGCCGAGCCGCCCCCCCATATTGGCCCGACTGTCGGT",
                   "AAGCATAACTTATTGATTTACAACATTTTTTTCGTATAAAACTGCTTGGC",
                   "TGCCTTTTTACGCAATTTCGTTGGCTGGGTATGTTGCGGCCACATGCCGC",
                   "TGATTTACTGTCTTCAAGGTGTTCGAAGCGATCATCTCGACGAGAGCAGG",
                   "GGTTGAGCTTGCTGTCGATGTGGTCCATGTGGTGCATCATCAGGCGCACC",
                   "ATCGAGTACCATTTCAAGTATGGAGAACTTCTAATAGAAGGTTTCTGCCG",
                   "GATTGTGTGTCATAGTCACGGACGCCAATGATGTTCAGTTCTTGTGACAA",
                   "GCGGCTGCTGGAAAAGCCTGATCGGGCCATCCGCTACAGTCTCGATGGTG",
                   "CTGGGTTTAATAAATGCCCTGAAACCCCTGAAAATACGTTGGTAGCGCGT",
                   "TCGCTTTCTGCTTGTCAATCAAAAAAATCGGACATATAAACGGCTCACGA",
                   "TGAATGTCGCTATTGACGCCCAGCCAAAGCCCCCTATAATGCGCACCACT",
                   "CTGCGCCCTCGTTTGTCTTGCCTGGGCGATGCGCTACCATGGCGCTCCTC",
                   "AGTGAAATCTTGTGGAAGCAAATTAGTCTTTATGTATGGCAAGGACAAAA",
                   "TCTATCACTTTGGCAACTCTCACTTCCACCAGCATATGTTTCCGCTGCTG",
                   "AATCCTGATCAACTGACACCAAATTGCCTCACTGTCGAATGCGAGGACCC",
                   "ACCTGGATTTTTTGCCGGAAAGCCATACCGACTTTATCATTGCCGTTCTG",
                   "AGGTCGGCTGCTTTGTATTTCGGCCCTGTTCTTGTAACGTTACAGCCTTC",
                   "GAGGGCGGTGTTTCGACGCACCGCCCTCGGCGCGTCAAATACTGAAACGC",
                   "GTAAGTGACTGATTTGTATGGGAAATGAATAGAAGGGCGCTTTTAGAGCG",
                   "TGAGTAGTTGGAGAGACGCCATCCTGAACGATTTTGTACCCAACGTCAGC",
                   "CCAGAGCCGCTCTTGCTACAGCTGCGAGTTCCGATAAATTGAGCGCAATT",
                   "CCGGCGCCTTTGTCGGCCATCGCACCCTCGAGGAGACAATCTTCAAGACC",
                   "TGAATTCCGATGTGACTCATGGGTCCTCTGAGCGCATCATTTGGATAAGG",
                   "ATACGTCTTGGAGGGGCGGCTGCCCGACGCAGAATGGGTCGGCCGGGCAG",
                   "GATGAGTATTTGCTGTGGCCTGAAGGGAAACCCGTAACCTTTGACCGCTC",
                   "GCTTGGCTCGACCCGCAACCACGGTGGCGTAAGTTTTCTCGGCACCAGCC",
                   "AAAATTAATATTTTGATATATCTTGAAATTTCGAACTAATAACGCAACAA",
                   "AATTAGCTTGTAAAATAGAAACTTCCCCTGGCGATAAAGTTCCACCAACC",
                   "TATTTAGACTGGCTCTAGTCGACATCGTTGATAATGCCGAGACTGCCTGC",
                   "TTGGTCACTGGAATTGACCCAGACATTGTTGATAAACAATTTTGTATTCA",
                   "ATCGTGGTTGCCGAGCAGGAAGGCGAAGACAACATCCTGATCTATGCCAA",
                   "AGCTCCTCGCTCTTGAATCCGTAGCCGCGCAGCAGAAAATCCGCCTGGTA",
                   "CTCGATCTGGAACGCGTCACGGTCGACGACATCATGATTCCGCGCAACGA",
                   "TCCTTGCTGGATGGACTCCCCGCTTCGAGAAAAATCCAGGCCAAGGATGG",
                   "CGTCGTACATGTTCAAGGATGCCTTCGCCAGCACCATCATCGAAGACCTC",
                   "GATTTTGACTTTATAGCCCCTGAGTCCTCGAAATTGAATTCGAGCTTGGC",
                   "TGAAGTTGAAGGATCAGCAAAATTGTACATACAGTAAAAACTACTGCCGA",
                   "AGTGCAATGATTTCGAACTCGTCTACCAGCCACAGATCATGCTGGGCGAC",
                   "GTGACCTGCTTGCCGGCTTCCATGTGCTGCTGGATCTCATCGCTGGTCAG",
                   "CTTTTTTTTAGGTCAGGCATATTGACGTATTTATTCGGCGAGGCGTAATT",
                   "AGCGATTTGAACTGCAGGGGGACCTTTTGCAGGATGTAGTCGATGCTGCC",
                   "CCGAATTTTGTCTCGGGTCAGACTATCAATTTCATCCATGCCAGAGCCCT",
                   "CATGTTGACTTAACGAGCGACTGGCTCGTTAGTATTGATATCCGGAAGCT",
                   "TTCTTGCTAAAAAAGACTGCCTTTAGTAATAAAAGCTACAGCAAAATTCT",
                   "GCACGCTGATTGGCCGTCTGCTGCACGATTCCAAGATGATCTACGAAGAT",
                   "CAGCCAACGAAATTGCGTAAAAAGGCAAATAAGTTATTTTTTATGTCGAG",
                   "TTGCACCTATGGATTCAGTACAAGATACCTAGGTTATCCTAGGTGGGTTC",
                   "TGTTCTGGAAAACCGCCTATGTCTATGGCGACAATGTCGACACCGGCACT",
                   "CGATGGCGCCTTATGAAATCACCCAGGCCGGCGGTAGCGTCGAGCACTGG",
                   "AGGTGATTGCCGTCCTGTCGGAGGATCTGCATCTTCGCCAGCCACTCCTC",
                   "TCTTTGCGTGACAGCCAGACTCAAAGCTGTACAATGGCCGTCGCGGGATG",
                   "GGATGAATTCGACGAAAAAATCTGTGCTGTATACTGCACATACCGGCCGC",
                   "CTTGTTGATCATGCCGCGATTCTCAGGCGTATCCTGGACCTCGACGGTAT",
                   "AACTGGCTGACTTCCACCTGGCCGGGCTTGAACATGATCGCTGTCCTCCT",
                   "CGGCTTGATGGAGCGCACCTGAGGGTTGACATACTCAGGCTGAACCGAAG",
                   "ACGGCAGTTTGAATAAAGGCATTGATATCGCCGGTGAATTAGGACAGCCT",
                   "AGGCTACCCATTTTTGACATTCAAGGATGTCTTTTACAACTACTTCACAC",
                   "GACACAGGACTTGCGGCCGGCGTTGCGTCAGCCCTAGATTGCCCTGACCT",
                   "CCACCATCGTGGTGGACTGCCGGGATAACCGCATTAGCTTCGGTGAGGCT",
                   "AGTTGAAGCCGCCAGCGTAGTAATGCTCGTAGAACGGCAGGCGCTCGGTC",
                   "CGGTGAGCTTGACACCGACGATATCGGGCAGGCGCATCATCGACGGATGA",
                   "ATAGTTCTTGACCTGTCCAACCTGGATCTGGCGATAAAAGACCGGGCTGC",
                   "GTGTTCTGACAAAGAGTTTCGAAGAACGCTTAAATGCTGCCGATGTGGGT",
                   "ATGATGATTTGCGGCGTGCTCGCATGGATCATCATCGGCTTTCCGCTGAT",
                   "CTGCGCTTGGGAATGCCGCGGGCTGCGGCTATACTCAGCCCGTTTTTCCC",
                   "AGCCGAAGGGTTTGACAGTCGCCGGAAGCAGCATTACGTTAACGTAAAGG",
                   "CGGTTTTCCAGCTTTTAACTCCAAACCGATCGAATTCGTAGGGTGGATGG",
                   "CCCTGTCGCTTGTGTCATCATGCCGCGACCGCATTAAAGCCGCCCCCGCA",
                   "GGCTGATTGTTACCGTCCGCTTCAGCGGGCAGTATTTCCAGTGCGATGCG",
                   "GCAATTGAGGGGGGATATCAATTAGTGGGTAAAATGGAAGATGCTCCACG",
                   "TCTAGCAATTTGCAGTCTCCTTGGATCGATATCCTACAAGTGGGCTGTAG",
                   "GCCGGTGCCTTGTGGAACTGGAACTGGGTCAGGCCATAGTCGTTCGCCAG",
                   "GCTGATGGTGACAGACAACCCGAAGAGCAGACTCTAGAGTCACGGTCGAG",
                   "TTTTTGTTTGTATTTCCGAAGGTCGGCTCGAGCATCTGTAGGGTGTCGTG",
                   "GCTCGTCATTTTCGACTGTGCCGATCATCGCGGCCATCTTCGTTCCGCTT",
                   "TCTTCAAGTAGAACGCCGCTGTCAGCAGCTCGAATAGCTGCCTTTCTGGC"]

parameters = {# Part 1: Simulation metadata
              "simulation_name": "23_simulation_base",
              "population_names": ['pop_01'],

              # Part 2: World settings
              "world_x": 1,
              "world_y": 1,
              "world_z": 1,
              "population_locations": [[(0,0,0)]],
              "eco_cell_capacity": 1000,
              "deployment_code": 1,

              # Part 3: Population settings
              "population_size": 100,

              # Part 4: Genetics settings
              "genome_size": 1,
              "chromosome_size": 2000,
              "chromosome_bases": ['A', 'T', 'G', 'C'],
              "initial_chromosome": ['A', 'T', 'G', 'A', 'A', 'G', 'G', 'G', 'G', 'C', 'G', 'G', 'C', 'C', 'G', 'G', 'G', 'A', 'C', 'G', 'C', 'G', 'C', 'C', 'G', 'C', 'G', 'C', 'G', 'G', 'G', 'A', 'G', 'A', 'A', 'C', 'G', 'C', 'C', 'A', 'G', 'A', 'G', 'A', 'G', 'A', 'G', 'G', 'G', 'G', 'C', 'G', 'C', 'T', 'A', 'A'],

              # Part 5: Mutation settings
              "background_mutation": 0.1,
              "additional_mutation": 0,
              "mutation_type": 'point',
              
              # Part 6: Metabolic settings
              "interpreter": 'ragaraja',
              "instruction_size": 3,
              "ragaraja_version": 0,
              "base_converter": None,
              "ragaraja_instructions": [],
              "max_tape_length": 50,
              "interpret_chromosome": False,
              "clean_cell": False,
              "max_codon": 2000,

              # Part 7: Simulation settings
              "goal": 0,
              "maximum_generations": 500,
              "eco_buried_frequency": 100,
              "fossilized_ratio": 0.01,
              "fossilized_frequency": 20,
              
              # Part 8: Simulation report settings
              "print_frequency": 10,
              "database_file": "simulation.db",
              "database_logging_frequency": 1
             }

class simulation_functions(dose.dose_functions):

    def organism_movement(self, Populations, pop_name, World): pass

    def organism_location(self, Populations, pop_name, World): pass

    def ecoregulate(self, World): pass

    def update_ecology(self, World, x, y, z): pass

    def update_local(self, World, x, y, z): pass

    def report(self, World): pass

    def fitness(self, Populations, pop_name):
        agents = Populations[pop_name].agents
        for index in range(len(agents)):
            organism = agents[index]
            chromosome = ''.join(organism.genome[0].sequence)
            score = [aligner.score(chromosome, seq) 
                     for seq in known_sequences]
            score = sum(score) / len(score)
            agents[index].status['fitness'] = score

    def mutation_scheme(self, organism): 
        organism.genome[0].rmutate(parameters["mutation_type"],
                                   parameters["additional_mutation"])

    def prepopulation_control(self, Populations, pop_name): 
        agents = Populations[pop_name].agents
        status = [(index, agents[index].status['fitness'])
                   for index in range(len(agents))]
        eliminate = [x[1] for x in status]
        eliminate.sort()
        ethreshold = eliminate[9]
        if len([x for x in eliminate if x > ethreshold]) > 50:
            Populations[pop_name].agents = \
                [agents[i] for i in range(len(agents))
                    if agents[i].status['fitness'] > ethreshold]
        else:
            eliminate = [x[0] for x in status]
            eliminate = [random.choice(eliminate) for x in range(10)]
            Populations[pop_name].agents = \
                [agents[i] for i in range(len(agents))
                    if i not in eliminate]
        print("Population size after elimination: " + \
            str(len(Populations[pop_name].agents)))

    def mating(self, Populations, pop_name):
        agents = Populations[pop_name].agents
        while len(agents) < 100:
            chosen_agent = random.choice(agents)
            new_agent = copy.deepcopy(chosen_agent)
            agents.append(new_agent)

    def postpopulation_control(self, Populations, pop_name): pass

    def generation_events(self, Populations, pop_name): pass

    def population_report(self, Populations, pop_name):
        agents = Populations[pop_name].agents
        sequences = [''.join(org.genome[0].sequence) for org in agents]
        identities = [org.status['identity'] for org in agents]
        locations = [str(org.status['location']) for org in agents]
        demes = [org.status['deme'] for org in agents]
        fitness = [org.status['fitness'] for org in agents]
        gen_count = agents[0].status["generation"]
        print(gen_count, max(fitness), sum(fitness)/len(fitness))
        return '\n'.join(sequences)

    def database_report(self, con, cur, start_time, 
                        Populations, World, generation_count):
        try: dose.database_report_populations(con, cur, start_time, 
                                    Populations, generation_count)
        except: pass
        try: dose.database_report_world(con, cur, start_time, 
                                        World, generation_count)
        except: pass

    def deployment_scheme(self, Populations, pop_name, World): pass

dose.simulate(parameters, simulation_functions)
