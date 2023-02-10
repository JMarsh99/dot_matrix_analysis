from PIL import Image
import os
import numpy as np
import sys


SIMILARITY_THRESHOLD = 0.5
IMAGES_PATH = '/home/jordan/personal-project/dot_matrix_analysis/images'


def usage():
    print('python compare_files.py path/to/file1 path/to/file2')


def main(argv=sys.argv):
    if len(argv) < 3:
        usage()
        sys.exit(0)

    matrix = compare(argv[1], argv[2])
    file1_name = os.path.basename(argv[1])
    file2_name = os.path.basename(argv[2])
    print('Mean Jaccard Similarity:', np.mean(np.array(matrix)))
    create_image(matrix, file1_name, file2_name)



def compare(file_path1, file_path2):
    f1_lines = get_lines(file_path1)
    f2_lines = get_lines(file_path2)

    if len(f1_lines) < 100 or len(f2_lines) < 100:
        return None

    matrix = []

    for f1_line in f1_lines:
        row = []
        for f2_line in f2_lines:
            # Find intersection (with duplicates)
            intersection = set(f1_line).intersection(set(f2_line))
            # Find Union
            union = set(f1_line + f2_line)
            # Find Jaccard similarity
            js = len(intersection) / len(union)
            row.append(js)
        matrix.append(row)

    return matrix


def create_image(matrix, file1_name, file2_name):
    rgb_matrix = []
    for row in matrix:
        rgb_matrix.append([(125, 125, 0) if value >= SIMILARITY_THRESHOLD else (255, 255, 255) for value in row])
    np_array = np.array(rgb_matrix, dtype=np.uint8)

    dot_matrix = Image.fromarray(np_array)
    dot_matrix.save(f'{IMAGES_PATH}/{file1_name}_{file2_name}.png')


def get_lines(file_path):
    lines = []
    with open(file_path, 'r') as file1:
        lines = file1.readlines()
        formatted_lines = []
        for line in lines:
            formatted_line = [word for word in line.rstrip('\r\n').split(' ') if word]
            if formatted_line and '#' not in formatted_line[0]:
                formatted_lines.append(formatted_line)

    return formatted_lines


if __name__ == '__main__':
    main()
