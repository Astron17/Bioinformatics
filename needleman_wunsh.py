import configparser
import argparse
import test_bio

# parser = argparse.ArgumentParser()

# parser.add_argument('-a', required=True)
# parser.add_argument('-b', required=True)
# parser.add_argument('-c', required=True)
# parser.add_argument('-o', required=True)
# args = parser.parse_args()
# configParser = configparser.RawConfigParser()
# configFilePath = args.c
# configParser.read(configFilePath)


# """ Reads the Input Sequences form the text file """

# with open(args.a, 'r') as file:
#     Sequence_1 = (file.read())
# with open(args.b, 'r') as file2:
#     Sequence_2 = (file2.read())


Sequence_1 = 'SUM'
Sequence_2 = 'SAM'
Matrix_Row = len(Sequence_1)+1
Matrix_Column = len(Sequence_2)+1
# Match_Score = int(configParser.get('var', 'SAME'))
# Mismatch_Score = int(configParser.get('var', 'DIFF'))
# Gap_Score = int(configParser.get('var', 'GAP_PENALTY'))
Match_Score = 1
Mismatch_Score = -1
Gap_Score = -2
Gap_Character = '-'
Arrangement_Ways = []
Matrix = [[[[None] for i in range(2)] for i in range(
    Matrix_Column)] for i in range(Matrix_Row)]


def Print_Arrangements(ARRANGMENTS):
    print('Total ARRANGMENTS: ' + str(len(ARRANGMENTS)))
    print('Overall Score: '+str(ARRANGMENTS[0][3][0][1])+'\n')
    for Elements in ARRANGMENTS:
        print(Elements[0]+'\n'+Elements[1]+'\n')
    with open("C:/Users/aravi/Desktop/output.txt", 'w') as file1:
        file1.write("SCORE =" + str(ARRANGMENTS[0][3][0][1]) + '\n\n')
        for Elements in ARRANGMENTS:
            file1.write(Elements[0] + '\n' + Elements[1] + '\n' + '\n')
    return


def Find_All_Paths(c_i, c_j, path=''):
    global Arrangement_Ways
    i = c_i
    j = c_j
    if i == 0 and j == 0:
        Arrangement_Ways.append(path)
        return 2
    dir_t = len(Matrix[i][j][1])
    while dir_t <= 1:
        n_dir = Matrix[i][j][1][0] if (i != 0 and j != 0) else (
            1 if i == 0 else (3 if j == 0 else 0))
        path = path + str(n_dir)
        if n_dir == 1:
            j = j-1
        elif n_dir == 2:
            i = i-1
            j = j-1
        elif n_dir == 3:
            i = i-1
        dir_t = len(Matrix[i][j][1])
        if i == 0 and j == 0:
            Arrangement_Ways.append(path)
            return 3
    if dir_t > 1:
        for dir_c in range(dir_t):
            n_dir = Matrix[i][j][1][dir_c] if (i != 0 and j != 0) else (
                1 if i == 0 else (3 if j == 0 else 0))
            tmp_path = path + str(n_dir)
            if n_dir == 1:
                n_i = i
                n_j = j-1
            elif n_dir == 2:
                n_i = i-1
                n_j = j-1
            elif n_dir == 3:
                n_i = i-1
                n_j = j
            Find_All_Paths(n_i, n_j, tmp_path)
    return len(Arrangement_Ways)


for i in range(Matrix_Row):
    Matrix[i][0] = [Gap_Score*i, []]
for j in range(Matrix_Column):
    Matrix[0][j] = [Gap_Score*j, []]
for i in range(1, Matrix_Row):
    for j in range(1, Matrix_Column):
        score = Match_Score if (
            Sequence_1[i-1] == Sequence_2[j-1]) else Mismatch_Score
        Horizontal_Value = Matrix[i][j-1][0] + Gap_Score
        Diagonal_Value = Matrix[i-1][j-1][0] + score
        Vertical_Value = Matrix[i-1][j][0] + Gap_Score
        Output_Value = [Horizontal_Value, Diagonal_Value, Vertical_Value]
        # h = 1, d = 2, v = 3
        Matrix[i][j] = [
            max(Output_Value), [i+1 for i, v in enumerate(Output_Value) if v == max(Output_Value)]]

OVERALL_SCORE = Matrix[i][j][0]
score = OVERALL_SCORE
l_i = i
l_j = j

ARRANGMENTS = []
tot_alignment = Find_All_Paths(i, j)
alignment_count = 0

for Elements in Arrangement_Ways:
    i = l_i-1
    j = l_j-1
    side_alignment = ''
    top_alignment = ''
    step = 0
    alignment_info = []
    for n_dir_c in range(len(Elements)):
        n_dir = Elements[n_dir_c]
        score = Matrix[i+1][j+1][0]
        step = step + 1
        alignment_info.append([step, score, n_dir])
        if n_dir == '2':
            side_alignment = side_alignment + Sequence_1[i]
            top_alignment = top_alignment + Sequence_2[j]
            i = i-1
            j = j-1
        elif n_dir == '1':
            side_alignment = side_alignment + Gap_Character
            top_alignment = top_alignment + Sequence_2[j]
            j = j-1
        elif n_dir == '3':
            side_alignment = side_alignment + Sequence_1[i]
            top_alignment = top_alignment + Gap_Character
            i = i-1
    alignment_count = alignment_count + 1
    ARRANGMENTS.append([top_alignment[::-1], side_alignment[::-1],
                        Elements, alignment_info, alignment_count])

Print_Arrangements(ARRANGMENTS)

