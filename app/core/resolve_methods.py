"""
Methods for solving TSP
"""
from itertools import permutations


def brute_force(matrix, task_type='min', first_city=None):
    res_func = {'max': max, 'min': min}[task_type]
    res = {'max': -1, 'min': 99999999999}[task_type]
    if first_city:
        first_city -= 1
        perms = (permutation for permutation in permutations(range(len(matrix[0]))) if permutation[0] == first_city)
    else:
        perms = permutations(range(len(matrix[0])))
    for permutation in perms:
        tmp_res = matrix[permutation[-1]][permutation[0]]
        for num, el in enumerate(permutation[:-1]):
            tmp_res += matrix[el][permutation[num + 1]]
        res = res_func(res, tmp_res)
    return res


def bellman_func(i: int, v: tuple, matrix):
    if len(v) == 1:
        if v[0] == len(matrix) - 1:
            return matrix[i][v[0]]
        else:
            return matrix[i][v[0]] + bellman_func(v[0], (len(matrix) - 1, ), matrix)
    else:
        equation = ((matrix[i][j] + bellman_func(j, v[0:num] + v[num + 1:], matrix))
                    for num, j in enumerate(v))
        return min(equation)
