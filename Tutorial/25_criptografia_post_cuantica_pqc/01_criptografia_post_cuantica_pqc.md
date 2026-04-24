# Criptografía post-cuántica (PQC)

## 1. El problema: Shor amenaza la infraestructura criptográfica actual

El algoritmo de Shor factoriza enteros de $n$ bits en tiempo $O(n^3)$ con un procesador cuántico. Esto amenaza directamente los sistemas criptográficos asimétricos más usados:

- **RSA:** su seguridad depende de la dificultad de factorizar el producto de dos primos grandes. Un procesador cuántico tolerante a fallos con $\sim 4000$ qubits lógicos podría factorizar RSA-2048 en horas.
- **ECDSA / ECDH (Curvas Elípticas):** su seguridad depende del problema del logaritmo discreto en grupos de curvas elípticas. El algoritmo de Shor también lo resuelve eficientemente.
- **Diffie-Hellman:** mismo tipo de vulnerabilidad.

Los sistemas de clave simétrica (AES, SHA-3) son mucho menos vulnerables: el algoritmo de Grover solo proporciona una aceleración cuadrática, que se contrarresta duplicando la longitud de clave (AES-128 → AES-256).

## 2. El escenario "Harvest Now, Decrypt Later"

El riesgo no es futuro: ya existe hoy. Actores adversariales pueden:

1. Interceptar y almacenar tráfico cifrado hoy (e-mails, transacciones bancarias, comunicaciones gubernamentales).
2. Esperar a que existan computadoras cuánticas con corrección de errores.
3. Descifrar retroactivamente la información almacenada.

Para información con clasificación de largo plazo (datos médicos, secretos de estado, propiedad intelectual industrial), la ventana de exposición puede superar la vida útil prevista de las computadoras cuánticas: **la migración a PQC es una urgencia de seguridad nacional actual**, no futura.

## 3. La matemática de la resistencia cuántica

La criptografía post-cuántica usa problemas matemáticos para los que no se conocen algoritmos cuánticos eficientes.

### 3.1 Criptografía basada en retículos (Lattice-based)

Un **retículo** es un conjunto discreto de puntos en $\mathbb{R}^n$ con estructura periódica:

$$
\mathcal{L}(B) = \left\{\sum_{i=1}^n z_i \mathbf{b}_i : z_i \in \mathbb{Z}\right\}
$$

donde $B = (\mathbf{b}_1, \ldots, \mathbf{b}_n)$ es la base del retículo.

Los problemas difíciles clave:
- **SVP (Shortest Vector Problem):** encontrar el vector no nulo más corto de $\mathcal{L}$.
- **CVP (Closest Vector Problem):** dado un punto $\mathbf{t} \notin \mathcal{L}$, encontrar el punto de $\mathcal{L}$ más cercano.
- **LWE (Learning With Errors):** dado $(A, \mathbf{b} = A\mathbf{s} + \mathbf{e})$ con $A$ aleatoria y $\mathbf{e}$ ruido pequeño, encontrar $\mathbf{s}$.

El problema LWE tiene una reducción criptográfica desde SVP: si LWE es fácil, SVP también lo es. Y SVP no tiene algoritmo cuántico polinomial conocido (el mejor algoritmo cuántico es sub-exponencial pero no polinomial: coste $2^{O(\sqrt{n})}$).

### 3.2 Criptografía basada en códigos (Code-based)

Se basa en el problema de decodificación aleatoria de códigos lineales (equivalente a CVP para ciertos retículos). La propuesta original de McEliece (1978) nunca fue rota, pero tenía claves muy grandes. Las variantes modernas (como BIKE y HQC) tienen claves más compactas.

### 3.3 Criptografía basada en funciones hash (Hash-based)

Las firmas hash (XMSS, SPHINCS+) se basan únicamente en la resistencia de las funciones hash criptográficas (SHA-3, BLAKE3). Son las más conservadoras: la seguridad post-cuántica de SHA-3-256 se reduce a 128 bits por el algoritmo de Grover, que es manejable.

La desventaja es el tamaño grande de las firmas (varios kilobytes).

## 4. Estándares del NIST (2024)

Tras un proceso de evaluación de 7 años, el NIST finalizó en 2024 los estándares de criptografía post-cuántica (FIPS 203, 204, 205):

| Estándar | Algoritmo | Tipo | Uso | Seguridad base |
|---|---|---|---|---|
| **FIPS 203** | ML-KEM (CRYSTALS-Kyber) | Retículo (Module-LWE) | KEM (cifrado de clave) | 128/192/256 bits |
| **FIPS 204** | ML-DSA (CRYSTALS-Dilithium) | Retículo (Module-LWE) | Firma digital | 128/192/256 bits |
| **FIPS 205** | SLH-DSA (SPHINCS+) | Hash-based | Firma digital | 128/192/256 bits |

Además, FALCON (otra firma basada en retículos de NTRU) está en proceso de estandarización como FIPS 206 para firmas compactas.

### 4.1 ML-KEM (Kyber): intercambio de clave

Kyber es un mecanismo de encapsulación de clave (KEM). Su seguridad se basa en la dureza del problema Module-LWE. El protocolo funciona así:

1. **Generación de clave:** Alice genera $(pk, sk)$ (clave pública y privada).
2. **Encapsulación:** Bob usa $pk$ para encapsular una clave simétrica aleatoria $K$ en un ciphertext $c$.
3. **Desencapsulación:** Alice usa $sk$ para extraer $K$ de $c$.

El resultado es que Alice y Bob comparten $K$ sin haberla transmitido directamente (similar a Diffie-Hellman, pero resistente a Shor).

Kyber-768 (nivel de seguridad 3): clave pública de 1184 bytes, ciphertext de 1088 bytes, clave compartida de 32 bytes.

### 4.2 ML-DSA (Dilithium): firmas digitales

Dilithium usa el paradigma "Fiat-Shamir con abortos" basado en Module-LWE. Ofrece firmas de ~2420-4595 bytes (Dilithium2-5), más grandes que ECDSA (~64 bytes) pero eficientes de verificar.

## 5. Criptografía cuántica vs. post-cuántica

Hay que distinguir claramente dos enfoques:

| | Criptografía Cuántica (QKD) | Criptografía Post-Cuántica (PQC) |
|---|---|---|
| **Base** | Leyes de la física (mecánica cuántica) | Matemáticas (problemas difíciles) |
| **Hardware** | Canales cuánticos, fotones, hardware especial | Software, hardware clásico estándar |
| **Seguridad** | Incondicionalmente seguro (info-teórico) | Computacionalmente seguro |
| **Distancia** | Limitada (~100 km por tramo sin repetidores) | Ilimitada (internet clásica) |
| **Coste** | Muy alto, infraestructura especializada | Bajo (actualización de software) |
| **Adopción** | Nicho (bancos, gobiernos, redes privadas) | Masiva (ya en TLS 1.3, navegadores) |

La recomendación pragmática del NIST y agencias de seguridad: migrar a PQC para la mayoría de aplicaciones; considerar QKD solo para aplicaciones de máxima seguridad con infraestructura dedicada.

## 6. Estado de adopción (2024-2026)

- **TLS 1.3:** Google Chrome y Cloudflare activaron X25519Kyber768 (híbrido ECDH + Kyber) desde 2023.
- **Signal Protocol:** Signal actualiza su protocolo con CRYSTALS-Kyber.
- **OpenSSH:** soporte experimental para ML-KEM.
- **iOS/macOS Apple:** iMessage usa PQ3 (protocolo post-cuántico propio) desde 2024.
- **Certificados X.509:** en proceso de estandarización en IETF.

El modelo de migración recomendado es **híbrido**: combinar algoritmos clásicos (ECDH) con PQC (Kyber) durante el período de transición, para mantener la seguridad si alguno de los dos falla.

## 7. Implicaciones para el desarrollo de software

```python
# Ejemplo conceptual: uso de CRYSTALS-Kyber con la biblioteca pqcrypto
# (biblioteca Python experimental, no para producción)

# from pqcrypto.kem.kyber768 import generate_keypair, encrypt, decrypt
# 
# # Alice genera su par de claves
# public_key, secret_key = generate_keypair()
# 
# # Bob encapsula una clave simétrica
# ciphertext, shared_key_bob = encrypt(public_key)
# 
# # Alice desencapsula
# shared_key_alice = decrypt(secret_key, ciphertext)
# 
# assert shared_key_alice == shared_key_bob  # True
# print(f"Clave compartida: {shared_key_alice.hex()[:32]}...")
# print(f"Tamaño clave pública: {len(public_key)} bytes")
# print(f"Tamaño ciphertext: {len(ciphertext)} bytes")

# En Python, la biblioteca de referencia es `oqs` (Open Quantum Safe):
# pip install oqs
import hashlib

def simulate_kyber_kem():
    """Simulación conceptual del protocolo KEM de Kyber."""
    # En producción usar: from oqs import KeyEncapsulation
    # kem = KeyEncapsulation('Kyber768')
    # public_key = kem.generate_keypair()
    # ciphertext, shared_key = kem.encap_secret(public_key)
    # recovered_key = kem.decap_secret(ciphertext)

    # Simulación con HKDF para ilustrar el protocolo:
    alice_secret = b"alice_secret_seed_kyber"
    shared_material = hashlib.sha3_256(alice_secret).digest()
    print(f"Clave compartida simulada: {shared_material.hex()[:32]}...")
    print(f"Longitud: {len(shared_material)} bytes = {len(shared_material)*8} bits")

simulate_kyber_kem()
```

## 8. Ideas clave

- El algoritmo de Shor amenaza RSA, ECDSA y Diffie-Hellman; el escenario "harvest now, decrypt later" hace urgente la migración hoy.
- La criptografía post-cuántica usa problemas matemáticos (LWE, SVP, decodificación de códigos) para los que no hay algoritmos cuánticos polinomiales.
- El NIST estandarizó en 2024 ML-KEM (Kyber) para intercambio de clave y ML-DSA (Dilithium) + SLH-DSA (SPHINCS+) para firmas digitales.
- La migración recomendada es híbrida: combinar algoritmos clásicos con PQC durante el período de transición.
- QKD (criptografía cuántica) ofrece seguridad incondicional pero requiere hardware especializado y distancias limitadas; PQC es software ejecutable en hardware clásico estándar.

## 9. Ejercicios sugeridos

1. Explicar por qué AES-256 es considerado seguro frente a ataques cuánticos pero AES-128 ya no.
2. Comparar el tamaño de claves y firmas de RSA-2048, ECDSA-256, Dilithium3 y SPHINCS+-128.
3. Describir el ataque "harvest now, decrypt later" y calcular para qué datos actuales el riesgo es real dado un horizonte de 10-15 años para computadoras cuánticas tolerantes a fallos.
4. Investigar qué navegadores web ya soportan algoritmos post-cuánticos en TLS y qué nivel de seguridad ofrecen.

## Navegación

- Anterior: [Programación de pulsos con Qiskit Pulse](../24_control_de_pulsos_y_qiskit_pulse/02_programacion_de_pulsos_con_qiskit_pulse.md)
- Siguiente: [El lenguaje de las arañas: introducción al ZX-Calculus](../26_calculo_grafico_y_zx_calculus/01_el_lenguaje_de_las_aranas.md)
