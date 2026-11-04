# Clement_RIFFIOD_C2
# Projet de Module - Jeu d'Artillerie & Solveur Hybride

Ce projet met en œuvre un simulateur de jeu d'artillerie écrit en Python. Le joueur tire deux fois (sans puis avec frottement de l'air) et une IA calcule l'angle de tir gagnant, en tenant compte d'un mur placé devant la cible. Le projet utilise les notions de calcul numérique et de géométrie algorithmique vues en TP.

## Structure du dépôt
- `tp/` : résolutions des TP 1 à 6.
- `projet/` : code du projet (`artillerie.py`).
- `README.md` : explications du projet et analyse critique.

## Utilisation
```
pip install matplotlib
python projet/artillerie.py
```
Le mur a une hauteur aléatoire (3 à 5 m) et le coefficient de frottement `k` est aussi tiré au hasard. Le programme demande une vitesse `v0` (m/s) et un angle (°) pour chaque tir, puis affiche les trajectoires et les résultats (TOUCHÉ / MUR / MANQUÉ).

## Notions des TP utilisées
1. **Géométrie algorithmique (TP6)**
   - Détection d'intersection de segments par signe de déterminants 2x2 (`orientation`, `se_coupent`), utilisée pour les collisions avec le mur et la cible, sans bibliothèque externe.
2. **Recherche de racines (TP3)**
   - **Newton** avec dérivée centrée numérique pour trouver l'angle $\theta$.
   - **Dichotomie** comme méthode de secours.
3. **Calcul numérique (TP1 & TP3)**
   - Frottement de l'air (force $-k\,\|v\|\,\vec v$) intégré par la méthode d'Euler, avec interpolation linéaire du point d'impact au sol.

## Fonctionnement de l'IA hybride
L'IA cherche l'angle $\theta$ qui annule la fonction $f(\theta)$ : la hauteur du tir à l'abscisse de la cible (qui est au sol). Si le tir n'atteint pas la cible, $f$ vaut l'opposé de la distance manquante, ce qui garde $f$ continue.

1. **Newton** est essayé depuis trois angles de départ (45°, 20° pour le tir tendu, 70° pour le tir en cloche).
2. Une solution n'est acceptée que si la trajectoire simulée est bien **TOUCHÉ** : un angle qui annule $f$ mais fait traverser le mur est rejeté.
3. Si Newton échoue, le programme **balaie 1° à 85° par pas de 1°**, repère tous les changements de signe de $f$ et applique la **dichotomie** sur chacun. On garde la première solution qui passe le mur (tir tendu en priorité, sinon tir en cloche).
4. Si aucune solution n'existe (vitesse trop faible, mur trop haut), l'IA l'indique au lieu de tirer au hasard.

## Regard critique
- **Newton** converge en général en 3 à 5 itérations, avec ou sans frottement. Il peut échouer car $f$ n'est pas dérivable au point où la portée devient égale à la distance de la cible, et car sa dérivée s'annule près de la portée maximale. Il peut alors sortir de $]1°, 88°[$ ou converger vers un tir qui touche le mur.
- **La dichotomie** converge à coup sûr dans un intervalle où $f$ change de signe. Il faut donc d'abord les repérer : sans le balayage, un intervalle fixe comme [1°, 45°] / [45°, 85°] peut les manquer, car avec frottement la portée maximale est atteinte avant 45°.
- **Limites du modèle**
  - Euler avec $dt = 0{,}01$ s : précision limitée (erreur de l'ordre du centimètre à quelques centimètres).
  - Le mur est un segment sans épaisseur.
  - Le frottement est quadratique, sans vent réel (pas de composante horizontale).
  - Le balayage au pas de 1° peut manquer deux solutions très proches.

## Utilisation de l'IA
Une IA a généré la structure initiale du code et aidé au tracé Matplotlib. Le code a ensuite été relu et corrigé à la main : prise en compte du mur par l'IA de tir, balayage des angles pour la dichotomie, interpolation de l'impact, validation des saisies. Il a été testé sur plusieurs tirages aléatoires.
