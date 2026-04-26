# ML-KEM (Kyber) y ML-DSA (Dilithium)

**Módulo 36 · Artículo 1 · Nivel muy avanzado**

---

## El problema de retícula: fundamento matemático

La seguridad de Kyber y Dilithium descansa sobre el problema **Module-LWE (MLWE)**:

**Learning With Errors (LWE):** dado $(A, b = As + e)$ donde:
- $A \in \mathbb{Z}_q^{m \times n}$ es aleatoria y pública
- $s \in \mathbb{Z}_q^n$ es el secreto
- $e$ es un vector de ruido pequeño (distribución gaussiana centrada)

es computacionalmente difícil encontrar $s$ — incluso para ordenadores cuánticos
(no hay algoritmo sub-exponencial conocido).

**Module-LWE** usa módulos de polinomios $R_q = \mathbb{Z}_q[X]/(X^n+1)$ en lugar
de vectores de enteros, permitiendo claves más compactas.

```python
import numpy as np

def gen_lwe_instance(n: int = 256, q: int = 3329, sigma: float = 1.0,
                      seed: int = 0) -> dict:
    """
    Genera una instancia LWE pedagógica.
    
    n: dimensión del secreto
    q: módulo (3329 en Kyber — primo para facilitar NTT)
    sigma: desviación estándar del ruido
    """
    rng = np.random.default_rng(seed)

    # Secreto uniforme en Z_q
    s = rng.integers(0, q, n)

    # Matriz pública A ∈ Z_q^{m×n}
    m = 2 * n
    A = rng.integers(0, q, (m, n))

    # Ruido gaussiano (redondeado y reducido mod q)
    e = np.round(rng.normal(0, sigma, m)).astype(int)

    # b = As + e mod q
    b = (A @ s + e) % q

    # Dificultad: dado (A, b), encontrar s
    return {
        'n': n, 'q': q, 'sigma': sigma,
        'A_shape': A.shape,
        'norma_s': np.linalg.norm(s),
        'norma_e': np.linalg.norm(e),
        'ratio_e_b': np.linalg.norm(e) / np.linalg.norm(b),
    }

r = gen_lwe_instance()
print('Instancia LWE pedagógica:')
print(f'  n = {r["n"]}, q = {r["q"]}')
print(f'  A: {r["A_shape"][0]}×{r["A_shape"][1]}')
print(f'  ‖s‖ = {r["norma_s"]:.1f}')
print(f'  ‖e‖ = {r["norma_e"]:.1f}  (ruido)')
print(f'  ‖e‖/‖b‖ = {r["ratio_e_b"]:.4f}  (ruido relativo)')
print(f'\nSin conocer s, distinguir b=As+e de un vector aleatorio es MLWE hard.')
```

---

## ML-KEM (Kyber): esquema de encapsulación de clave

Kyber usa tres parámetros de seguridad: Kyber-512 (128 bits), Kyber-768 (192 bits),
Kyber-1024 (256 bits). Aquí simulamos la lógica de Kyber-512.

```python
def kyber_toy(n: int = 8, q: int = 17, k: int = 2, sigma: float = 1.0,
               seed: int = 0) -> dict:
    """
    Implementación pedagógica de Kyber (versión toy, sin NTT ni seguridad real).
    
    Kyber real usa: n=256, q=3329, k=2/3/4, polinomios en Z_q[X]/(X^n+1).
    Esta versión usa vectores de enteros para claridad conceptual.
    """
    rng = np.random.default_rng(seed)

    # === Generación de claves ===
    # Clave pública: (A, t = As + e)
    A = rng.integers(0, q, (k*n, k*n))
    s = rng.integers(0, 2, k*n)      # secreto binario (simplificado)
    e = np.round(rng.normal(0, sigma, k*n)).astype(int)
    t = (A @ s + e) % q

    # Clave privada: s
    # Clave pública: (A, t)

    # === Encapsulación (Alice) ===
    # Genera mensaje m = 0 o 1 por bit
    m = rng.integers(0, 2, n)
    
    # Ruido fresco
    r_vec = rng.integers(0, 2, k*n)
    e1 = np.round(rng.normal(0, sigma, k*n)).astype(int)
    e2 = np.round(rng.normal(0, sigma, n)).astype(int)

    # Ciphertext
    u = (A.T @ r_vec + e1) % q           # u ∈ Z_q^{kn}
    v = (t @ r_vec + e2 + (q//2)*m) % q  # v ∈ Z_q^n

    # === Desencapsulación (Bob) ===
    # m' ≈ v - s·u (con ruido pequeño)
    w = (v - s @ u[:n]) % q   # simplificado

    # Decodificar: bits donde w es cercano a q/2 → 1, cercano a 0 → 0
    m_rec = np.where(np.abs(w - q//2) < q//4, 1, 0)

    # Tasa de error de bit
    ber = np.mean(m != m_rec[:n])

    return {
        'n': n, 'q': q, 'k': k,
        'm_original': m[:8],   # primeros 8 bits
        'm_recuperado': m_rec[:8],
        'BER': ber,
        'pk_size_bytes': (k*n * 2 * 12 + 256) // 8,  # estimado Kyber-512
        'ct_size_bytes': (k*n * 12 + n * 12) // 8,
    }

r = kyber_toy()
print('Kyber pedagógico (toy, sin seguridad real):')
print(f'  m original:   {r["m_original"]}')
print(f'  m recuperado: {r["m_recuperado"]}')
print(f'  BER: {r["BER"]:.4f}')
print()

# Tamaños de claves reales de Kyber (FIPS 203)
print('Tamaños de clave ML-KEM (estándar FIPS 203):')
kyber_params = [
    ('ML-KEM-512',  1632, 800,  768, '128 bits (AES-128 equiv.)'),
    ('ML-KEM-768',  2400, 1184, 1088, '192 bits (AES-192 equiv.)'),
    ('ML-KEM-1024', 3168, 1568, 1568, '256 bits (AES-256 equiv.)'),
]
print(f'{"Variante":>15} | {"sk (B)":>8} | {"pk (B)":>8} | {"ct (B)":>8} | {"Seguridad"}')
print('-' * 60)
for nombre, sk, pk, ct, seg in kyber_params:
    print(f'{nombre:>15} | {sk:>8} | {pk:>8} | {ct:>8} | {seg}')

# Comparativa con RSA y ECDH
print('\nComparativa con criptografía clásica:')
clasica = [
    ('RSA-2048',   256, 256, 256, '112 bits — ROTO por Shor'),
    ('RSA-4096',   512, 512, 512, '140 bits — ROTO por Shor'),
    ('ECDH-256',  32,  64,  32,  '128 bits — ROTO por Shor'),
]
for nombre, sk, pk, ct, seg in clasica:
    print(f'{nombre:>15} | {sk:>8} | {pk:>8} | {ct:>8} | {seg}')
```

---

## ML-DSA (Dilithium): firma digital

Dilithium (ML-DSA) es el estándar NIST para firmas digitales post-cuánticas.
Basado en el problema MLWE y MSIS (Module-SIS).

```python
def dilithium_conceptual(nivel: int = 2) -> dict:
    """
    Parámetros conceptuales de Dilithium (ML-DSA).
    
    No implementa la criptografía real — muestra los parámetros y la lógica.
    """
    # Parámetros de ML-DSA (FIPS 204)
    params = {
        2: {'n': 256, 'q': 8380417, 'k': 4, 'l': 4,
            'eta': 2, 'gamma1': 131072, 'gamma2': 95232,
            'sk_bytes': 2528, 'pk_bytes': 1312, 'sig_bytes': 2420,
            'seguridad': '128 bits'},
        3: {'n': 256, 'q': 8380417, 'k': 6, 'l': 5,
            'eta': 4, 'gamma1': 524288, 'gamma2': 261888,
            'sk_bytes': 4000, 'pk_bytes': 1952, 'sig_bytes': 3293,
            'seguridad': '192 bits'},
        5: {'n': 256, 'q': 8380417, 'k': 8, 'l': 7,
            'eta': 2, 'gamma1': 524288, 'gamma2': 261888,
            'sk_bytes': 4864, 'pk_bytes': 2592, 'sig_bytes': 4595,
            'seguridad': '256 bits'},
    }
    p = params[nivel]

    # La lógica de firma (simplificada):
    # 1. Clave privada: s₁ ∈ R_q^l, s₂ ∈ R_q^k (coeficientes pequeños ≤ η)
    # 2. Clave pública: (A, t = As₁ + s₂) donde A es la "semilla"
    # 3. Firma: z = y + cs₁, h (hint para reconstruir t)
    #           donde y es nonce, c es hash del mensaje
    # 4. Verificación: Az ≈ ct + h·2^d (con tolerancia de redondeo)

    return p

print('Parámetros ML-DSA (FIPS 204):')
print(f'{"Nivel":>8} | {"sk (B)":>8} | {"pk (B)":>8} | {"sig (B)":>9} | {"Seguridad"}')
print('-' * 50)
for nivel in [2, 3, 5]:
    p = dilithium_conceptual(nivel)
    print(f'{"ML-DSA-" + str(nivel*17+len(str(nivel))):>8} | '  # aproximación nombre
          f'{p["sk_bytes"]:>8} | {p["pk_bytes"]:>8} | {p["sig_bytes"]:>9} | {p["seguridad"]}')

# Comparativa con ECDSA
print('\nComparativa ML-DSA vs ECDSA:')
print(f'{"Algoritmo":>15} | {"sk (B)":>8} | {"pk (B)":>8} | {"sig (B)":>9} | {"Resistente QC"}')
print('-' * 60)
for row in [
    ('ML-DSA-44',  2528, 1312, 2420, '✅ Sí (retícula)'),
    ('ECDSA P-256',  32,   64,   64, '❌ No (Shor)'),
    ('ECDSA P-384',  48,   96,   96, '❌ No (Shor)'),
    ('RSA-PSS-2048', 256, 256,  256, '❌ No (Shor)'),
    ('Ed25519',      32,   32,   64, '❌ No (Shor)'),
]:
    print(f'{row[0]:>15} | {row[1]:>8} | {row[2]:>8} | {row[3]:>9} | {row[4]}')
```

---

## Number Theoretic Transform (NTT): la operación clave

La eficiencia de Kyber/Dilithium depende de la NTT para multiplicar polinomios
en $R_q = \mathbb{Z}_q[X]/(X^n+1)$ en $O(n \log n)$ en lugar de $O(n^2)$.

```python
def ntt_naive(a: list[int], q: int = 3329, n: int = 256) -> list[int]:
    """
    NTT (Number Theoretic Transform) ingenua para Z_q[X]/(X^n+1).
    
    Kyber usa q=3329, n=256, con primitiva raíz de la unidad ω = 17^((q-1)/512) mod q.
    
    Esta implementación es O(n²) — solo pedagógica.
    """
    omega = pow(17, (q-1)//(2*n), q)  # raíz primitiva 2n-ésima mod q
    result = [0] * n
    for k in range(n):
        s = 0
        for j in range(n):
            s = (s + a[j] * pow(omega, j*k, q)) % q
        result[k] = s
    return result

def poly_mul_mod(a: list[int], b: list[int], q: int = 17, n: int = 4) -> list[int]:
    """
    Multiplicación de polinomios mod (X^n + 1) y mod q.
    a, b ∈ Z_q[X]/(X^n+1)
    """
    c = [0] * n
    for i in range(n):
        for j in range(n):
            idx = (i + j) % n
            sign = -1 if (i + j) >= n else 1  # reducción mod X^n+1
            c[idx] = (c[idx] + sign * a[i] * b[j]) % q
    return c

# Ejemplo de multiplicación de polinomios en Z_17[X]/(X^4+1)
a_poly = [3, 1, 4, 1]  # 3 + x + 4x² + x³
b_poly = [5, 9, 2, 6]  # 5 + 9x + 2x² + 6x³
c_poly = poly_mul_mod(a_poly, b_poly, q=17, n=4)

print(f'Multiplicación en Z_17[X]/(X^4+1):')
print(f'  a(x) = {a_poly[0]} + {a_poly[1]}x + {a_poly[2]}x² + {a_poly[3]}x³')
print(f'  b(x) = {b_poly[0]} + {b_poly[1]}x + {b_poly[2]}x² + {b_poly[3]}x³')
print(f'  c(x) = {c_poly[0]} + {c_poly[1]}x + {c_poly[2]}x² + {c_poly[3]}x³  (mod 17, X^4+1)')

# Rendimiento teórico
print(f'\nNTT: O(n log n) vs multiplicación naïve O(n²)')
for n in [256, 512, 1024]:
    naive_ops = n**2
    ntt_ops = 2 * n * int(np.log2(n))
    speedup = naive_ops / ntt_ops
    print(f'  n={n}: naïve={naive_ops:,}, NTT≈{ntt_ops:,}, speedup≈×{speedup:.0f}')
```

---

## Seguridad cuántica: análisis del mejor ataque conocido

El mejor ataque cuántico contra LWE es el **algoritmo de Grover** combinado
con técnicas de retícula (BKZ). El nivel de seguridad cuántica es:

```python
def seguridad_kyber(variante: str) -> dict:
    """
    Análisis de seguridad de Kyber contra ataques cuánticos.
    Basado en los estimadores de CRYSTALS-Kyber v3.
    """
    params = {
        'Kyber-512':  {'n': 256, 'k': 2, 'q': 3329, 'eta1': 3, 'eta2': 2,
                       'bits_clasico': 118, 'bits_cuantico': 107},
        'Kyber-768':  {'n': 256, 'k': 3, 'q': 3329, 'eta1': 2, 'eta2': 2,
                       'bits_clasico': 183, 'bits_cuantico': 161},
        'Kyber-1024': {'n': 256, 'k': 4, 'q': 3329, 'eta1': 2, 'eta2': 2,
                       'bits_clasico': 247, 'bits_cuantico': 218},
    }
    return params.get(variante, {})

print('\nAnálisis de seguridad cuántica de Kyber (estimadores BKZ+Grover):')
print(f'{"Variante":>14} | {"Bits clásicos":>14} | {"Bits cuánticos":>15} | {"NIST nivel"}')
print('-' * 58)
niveles = {'Kyber-512': 'I (128)', 'Kyber-768': 'III (192)', 'Kyber-1024': 'V (256)'}
for v in ['Kyber-512', 'Kyber-768', 'Kyber-1024']:
    p = seguridad_kyber(v)
    print(f'{v:>14} | {p["bits_clasico"]:>14} | {p["bits_cuantico"]:>15} | {niveles[v]}')

print('\nNota: "bits cuánticos" = coste del mejor ataque cuántico conocido.')
print('No existe algoritmo cuántico sub-exponencial para MLWE (a diferencia de RSA/ECDH).')
```

---

**Referencias:**
- Bos et al., *CRYSTALS-Kyber* (2017) — diseño original
- NIST, *FIPS 203: ML-KEM* (2024) — estándar oficial
- Ducas et al., *CRYSTALS-Dilithium* (2018) — diseño original
- NIST, *FIPS 204: ML-DSA* (2024) — estándar oficial
- Peikert, *Communications of the ACM* 62, 3 (2019) — introducción a retículas
