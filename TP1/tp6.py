import math
import random
import matplotlib.pyplot as plt

# Ex 1.1
def vecteur(a, b):
    return (b[0] - a[0], b[1] - a[1])

def produit_scalaire(u, v):
    return u[0] * v[0] + u[1] * v[1]

def norme(u):
    return math.sqrt(produit_scalaire(u, u))

def angle(u, v):
    cos_t = produit_scalaire(u, v) / (norme(u) * norme(v))
    return math.degrees(math.acos(max(-1.0, min(1.0, cos_t))))

print(norme((3, 4)), produit_scalaire((1, 2), (3, 4)), angle((1, 0), (1, 1)), angle((1, 0), (0, 1)))
# diviser par norme(u) + norme(v) au lieu du produit des normes dans cos_t renvoie des angles absurdes

# Ex 1.2
def determinant(u, v):
    return u[0] * v[1] - u[1] * v[0]

def distance_point_droite(p, a, b):
    ab, ap = vecteur(a, b), vecteur(a, p)
    return abs(determinant(ab, ap)) / norme(ab)

print(distance_point_droite((0, 0), (0, 1), (1, 0)), distance_point_droite((3, 4), (0, 0), (1, 0)))
# inverser ux*vy - uy*vx en ux*vx - uy*vy ne calcule pas le determinant 2x2 mais un produit terme a terme

# Ex 2.1
def orientation(a, b, c):
    d = determinant(vecteur(a, b), vecteur(b, c))
    return 1 if d > 0 else (-1 if d < 0 else 0)

print(orientation((0, 0), (1, 0), (1, 1)), orientation((0, 0), (1, 0), (1, -1)), orientation((0, 0), (1, 1), (2, 2)))
# inverser les signes > et < fait confondre les virages a gauche et a droite

# Ex 2.2
def aire(poly):
    n = len(poly)
    s = sum(poly[i][0] * poly[(i + 1) % n][1] - poly[(i + 1) % n][0] * poly[i][1] for i in range(n))
    return abs(s) / 2.0

maison = [(0, 0), (2, 0), (2, 1.5), (1, 2.5), (0, 1.5)]
print(aire([(0, 0), (1, 0), (1, 1), (0, 1)]), aire([(0, 0), (4, 0), (0, 3)]), aire(maison))
# oublier l'indice (i + 1) % n pour le dernier sommet omet de relier le dernier point au premier

# Ex 3.1
def se_coupent(a, b, c, d):
    o1, o2 = orientation(a, b, c), orientation(a, b, d)
    o3, o4 = orientation(c, d, a), orientation(c, d, b)
    return o1 != o2 and o3 != o4

print(se_coupent((0, 0), (1, 1), (0, 1), (1, 0)), se_coupent((0, 0), (1, 0), (0, 1), (1, 1)))
# o1 != o2 seul teste si la droite (AB) coupe le segment [CD], mais oublie de verifier si le segment [AB] coupe la droite (CD)

# Ex 3.2
def intersection(a, b, c, d):
    if not se_coupent(a, b, c, d):
        return None
    ab, cd, ac = vecteur(a, b), vecteur(c, d), vecteur(a, c)
    denom = determinant(ab, cd)
    if denom == 0:
        return None
    t = determinant(ac, cd) / denom
    return (a[0] + t * ab[0], a[1] + t * ab[1])

print(intersection((0, 0), (2, 2), (0, 2), (2, 0)))
# diviser par determinant(ab, ac) au lieu de determinant(ab, cd) donne un t faux pour le point d'intersection

# Ex 4.1
def dedans(p, poly):
    n = len(poly)
    cnt = 0
    x, y = p
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        if (a[1] <= y < b[1]) or (b[1] <= y < a[1]):
            x_int = a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x_int > x:
                cnt += 1
    return cnt % 2 == 1

print(dedans((1, 1), maison), dedans((1, 2.4), maison), dedans((3, 1), maison), dedans((0.2, 2.2), maison))
# utiliser a[1] <= y <= b[1] sans inégalité stricte sur un des bords compte les sommets deux fois et fausse la parite du lancer de rayon

# Ex 4.2
random.seed(1)
n_pts = 200000
dans_m = sum(1 for _ in range(n_pts) if dedans((random.uniform(0, 2), random.uniform(0, 2.5)), maison))
aire_mc = (dans_m / n_pts) * (2.0 * 2.5)
print(aire_mc)
# oublier de multiplier la proportion par l'aire totale du rectangle englobant (2.0 * 2.5 = 5.0) renvoie une valeur entre 0 et 1

# Ex 5.1
p_non_convexe = [(0, 0), (2, 0), (2, 2), (1, 1), (0, 2)]
print(aire(p_non_convexe), dedans((1, 0.5), p_non_convexe), dedans((1, 1.5), p_non_convexe))
# supposer qu'un polymorphisme non convexe nécessite de le découper en triangles oublie que le lancer de rayon et la formule du lacet restent valides

# Ex 6.1
def zone_de(p, zones):
    for i, z in enumerate(zones):
        if dedans(p, z):
            return i
    return None

carre = [(3, 0), (4, 0), (4, 1), (3, 1)]
zones = [maison, carre]
print(zone_de((1, 1), zones), zone_de((3.5, 0.5), zones), zone_de((2.5, 0.5), zones))
# tester seulement la distance au centre du polygone échoue si les zones ont des formes complexes ou imbriquees
