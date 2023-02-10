from fnmatch import fnmatch
import numpy as np
import os
import sys

from project.compare_files import compare, create_image


def usage():
    print('python dot_matrix_analysis.py path/to/folder')


def main(argv=sys.argv):
    if len(argv) < 2:
        usage()
        sys.exit(0)

    base_folder = argv[1]

    files_to_compare = []
    for path, subdirs, files in os.walk(base_folder):
        for name in files:
            if fnmatch(name, '*.py'):
                if name != '__init__.py':
                    files_to_compare.append(os.path.join(path, name))

    all_scores = []
    completed_combos = []
    for file1 in files_to_compare:
        for file2 in files_to_compare:
            if (file1, file2) in completed_combos or (file2, file1) in completed_combos:
                continue

            matrix = compare(file1, file2)
            if matrix:
                average_score = np.mean(np.array(matrix))
                all_scores.append({
                    'file1': file1,
                    'file2': file2,
                    'score': average_score,
                    'matrix': matrix
                })

            completed_combos.append((file1, file2))

    sorted_scores = sorted(all_scores, key=lambda score_dict: -score_dict['score'])

    print('TOP 5 SCORES')
    for score_dict in sorted_scores[:5]:
        print(f'{score_dict["file1"]} compared to {score_dict["file2"]} with a average score of {score_dict["score"]}')
        create_image(score_dict['matrix'], os.path.basename(score_dict["file1"]), os.path.basename(score_dict["file2"]))

    print('NEXT 20 SCORES')
    for score_dict in sorted_scores[:20]:
        print(f'{score_dict["file1"]} compared to {score_dict["file2"]} with a average score of {score_dict["score"]}')

if __name__ == '__main__':
    main()
