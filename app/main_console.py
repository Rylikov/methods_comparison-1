import time

import numpy as np

from core.data import Data

if __name__ == '__main__':
    print('-' * 80 + '\nMethod comparison v.0.1.\n' + '-' * 80,
          '\nHello! Please, select command:\n'
          '\t1)Brute_force - Calc task with brute force method;\n'
          '\t2) Exit;')
    while True:
        cmd = input('Enter command here:\n')
        if cmd.lower() in ('2', 'exit'):
            break
        elif cmd.lower() in ('1', 'brute_force'):
            task_type = input('Enter task type(min or max):\n')
            while task_type not in ('min', 'max'):
                print('Wrong, try again.')
                task_type = input('Enter task type(min or max):\n')
            print('How you want to enter data?:\n'
                  '\t1)From file;\n'
                  '\t2)From keyboard;')
            insert_type = input()
            while insert_type not in ('1', '2'):
                insert_type = input()
                if insert_type not in ('1', '2'):
                    print('Error, try again\n')
            if insert_type == '1':
                print('Careful! Matrix in file should be square. One string in file - one row of matrix, '
                      'entry splitter - ";".\n')
                matr_file = input('Enter path to file(full):\n')
                task = Data(matr_file, task_type, from_file=True)
                task.solve()
                print('Answer:', task.result)
            elif insert_type == '2':
                matrix = []
                dim = input('Enter dimension(max=10):\n')
                while int(dim) not in range(1, 11):
                    print('Wrong, try again\n')
                    dim = input()
                print('Enter matrix(1 row per string, entries splitter is whitespace:')
                for i in range(int(dim)):
                    row = input()
                    matrix.append(list(map(float, row.split(' '))))
                matrix = np.array(matrix)
                task = Data(matrix, task_type)
                start = time.clock()
                task.solve()
                resolve_time = time.clock() - start
                print('Matrix(corrected):')
                print(task.matrix)
                print('Answer: ' + str(task.result) + '\nSolving time: ' + str(resolve_time) + ' seconds')
        else:
            print("Command wasn't found")
