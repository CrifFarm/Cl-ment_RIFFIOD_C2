import math
import time
import numpy as np
from fractions import Fraction

# Ex 1.1
def transposee(a):
    return [[a[j][i] for j in range(len(a))] for i in range(len(a[0]))]

a = [[1, 2, 3], [4, 5, 6]]
print(transposee(a))
# inverser les indices len(a) et len(a[0]) dans la comprehension de liste provoque une erreur IndexError si la matrice n'est pas carree

# Ex 2.1
def produit(a, b):
    m, n, p = len(a), len(a[0]), len(b[0])
    c = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                c[i][j] += a[i][k] * b[k][j]
    return c

id3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
m3 = [[1, 2, 2], [1, 3, -2], [3, 5, 8]]
print(produit(m3, id3))
# confondre l'ordre des boucles j et k en assignant c[i][k] ecrase les valeurs au lieu de faire le produit matriciel

# Ex 2.2
n = 80
m_a = [[1.0] * n for _ in range(n)]
m_b = [[1.0] * n for _ in range(n)]
t0 = time.perf_counter()
produit(m_a, m_b)
t_80 = time.perf_counter() - t0

n = 160
m_a2 = [[1.0] * n for _ in range(n)]
m_b2 = [[1.0] * n for _ in range(n)]
t0 = time.perf_counter()
produit(m_a2, m_b2)
t_160 = time.perf_counter() - t0

print(t_160 / t_80)
# la complexite etant en O(n^3), doubler la taille multiplie le temps par environ 8 et non par 2 ou 4

# Ex 3.1
a_np = np.ones((120, 120))
b_np = np.ones((120, 120))

t0 = time.perf_counter()
produit(m_a2, m_b2)
t_py = time.perf_counter() - t0

t0 = time.perf_counter()
_ = a_np @ b_np
t_np = time.perf_counter() - t0

print(t_py / t_np)
# utiliser a * b au lieu de a @ b fait un produit terme a terme et non le produit matriciel

# Ex 4.1
def resoudre(a, b):
    n = len(a)
    m = [a[i][:] + [b[i]] for i in range(n)]
    for k in range(n):
        p_max = max(range(k, n), key=lambda i: abs(m[i][k]))
        m[k], m[p_max] = m[p_max], m[k]
        p = m[k][k]
        for j in range(k, n + 1):
            m[k][j] /= p
        for i in range(k + 1, n):
            f = m[i][k]
            for j in range(k, n + 1):
                m[i][j] -= f * m[k][j]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = m[i][n] - sum(m[i][j] * x[j] for j in range(i + 1, n))
    return x

a_ex = [[1.0, 2.0, 2.0], [1.0, 3.0, -2.0], [3.0, 5.0, 8.0]]
b_ex = [2.0, -1.0, 8.0]
print(resoudre(a_ex, b_ex))
# ignorer le pivot partiel p_max entraine une division par zero si un terme diagonal est nul au cours du calcul

# Ex 4.2
np.random.seed(0)
a_rnd = np.random.rand(50, 50)
b_rnd = np.random.rand(50)
x_py = resoudre(a_rnd.tolist(), b_rnd.tolist())
x_np = np.linalg.solve(a_rnd, b_rnd)
print(max(abs(x_py[i] - x_np[i]) for i in range(50)))
# modifier la matrice b en place dans les boucles sans adapter les indices fausse la remontee

# Ex 5.1
def hilbert(n):
    return np.array([[1.0 / (i + j + 1) for j in range(n)] for i in range(n)])

h = hilbert(12)
x_v = np.ones(12)
b_h = h @ x_v
x_sol = np.linalg.solve(h, b_h)
x_inv = np.linalg.inv(h) @ b_h
print(float(np.max(np.abs(x_sol - x_v))), float(np.max(np.abs(x_inv - x_v))), float(np.linalg.cond(h)))
# utiliser inv(h) @ b au lieu de solve(h, b) amplifie massivement l'erreur car la matrice est tres mal conditionnee

# Ex 6.1
def rot(deg):
    rad = math.radians(deg)
    c, s = math.cos(rad), math.sin(rad)
    return np.array([[c, -s], [s, c]])

r30, r60, r90 = rot(30), rot(60), rot(90)
print(np.allclose(r60 @ r30, r90))
# faire r30 @ r60 au lieu de r60 @ r30 ne change rien pour deux rotations, mais echoue pour d'autres transformations car le produit n'est pas commutatif en general

# Ex 7.1
def determinant(a):
    n = len(a)
    m = [row[:] for row in a]
    det = 1.0
    for k in range(n):
        p_max = max(range(k, n), key=lambda i: abs(m[i][k]))
        if abs(m[p_max][k]) < 1e-12:
            return 0.0
        if p_max != k:
            m[k], m[p_max] = m[p_max], m[k]
            det = -det
        p = m[k][k]
        det *= p
        for i in range(k + 1, n):
            f = m[i][k] / p
            for j in range(k + 1, n):
                m[i][j] -= f * m[k][j]
    return det

a_sing = [[1.0, 2.0], [2.0, 4.0]]
print(determinant(m3), determinant(a_sing), np.linalg.det(m3))
# oublier de changer le signe de det lors de l'echange de deux lignes inverse le signe du determinant final

# Ex 8.1
def hilbert_exact(n):
    a = [[Fraction(1, i + j + 1) for j in range(n)] for i in range(n)]
    b = [sum(a[i]) for i in range(n)]
    return a, b

a_h, b_h = hilbert_exact(12)
x_ex = resoudre(a_h, b_h)
print(x_ex)
# utiliser Fraction(1.0 / (i + j + 1)) réintroduit les arrondis du float au lieu de passer deux entiers Fraction(1, i + j + 1)

# Ex 9.1
def trans_h(tx, ty):
    return np.array([[1.0, 0.0, tx], [0.0, 1.0, ty], [0.0, 0.0, 1.0]])

def rot_h(deg):
    rad = math.radians(deg)
    c, s = math.cos(rad), math.sin(rad)
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])

p_pt = np.array([1.0, 0.0, 1.0])
t_m = trans_h(3, 1)
r_m = rot_h(90)

p1 = r_m @ (t_m @ p_pt)
p2 = t_m @ (r_m @ p_pt)
print(p1[:2], p2[:2])
# inverser l'ordre des matrices de transformation r_m @ t_m au lieu de t_m @ r_m ne donne pas le meme point d'arrivee
