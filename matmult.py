import math


def mult_scalar(matrix, scale):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] *= scale
    return matrix


def mult_matrix(a, b):
    matrix = [[0 for _ in range(len(b[0]))] for _ in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                matrix[i][j] += a[i][k] * b[k][j]
    return matrix


def euclidean_dist(a, b):
    sum = 0
    for i in range(len(a[0])):
        sum += (a[0][i] - b[0][i]) ** 2
    return math.sqrt(sum)
