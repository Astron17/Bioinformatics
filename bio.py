import configparser
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-a', required=True)
parser.add_argument('-b', required=True)
parser.add_argument('-c', required=True)
parser.add_argument('-o', required=True)
args = parser.parse_args()
configParser = configparser.RawConfigParser()
configFilePath = args.c
configParser.read(configFilePath)

""" Reads the Input Sequences form the text file """

with open(args.a, 'r') as file:
    SEQUENCE_1 = (file.read())
with open(args.b, 'r') as file2:
    SEQUENCE_2 = (file2.read())

""" Declaring the variables and parsing the values form the text file """

MATRIX_ROW = len(SEQUENCE_1) + 1  
MATRIX_COLUMN = len(SEQUENCE_2) + 1  
MATCH_SCORE = int(configParser.get('var', 'SAME'))  
MISMATCH_SCORE = int(configParser.get('var', 'DIFF'))  
GAP_SCORE = int(configParser.get('var', 'GAP_PENALTY'))  
GAP_CHARACTER = '-'  
ALN_PATHWAYS = []  
MATRIX = [[[[None] for i in range(2)] for i in range(MATRIX_COLUMN)]
          for i in range(MATRIX_ROW)]  

""" This function writes all possible arrangements to the Output file """

def write_alignments(ARRANGMENTS):  
    with open(args.o, 'w') as file1:
        file1.write("SCORE =" + str(ARRANGMENTS[0][3][0][1]) + '\n\n')
        for elem in ARRANGMENTS:
            file1.write(elem[0] + '\n' + elem[1] + '\n' + '\n')
    return

""" This function finds all the paths """

def find_each_path(c_i, c_j,
                   path=''):  
    global ALN_PATHWAYS
    i = c_i
    j = c_j
    if i == 0 and j == 0:
        ALN_PATHWAYS.append(path)
        return 2
    dir_t = len(MATRIX[i][j][1])
    while dir_t <= 1:
        n_dir = MATRIX[i][j][1][0] if (i != 0
                                       and j != 0) else (1 if i == 0 else
                                                         (3 if j == 0 else 0))
        path = path + str(n_dir)
        if n_dir == 1:
            j = j - 1
        elif n_dir == 2:
            i = i - 1
            j = j - 1
        elif n_dir == 3:
            i = i - 1
        dir_t = len(MATRIX[i][j][1])
        if i == 0 and j == 0:
            ALN_PATHWAYS.append(path)
            return 3
    if dir_t > 1:
        for dir_c in range(dir_t):
            n_dir = MATRIX[i][j][1][dir_c] if (i != 0 and j != 0) else (
                1 if i == 0 else (3 if j == 0 else 0))
            tmp_path = path + str(n_dir)
            if n_dir == 1:
                n_i = i
                n_j = j - 1
            elif n_dir == 2:
                n_i = i - 1
                n_j = j - 1
            elif n_dir == 3:
                n_i = i - 1
                n_j = j
            find_each_path(n_i, n_j, tmp_path)
    return len(ALN_PATHWAYS)

""" Program Starts Here """
""" Creates score matrix """
for i in range(MATRIX_ROW):
    MATRIX[i][0] = [GAP_SCORE * i, []]
for j in range(MATRIX_COLUMN):
    MATRIX[0][j] = [GAP_SCORE * j, []]
for i in range(1, MATRIX_ROW):
    for j in range(1, MATRIX_COLUMN):
        score = MATCH_SCORE if (
            SEQUENCE_1[i - 1] == SEQUENCE_2[j - 1]) else MISMATCH_SCORE
        horizontal_val = MATRIX[i][j - 1][0] + GAP_SCORE
        diagonal_val = MATRIX[i - 1][j - 1][0] + score
        vertical_val = MATRIX[i - 1][j][0] + GAP_SCORE
        output_val = [horizontal_val, diagonal_val, vertical_val]
        MATRIX[i][j] = [
            max(output_val),
            [i + 1 for i, v in enumerate(output_val) if v == max(output_val)]
        ]  

OVERALL_SCORE = MATRIX[i][j][0]
score = OVERALL_SCORE
l_i = i
l_j = j
ARRANGMENTS = []
tot_aln = find_each_path(i, j)
aln_count = 0

for elem in ALN_PATHWAYS:
    i = l_i - 1
    j = l_j - 1
    side_aln = ''
    top_aln = ''
    step = 0
    aln_info = []
    for n_dir_c in range(len(elem)):
        n_dir = elem[n_dir_c]
        score = MATRIX[i + 1][j + 1][0]
        step = step + 1
        aln_info.append([step, score, n_dir])
        if n_dir == '2':
            side_aln = side_aln + SEQUENCE_1[i]
            top_aln = top_aln + SEQUENCE_2[j]
            i = i - 1
            j = j - 1
        elif n_dir == '1':
            side_aln = side_aln + GAP_CHARACTER
            top_aln = top_aln + SEQUENCE_2[j]
            j = j - 1
        elif n_dir == '3':
            side_aln = side_aln + SEQUENCE_1[i]
            top_aln = top_aln + GAP_CHARACTER
            i = i - 1
    aln_count = aln_count + 1
    ARRANGMENTS.append(
        [top_aln[::-1], side_aln[::-1], elem, aln_info, aln_count])

write_alignments(ARRANGMENTS)
