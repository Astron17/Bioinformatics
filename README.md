# Bioinformatics

example usage:python needleman_wunsh.py -a seq1.txt -b seq2.txt -c config.txt -o output.txt 
● seq1.txt and seq2.txt should be in FASTA format(​https://en.wikipedia.org/wiki/FASTA_format​)
● config.txt:
    GAP_PENALTY = int
    SAME = int
    DIFF = int
● e.g. output.txt: 
    SCORE = 6

    SU-MS-AM
    S-UMSA-M
