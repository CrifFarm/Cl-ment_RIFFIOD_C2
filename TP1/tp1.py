import math
import sys
from fractions import Fraction

# Ex 1.1
q = 2026 // 7
r = 2026 % 7
print(q, r)
# 2026 / 7 renvoie 289.42857142857144 au lieu d'un entier

# Ex 1.2
n = 123456789
d = n % 10
s = n // 10
print(d, s)
# pour n < 0 (ex: -123), -123 % 10 renvoie 7 et non -3

# Ex 2.1
s = 0.0
for _ in range(1000):
    s += 0.1
e = abs(s - 100)
print(s, e)
# s ne vaut pas 100.0 exactement car 0.1 ne s'écrit pas exactement en binaire

# Ex 2.2
def presque_egaux(a, b, tol=1e-9):
    return abs(a - b) < tol

print(presque_egaux(0.1 + 0.2, 0.3))
# presque_egaux(1e20, 1e20 + 1) renvoie False alors que l'écart dépasse la tolérance fixe malgré l'échelle

# Ex 3.1
for i in range(1, 11):
    print(f"7 x {i} = {7 * i}")
# range(1, 10) s'arrête à 9 au lieu de 10

# Ex 3.2
sb = 0
for i in range(1, 101):
    sb += i
sf = 100 * 101 // 2
print(sb, sf)
# 100 * 101 / 2 renvoie 5050.0 (float) au lieu d'un entier exact

# Ex 4.1
def nombre_de_chiffres(n):
    if n == 0:
        return 1
    c = 0
    t = abs(n)
    while t > 0:
        t //= 10
        c += 1
    return c

print(nombre_de_chiffres(2026), nombre_de_chiffres(7))
# sans le cas n == 0, la boucle ne s'exécute pas et renvoie 0 au lieu de 1

# Ex 5.1
def heron(a):
    x = a
    while True:
        xs = 0.5 * (x + a / x)
        if math.isclose(x, xs, abs_tol=1e-12):
            return xs
        x = xs

print(heron(2))
# heron(0) provoque une division par zéro et heron(-2) boucle à l'infini

# Ex 6.1
def vers_binaire(n):
    if n == 0:
        return "0"
    res = ""
    t = n
    while t > 0:
        res = str(t % 2) + res
        t //= 2
    return res

print(vers_binaire(37), vers_binaire(0))
# faire res += str(t % 2) inverse les bits du résultat

# Ex 6.2
eps = 1.0
while 1.0 + (eps / 2.0) != 1.0:
    eps /= 2.0
print(eps)
# tester 1.0 + eps != 1.0 directement divise eps une fois de trop

# Ex 7.1
def racines_naif(a, b, c):
    d = b**2 - 4*a*c
    r1 = (-b + math.sqrt(d)) / (2*a)
    r2 = (-b - math.sqrt(d)) / (2*a)
    return r1, r2

r1, r2 = racines_naif(1, -10**8, 1)
print(r1, r2, r1 * r2)
# pour b très grand, -b - sqrt(d) soustrait deux nombres très proches et perd toute précision

# Ex 7.2
def racines(a, b, c):
    d = b**2 - 4*a*c
    if b < 0:
        r1 = (-b + math.sqrt(d)) / (2*a)
    else:
        r1 = (-b - math.sqrt(d)) / (2*a)
    r2 = c / (a * r1)
    return r1, r2

r1, r2 = racines(1, -10**8, 1)
print(r1, r2, r1 * r2)

# Ex 7.3
s = sum(Fraction(1, 10) for _ in range(1000))
print(s)
print(Fraction(1, 10) + Fraction(2, 10) == Fraction(3, 10))
# utiliser Fraction(0.1) au lieu de Fraction(1, 10) conserve l'erreur du float d'origine
