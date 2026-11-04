import math
import random
import matplotlib.pyplot as plt

def orientation(p, q, r):
    d = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return 1 if d > 0 else (-1 if d < 0 else 0)

def se_coupent(a, b, c, d):
    o1, o2 = orientation(a, b, c), orientation(a, b, d)
    o3, o4 = orientation(c, d, a), orientation(c, d, b)
    return o1 != o2 and o3 != o4

def trajectoire_sans_frottement(v0, th_deg, g=9.81, n_pts=200):
    if v0 <= 0 or th_deg <= 0 or th_deg >= 90:
        return [], []
    rad = math.radians(th_deg)
    x_portee = (v0 ** 2 * math.sin(2 * rad)) / g
    xs, ys = [], []
    dx = x_portee / n_pts
    for i in range(n_pts + 1):
        x = i * dx
        y = x * math.tan(rad) - (g * x ** 2) / (2 * (v0 ** 2) * (math.cos(rad) ** 2))
        xs.append(x)
        ys.append(max(0.0, y))
    ys[-1] = 0.0  # évite un y = 1e-15 au point d'impact
    return xs, ys

def trajectoire_avec_frottement(v0, th_deg, k=0.01, g=9.81, dt=0.01):
    if v0 <= 0 or th_deg <= 0 or th_deg >= 90:
        return [], []
    rad = math.radians(th_deg)
    vx = v0 * math.cos(rad)
    vy = v0 * math.sin(rad)
    x, y = 0.0, 0.0
    xs, ys = [x], [y]
    for _ in range(200000):  # évite boucles infinies
        v = math.hypot(vx, vy)
        vx += -k * v * vx * dt
        vy += (-g - k * v * vy) * dt
        x_n, y_n = x + vx * dt, y + vy * dt
        if y_n < 0:
            # interpolation linéaire du point d'impact au sol
            r = y / (y - y_n)
            xs.append(x + r * (x_n - x))
            ys.append(0.0)
            break
        x, y = x_n, y_n
        xs.append(x)
        ys.append(y)
    return xs, ys

def calculer_trajectoire(v0, th, avec_frot=False, k=0.01):
    if avec_frot:
        return trajectoire_avec_frottement(v0, th, k=k)
    return trajectoire_sans_frottement(v0, th)

def tester_collision(xs, ys, obstacle, cible):
    """Renvoie (résultat, point d'impact, indice du segment touché)."""
    if len(xs) < 2:
        return "MANQUÉ", (0, 0), 0
    for i in range(len(xs) - 1):
        p1 = (xs[i], ys[i])
        p2 = (xs[i + 1], ys[i + 1])
        if se_coupent(p1, p2, obstacle[0], obstacle[1]):
            return "MUR", p2, i
        if se_coupent(p1, p2, cible[0], cible[1]):
            return "TOUCHÉ", p2, i
    return "MANQUÉ", (xs[-1], ys[-1]), len(xs) - 2

def simuler_tir(v0, th, obstacle, cible, avec_frot=False, k=0.01):
    """Calcule le tir et coupe la trajectoire au point d'impact."""
    xs, ys = calculer_trajectoire(v0, th, avec_frot, k)
    res, p, i = tester_collision(xs, ys, obstacle, cible)
    if xs:
        xs, ys = xs[:i + 1] + [p[0]], ys[:i + 1] + [p[1]]
    return res, xs, ys

def ecart_cible(th, v0, x_c, avec_frot=False, k=0.01):
    xs, ys = calculer_trajectoire(v0, th, avec_frot, k)
    if not xs:
        return -100.0
    # Si le tir n'atteint pas la distance x_cible
    if xs[-1] < x_c:
        return -(x_c - xs[-1])
    # Interpolation de la hauteur y à la position x_c
    for i in range(len(xs) - 1):
        if xs[i] <= x_c <= xs[i + 1]:
            r = (x_c - xs[i]) / (xs[i + 1] - xs[i]) if xs[i + 1] != xs[i] else 0
            return ys[i] + r * (ys[i + 1] - ys[i])
    return -(x_c - xs[-1])

def viser_tir_newton(v0, x_c, th0=45.0, avec_frot=False, k=0.01, tol=1e-2, max_it=15):
    th = th0
    h = 0.1
    for it in range(1, max_it + 1):
        fv = ecart_cible(th, v0, x_c, avec_frot, k)
        if abs(fv) < tol:
            return th, it, True
        dfv = (ecart_cible(th + h, v0, x_c, avec_frot, k) - ecart_cible(th - h, v0, x_c, avec_frot, k)) / (2 * h)
        if abs(dfv) < 1e-6:
            break
        th_n = th - fv / dfv
        if th_n <= 1 or th_n >= 88 or abs(th_n - th) > 30:
            return th, it, False
        th = th_n
    return th, max_it, False

def trouver_angles(v0, x_c, avec_frot=False, k=0.01, tol=1e-3):
    """Balaie 1°..85° par pas de 1° et fait une dichotomie sur chaque changement de signe."""
    angles = [float(a) for a in range(1, 86)]
    f = [ecart_cible(a, v0, x_c, avec_frot, k) for a in angles]
    sols = []
    for i in range(len(angles) - 1):
        if f[i] * f[i + 1] <= 0:
            a, b, fa = angles[i], angles[i + 1], f[i]
            it = 0
            while (b - a) > tol and it < 40:
                it += 1
                m = (a + b) / 2
                fm = ecart_cible(m, v0, x_c, avec_frot, k)
                if fa * fm <= 0:
                    b = m
                else:
                    a, fa = m, fm
            th = (a + b) / 2
            if not sols or abs(th - sols[-1][0]) > 0.1:
                sols.append((th, it))
    return sols

def viser_tir_dichotomie(v0, x_c, obstacle, cible, avec_frot=False, k=0.01):
    # On essaie les solutions de la plus tendue à la plus cloche
    # et on garde la première qui passe au-dessus du mur.
    for th, it in trouver_angles(v0, x_c, avec_frot, k):
        res, _, _ = simuler_tir(v0, th, obstacle, cible, avec_frot, k)
        if res == "TOUCHÉ":
            return th, it
    return None, 0

def viser_hybride(v0, x_c, obstacle, cible, avec_frot=False, k=0.01):
    # Newton depuis 3 angles de départ (45°, tir tendu, tir cloche)
    for th0 in (45.0, 20.0, 70.0):
        th_n, it_n, ok = viser_tir_newton(v0, x_c, th0=th0, avec_frot=avec_frot, k=k)
        if ok and simuler_tir(v0, th_n, obstacle, cible, avec_frot, k)[0] == "TOUCHÉ":
            return th_n, f"Newton ({it_n} it, départ {th0}°)"
    th_d, it_d = viser_tir_dichotomie(v0, x_c, obstacle, cible, avec_frot, k)
    if th_d is None:
        return None, f"Aucune solution (v0={v0} m/s : cible inatteignable ou mur infranchissable)"
    return th_d, f"Bascule Dichotomie (Newton échec, Dichotomie {it_d} it)"

def saisir(message, v_min, v_max):
    while True:
        try:
            val = float(input(message))
        except ValueError:
            print("  Entrée invalide, entre un nombre.")
            continue
        if v_min < val < v_max:
            return val
        print(f"  La valeur doit être comprise entre {v_min} et {v_max} (exclus).")

def tracer_tir(xs, ys, style, couleur, label):
    if xs:
        plt.plot(xs, ys, style, color=couleur, label=label)

def jouer():
    x_obs = 15.0
    h_obs = round(random.uniform(3.0, 5.0), 1)
    x_c, larg_c = 35.0, 4.0
    k_frot = round(random.uniform(0.005, 0.015), 3)
    obs = ((x_obs, 0), (x_obs, h_obs))
    cib = ((x_c - larg_c / 2, 0), (x_c + larg_c / 2, 0))
    print("=== JEU D'ARTILLERIE ===")
    print(f"Cible : x = {x_c}m (largeur {larg_c}m) | Mur : x = {x_obs}m, h = {h_obs}m | Frottement k = {k_frot}")
    print("\n--- Tir 1 : Sans frottement ---")
    v0_sans = saisir("Vitesse v0 (en m/s) : ", 0, 200)
    th_j_sans = saisir("Angle de tir (en °) : ", 0, 90)
    print("\n--- Tir 2 : Avec frottement ---")
    v0_avec = saisir("Vitesse v0 (en m/s) : ", 0, 200)
    th_j_avec = saisir("Angle de tir (en °) : ", 0, 90)
    plt.figure(figsize=(10, 5))
    plt.plot([x_obs, x_obs], [0, h_obs], color="red", linewidth=4, label=f"Mur ({h_obs}m)")
    plt.plot([cib[0][0], cib[1][0]], [0, 0], color="green", linewidth=6, label="Cible")
    courbes = []
    # 1. Tir joueur SANS frottement
    res_j1, xs_j1, ys_j1 = simuler_tir(v0_sans, th_j_sans, obs, cib)
    tracer_tir(xs_j1, ys_j1, "--", "orange", f"Joueur sans frottement ({v0_sans}m/s, {th_j_sans}°) -> {res_j1}")
    # 2. Tir joueur AVEC frottement
    res_j2, xs_j2, ys_j2 = simuler_tir(v0_avec, th_j_avec, obs, cib, avec_frot=True, k=k_frot)
    tracer_tir(xs_j2, ys_j2, "--", "brown", f"Joueur avec frottement ({v0_avec}m/s, {th_j_avec}°) -> {res_j2}")
    # 3. IA sans frottement
    th1, m1 = viser_hybride(v0_sans, x_c, obs, cib)
    xs_a1, ys_a1 = [], []
    if th1 is not None:
        _, xs_a1, ys_a1 = simuler_tir(v0_sans, th1, obs, cib)
        tracer_tir(xs_a1, ys_a1, "-", "blue", f"IA sans frottement ({round(th1, 1)}°) [{m1}]")
    # 4. IA avec frottement
    th2, m2 = viser_hybride(v0_avec, x_c, obs, cib, avec_frot=True, k=k_frot)
    xs_a2, ys_a2 = [], []
    if th2 is not None:
        _, xs_a2, ys_a2 = simuler_tir(v0_avec, th2, obs, cib, avec_frot=True, k=k_frot)
        tracer_tir(xs_a2, ys_a2, "-", "purple", f"IA avec frottement ({round(th2, 1)}°) [{m2}]")
    print("\n=== RÉSULTATS ===")
    print(f"Joueur sans frottement : {res_j1}")
    print(f"Joueur avec frottement : {res_j2}")
    print(f"IA sans frottement     : {m1}")
    print(f"IA avec frottement     : {m2}")
    courbes = [(xs_j1, ys_j1), (xs_j2, ys_j2), (xs_a1, ys_a1), (xs_a2, ys_a2)]
    max_x = max([max(xs) for xs, _ in courbes if xs] + [x_c + 10])
    max_y = max([max(ys) for _, ys in courbes if ys] + [h_obs + 5])
    plt.axhline(0, color="black", linewidth=1)
    plt.xlim(-1, max_x + 5)
    plt.ylim(-1, max_y * 1.35)
    plt.title(f"Artillerie : Mur {h_obs}m | Frottement k = {k_frot}")
    plt.xlabel("Distance x (m)")
    plt.ylabel("Hauteur y (m)")
    plt.legend(loc="upper left", fontsize=8, framealpha=0.9)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    jouer()
