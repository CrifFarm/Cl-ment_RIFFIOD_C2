import math
import time
import matplotlib.pyplot as plt

# Ex 1.1
def evaluer_naif(p, x):
    return sum(c * (x**i) for i, c in enumerate(p))

p = [2, 3, 0, 5]
print(evaluer_naif(p, 2))
# renverser les indices avec enumerate(p[::-1]) inverse les coefficients des puissances

# Ex 2.1
def evaluer(p, x):
    res = 0
    for c in reversed(p):
        res = res * x + c
    return res

print(evaluer(p, 2) == evaluer_naif(p, 2))
# partir du début de p au lieu de la fin ne calcule pas la bonne factorisation de Horner

# Ex 2.2
p_grand = [1] * 20000
t0 = time.perf_counter()
evaluer_naif(p_grand, 1.0001)
t_naif = time.perf_counter() - t0

t0 = time.perf_counter()
evaluer(p_grand, 1.0001)
t_horner = time.perf_counter() - t0

print(t_naif / t_horner)
# croire que Horner est 100x plus rapide sur les float en Python est faux car le processeur optimise x**i très efficacement

# Ex 2.3
p_int = [1] * 800
t0 = time.perf_counter()
evaluer_naif(p_int, 3)
t_naif_int = time.perf_counter() - t0

t0 = time.perf_counter()
evaluer(p_int, 3)
t_horner_int = time.perf_counter() - t0

print(t_naif_int / t_horner_int)
# sur de grands entiers le calcul exact de 3**i devient très lourd et Horner reprend un net avantage

# Ex 3.1
def deriver(p):
    return [i * c for i, c in enumerate(p)][1:]

print(deriver(p))
# oublier [1:] laisse un coefficient 0 en premier et garde un degré incorrect

# Ex 4.1
def dichotomie(f, a, b, tol=1e-6):
    while (b - a) > tol:
        m = (a + b) / 2
        if f(a) * f(m) <= 0:
            b = m
        else:
            a = m
    return (a + b) / 2

f_sq = lambda x: x**2 - 2
print(dichotomie(f_sq, 0, 2))
# utiliser f(a) * f(b) <= 0 dans le if au lieu de f(a) * f(m) empêche de réduire l'intervalle

# Ex 4.2
def newton(p, x0, tol=1e-6):
    dp = deriver(p)
    x = x0
    for _ in range(100):
        fx = evaluer(p, x)
        fpx = evaluer(dp, x)
        if abs(fx) < tol:
            return x
        x = x - fx / fpx
    return x

p_ex = [-5, -2, 0, 1]
print(newton(p_ex, 2))
# utiliser '+' au lieu de '-' dans x - fx / fpx fait s'éloigner la suite de la racine

# Ex 4.3
p_osc = [2, -2, 0, 1]
print(newton(p_osc, 0))
# partir de x0 = 0 fait osciller le calcul entre 0 et 1 sans jamais converger

# Ex 4.4
t0 = time.perf_counter()
res_2 = newton(p_ex, 2)
t_2 = time.perf_counter() - t0

t0 = time.perf_counter()
res_0 = newton(p_ex, 0)
t_0 = time.perf_counter() - t0

print(res_2, res_0)
# partir d'un mauvais point de départ x0 = 0 demande beaucoup plus d'itérations que x0 = 2

# Ex 5.1
q = [-5, -2, 0, 1]
xs = [i / 100 for i in range(-300, 301)]
ys = [evaluer(q, x) for x in xs]

plt.figure()
plt.plot(xs, ys, label="x^3 - 2x - 5")
plt.axhline(0, color='black', linewidth=0.8)
plt.axvline(0, color='black', linewidth=0.8)
plt.ylim(-20, 20)
plt.show()
print("Racine réelle unique visible aux alentours de x = 2.09, les 2 autres sont complexes")
# confondre le nombre de racines réelles (1) avec le degré du polynôme (3)

# Ex 6.1
def somme_poly(p1, p2):
    n = max(len(p1), len(p2))
    res = [0] * n
    for i in range(n):
        c1 = p1[i] if i < len(p1) else 0
        c2 = p2[i] if i < len(p2) else 0
        res[i] = c1 + c2
    return res

def produit_poly(p1, p2):
    res = [0] * (len(p1) + len(p2) - 1)
    for i, c1 in enumerate(p1):
        for j, c2 in enumerate(p2):
            res[i + j] += c1 * c2
    return res

print(produit_poly([1, 1], [1, 1]))
print(produit_poly([-1, 1], [1, 1]))
# initialiser la liste produit avec une taille len(p1) * len(p2) au lieu de len(p1) + len(p2) - 1 crée un tableau trop grand

# Ex 6.2
p_pascal = [1]
for _ in range(10):
    p_pascal = produit_poly(p_pascal, [1, 1])
print(p_pascal)
# multiplier par [1, 1] revient à additionner les coefficients adjacents comme dans le triangle de Pascal

# Ex 7.1
def derivee_avant(f, x, h):
    return (f(x + h) - f(x)) / h

def derivee_centree(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)

f_sin = math.sin
v_exacte = math.cos(1)
for k in [1, 2, 4, 6, 8, 10, 12]:
    h = 10**(-k)
    e_av = abs(derivee_avant(f_sin, 1, h) - v_exacte)
    e_ct = abs(derivee_centree(f_sin, 1, h) - v_exacte)
    print(f"h=1e-{k} -> avant: {e_av:.2e}, centree: {e_ct:.2e}")
# prendre un h trop petit (ex: 1e-12) détruit la précision à cause de la soustraction de deux nombres très proches

# Ex 8.1
def rectangles(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + i * h) for i in range(n))

def trapezes(f, a, b, n):
    h = (b - a) / n
    return h * ((f(a) + f(b)) / 2 + sum(f(a + i * h) for i in range(1, n)))

def simpson(f, a, b, n):
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        k = 4 if i % 2 == 1 else 2
        s += k * f(a + i * h)
    return (h / 3) * s

f_sq2 = lambda x: x**2
print(rectangles(f_sq2, 0, 1, 10), trapezes(f_sq2, 0, 1, 10), simpson(f_sq2, 0, 1, 10))
# simpson nécessite un nombre pair de tranches n pour alterner correctement les coefficients 4 et 2

# Ex 8.2
f_pi = lambda x: 4 / (1 + x**2)
i_trap = trapezes(f_pi, 0, 1, 1000)
i_simp = simpson(f_pi, 0, 1, 1000)
print(abs(i_trap - math.pi), abs(i_simp - math.pi))
# faire sum(f(a + i*h) for i in range(n)) dans les trapèzes compte f(a) en trop dans la somme interne
