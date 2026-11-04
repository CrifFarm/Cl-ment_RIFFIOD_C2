import time

# Ex 1.1
def diviseurs(n):
    return [d for d in range(1, n + 1) if n % d == 0]

print(diviseurs(28))
# range(1, n) oublierait n qui est pourtant un diviseur de lui-même

# Ex 2.1
def pgcd_naif(a, b):
    for d in range(min(a, b), 0, -1):
        if a % d == 0 and b % d == 0:
            return d

def pgcd(a, b):
    while b:
        a, b = b, a % b
    return a

print(pgcd_naif(1071, 462), pgcd(1071, 462))
# pgcd_naif plante ou devient extrêmement lent si a ou b vaut 0

# Ex 3.1
def est_premier_naif(n):
    if n < 2:
        return False
    for d in range(2, n):
        if n % d == 0:
            return False
    return True

def est_premier(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True

def duree(f, x):
    t0 = time.perf_counter()
    f(x)
    return time.perf_counter() - t0

for v in [10007, 100003, 1000003]:
    print(duree(est_premier_naif, v), duree(est_premier, v))
# tester d <= n au lieu de d * d <= n rend la fonction extrêmement lente sur les grands nombres premiers

# Ex 4.1
def cribler(lim):
    t = [True] * (lim + 1)
    t[0] = t[1] = False
    d = 2
    while d * d <= lim:
        if t[d]:
            for m in range(d * d, lim + 1, d):
                t[m] = False
        d += 1
    return [i for i, p in enumerate(t) if p]

p = cribler(100000)
print(len(p))
# démarrer les multiples à 2 * d au lieu de d * d refait des opérations inutiles déjà traitées

# Ex 5.1
def facteurs(n):
    res = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            res.append(d)
            n //= d
        d += 1
    if n > 1:
        res.append(n)
    return res

print(facteurs(360))
# utiliser 'if n % d == 0:' au lieu de 'while' ne récupère pas les facteurs répétés (ex: 4 renvoie [2] au lieu de [2, 2])

# Ex 6.1
def fibo_rec(n):
    if n < 2:
        return n
    return fibo_rec(n - 1) + fibo_rec(n - 2)

t0 = time.perf_counter()
fibo_rec(30)
print(time.perf_counter() - t0)
# fibo_rec recalculant les mêmes valeurs explose exponentiellement en temps dès n > 30

# Ex 6.2
def fibo_rec_comptage(n, c):
    c[n] = c.get(n, 0) + 1
    if n < 2:
        return n
    return fibo_rec_comptage(n - 1, c) + fibo_rec_comptage(n - 2, c)

d_appels = {}
fibo_rec_comptage(30, d_appels)
print(d_appels.get(1, 0), sum(d_appels.values()))
# ne pas mémoriser les résultats intermédiaires force à calculer F(1) plus de 800 000 fois

# Ex 6.3
def fibo(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

print(fibo(25) == fibo_rec(25), len(str(fibo(10000))))
# réinitialiser a et b à chaque tour dans la boucle détruit la suite de Fibonacci

# Ex 7.1
def euclide_etendu(a, b):
    if b == 0:
        return a, 1, 0
    g, u, v = euclide_etendu(b, a % b)
    return g, v, u - (a // b) * v

print(euclide_etendu(1071, 462))
# inverser 'u' et 'v' dans la valeur de retour 'g, v, u - (a // b) * v' donne une combinaison linéaire fausse

# Ex 7.2
def puissance_mod_naive(a, e, n):
    r = 1
    for _ in range(e):
        r = (r * a) % n
    return r

def puissance_mod(a, e, n):
    r = 1
    a = a % n
    while e > 0:
        if e % 2 == 1:
            r = (r * a) % n
        a = (a * a) % n
        e //= 2
    return r

a, e, n = 7, 10**7, 1000003
print(duree(lambda: puissance_mod_naive(a, e, n), None))
print(duree(lambda: puissance_mod(a, e, n), None))
print(duree(lambda: pow(a, e, n), None))
# calculer a**e avant d'appliquer % n fait déborder la mémoire pour de très grands exposants
