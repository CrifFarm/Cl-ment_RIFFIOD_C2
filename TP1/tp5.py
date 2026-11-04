import math
import random
from collections import Counter

# Ex 1.1
def l2n(c):
    return ord(c.upper()) - ord('A')

def n2l(n):
    return chr(n % 26 + ord('A'))

print(l2n("C"), n2l(2))
# utiliser ord(c) sans soustraire ord('A') renvoie 67 au lieu de l'indice 2

# Ex 1.2
def nettoyer(txt):
    acc = "ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝ"
    rep = "AAAAAAACEEEEIIIIDNOOOOOOUUUUY"
    t = txt.upper()
    for a, r in zip(acc, rep):
        t = t.replace(a, r)
    return "".join(c for c in t if 'A' <= c <= 'Z')

print(nettoyer("Été, à Paris !"))
# oublier de remplacer les lettres accentuees supprime complètement 'É' et 'à' au lieu de les transformer en 'E' et 'A'

# Ex 2.1
def chiffrer(txt, a, b):
    t = nettoyer(txt)
    return "".join(n2l(a * l2n(c) + b) for c in t)

print(chiffrer("ATTAQUEALAUBE", 5, 8))
# appliquer (a * x + b) sans le modulo 26 fait deborder les codes ascii lors de la conversion en caractère

# Ex 3.1
cles_valides = [a for a in range(1, 26) if math.gcd(a, 26) == 1]
print(cles_valides, len(cles_valides))
# inclure des valeurs paires ou 13 dans les cles invalide la fonction de dechiffrement car pgcd(a, 26) != 1

# Ex 3.2
def inv_mod(a, n=26):
    if math.gcd(a, n) != 1:
        raise ValueError(f"{a} pas inversible mod {n}")
    return pow(a, -1, n)

print(inv_mod(5, 26))
# calculer 1 / a avec une division flottante au lieu de l'inverse modulaire renvoie un float inexploitable pour le modulo

# Ex 4.1
def dechiffrer(txt, a, b):
    a_inv = inv_mod(a, 26)
    return "".join(n2l(a_inv * (l2n(c) - b)) for c in txt)

msg = "ATTAQUEALAUBE"
ciph = chiffrer(msg, 5, 8)
print(dechiffrer(ciph, 5, 8))
# utiliser une cle a non inversible (ex: a=4) fait lever une exception au lieu de dechiffrer le message

# Ex 5.1
def toutes_les_clefs(secret):
    res = []
    for a in cles_valides:
        for b in range(26):
            res.append(((a, b), dechiffrer(secret, a, b)))
    return res

props = toutes_les_clefs(ciph)
print(len(props), props[0])
# tester les 26 valeurs de 'a' au lieu de se limiter aux 12 cles valides provoque un plantage sur les cles non inversibles

# Ex 6.1
def casser_frequence(secret):
    c = Counter(secret)
    p_frequente = c.most_common(1)[0][0]
    y = l2n(p_frequente)
    x = l2n('E')
    candidats = []
    for a in cles_valides:
        b = (y - a * x) % 26
        candidats.append(((a, b), dechiffrer(secret, a, b)))
    return candidats

print(casser_frequence(ciph))
# sur un texte tres court la lettre la plus frequente n'est pas forcement 'E', l'attaque par frequence simple peut donc echouer

# Ex 7.1
def ic(txt):
    n = len(txt)
    if n <= 1:
        return 0.0
    c = Counter(txt)
    return sum(v * (v - 1) for v in c.values()) / (n * (n - 1))

txt_long = chiffrer("LECHIFFREMENTAFFINEESTUNECRYPTOGRAPHIECLASSIQUEFACILEACASSER" * 5, 5, 8)
rand_txt = "".join(n2l(random.randint(0, 25)) for _ in range(len(txt_long)))
print(ic(txt_long), ic(rand_txt))
# utiliser n**2 au lieu de n*(n-1) au denominateur fausse la valeur de l'indice de coincidence pour les textes courts

# Ex 8.1
def vigenere(txt, cle):
    t = nettoyer(txt)
    k = [l2n(c) for c in cle]
    return "".join(n2l(l2n(t[i]) + k[i % len(k)]) for i in range(len(t)))

v_ciph = vigenere(txt_long, "CLE")
print(ic(v_ciph))
# oublier de répéter la cle avec i % len(k) produit un debordement d'index IndexError sur les textes longs

# Ex 8.2
def longueur_cle(secret, max_l=7):
    ics = []
    for l in range(1, max_l + 1):
        cols = [secret[i::l] for i in range(l)]
        ic_m = sum(ic(col) for col in cols) / l
        ics.append((l, ic_m))
    return ics

print(longueur_cle(v_ciph))
# decouper en tranches de taille l au lieu d'extraire une lettre tous les l pas secret[i::l] ne separe pas les sous-textes chiffres par le meme decalage
