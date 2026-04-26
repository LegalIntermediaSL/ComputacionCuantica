# Migración a PQC: Estrategia y Timeline

**Módulo 36 · Artículo 2 · Nivel muy avanzado**

---

## La amenaza "Harvest Now, Decrypt Later"

Los adversarios sofisticados (estados-nación) ya están **recopilando tráfico
cifrado hoy** para descifrarlo cuando lleguen los ordenadores cuánticos
fault-tolerant. Esta amenaza es real e inmediata:

```
2025                    2030                    2035
 │                        │                        │
 ├── Recopilación ────────┼────────────────────────┤
 │   de tráfico TLS       │                        │
 │   (HARVEST NOW)        │                        │
 │                        ├── Primeros QC FT ───────┤
 │                        │   RSA-2048 vulnerable  │
 │                        │                        │
 ├── Migración PQC ───────┼────────────────────────┤
 │   DEBE COMPLETARSE     │   (DECRYPT LATER)       │
 │   ANTES DE 2030        │                        │
```

**Datos cifrados con RSA/ECDH hoy tienen vida útil efectiva hasta ~2030.**
Si el dato debe permanecer secreto más de 5-10 años, **la migración es urgente**.

```python
import numpy as np

def horizonte_riesgo(años_secreto: int, año_actual: int = 2025,
                      año_qc_estimado: int = 2030) -> dict:
    """
    Calcula el riesgo de "harvest-now-decrypt-later" para datos cifrados hoy.
    
    años_secreto: cuántos años debe permanecer secreto el dato
    año_qc_estimado: cuando se estima que QC pueda romper RSA-2048
    """
    año_expiracion = año_actual + años_secreto
    ventana_peligro = max(0, año_expiracion - año_qc_estimado)

    if año_expiracion <= año_qc_estimado:
        nivel = 'BAJO'
        accion = 'Migración conveniente pero no urgente'
    elif años_secreto < 3:
        nivel = 'BAJO'
        accion = 'Dato expira antes de que QC sea prácticamente disponible'
    elif ventana_peligro < 2:
        nivel = 'MEDIO'
        accion = 'Planificar migración a PQC en el próximo ciclo de actualización'
    else:
        nivel = 'ALTO ⚠️'
        accion = 'MIGRAR A PQC INMEDIATAMENTE — datos en riesgo'

    return {
        'años_secreto': años_secreto,
        'año_expiracion': año_expiracion,
        'ventana_peligro_años': ventana_peligro,
        'nivel_riesgo': nivel,
        'accion_recomendada': accion,
    }

print('Análisis de riesgo HNDL para datos cifrados en 2025:')
print(f'{"Años secreto":>13} | {"Expira":>7} | {"Peligro":>9} | {"Nivel":>8} | Acción')
print('-' * 80)
for años in [1, 2, 5, 7, 10, 15, 20]:
    r = horizonte_riesgo(años)
    print(f'{años:>13} | {r["año_expiracion"]:>7} | '
          f'{r["ventana_peligro_años"]:>9.0f} | {r["nivel_riesgo"]:>8} | {r["accion_recomendada"]}')
```

---

## Timeline de estándares NIST PQC

```python
timeline_nist = [
    (2016, 'NIST lanza competición PQC', 'Solicita propuestas de todo el mundo (82 recibidas)'),
    (2017, 'Primera ronda: 69 candidatos', 'Evaluación inicial de seguridad y eficiencia'),
    (2019, 'Segunda ronda: 26 candidatos', 'Análisis profundo, ataques publicados'),
    (2020, 'Tercera ronda: 7 finalistas', 'Kyber, Dilithium, FALCON, SPHINCS+, NTRU, SABER, McEliece'),
    (2022, 'Anuncio de selección', 'Kyber (KEM), Dilithium, FALCON, SPHINCS+ (firmas)'),
    (2023, 'NIST IR 8413: borradores', 'ML-KEM, ML-DSA, SLH-DSA publicados para revisión pública'),
    (2024, 'FIPS 203, 204, 205', 'Estándares definitivos publicados en agosto 2024'),
    (2024, 'FIPS 206 (FALCON)', 'Firma basada en retículas cíclicas; publicada sep. 2024'),
    (2025, 'Adopción por industria', 'TLS 1.3 híbrido PQC+clásico en Chrome, Firefox, OpenSSL'),
    (2030, 'Fase-out RSA/ECDH', 'NIST recomienda eliminar RSA<4096 y ECDH en sistemas federales'),
]

print('Timeline NIST PQC:')
print('-' * 80)
for año, hito, desc in timeline_nist:
    print(f'  {año}: {hito}')
    print(f'        → {desc}')
    print()
```

---

## TLS 1.3 Híbrido: X25519 + Kyber

La estrategia de transición recomendada usa **kems híbridos**: combinación de
un algoritmo clásico (seguro hoy) y un algoritmo PQC (seguro contra QC).

La clave compartida es: $K = H(K_{clásico} \| K_{PQC})$

```python
import hashlib
import os

def kex_hibrido_sim(seed: int = 0) -> dict:
    """
    Simula un intercambio de clave híbrido X25519 + ML-KEM-768.
    Usa valores simulados (no implementación criptográfica real).
    """
    rng = np.random.default_rng(seed)

    # === ECDH X25519 (simulado) ===
    # Alice genera clave privada/pública ECDH
    sk_ecdh_alice = rng.bytes(32)  # 32 bytes clave privada
    pk_ecdh_alice = hashlib.sha256(sk_ecdh_alice + b'pk').digest()

    # Bob genera clave privada/pública ECDH
    sk_ecdh_bob = rng.bytes(32)
    pk_ecdh_bob = hashlib.sha256(sk_ecdh_bob + b'pk').digest()

    # Secreto compartido ECDH (simulado)
    K_ecdh = hashlib.sha256(sk_ecdh_alice + pk_ecdh_bob).digest()

    # === ML-KEM-768 (simulado) ===
    # Alice genera clave de encapsulación (simulado)
    sk_kyber = rng.bytes(2400)  # 2400 bytes sk de Kyber-768
    pk_kyber = hashlib.sha3_256(sk_kyber + b'pk').digest()

    # Bob encapsula (genera ciphertext + secreto)
    K_kyber_bob = rng.bytes(32)
    ct_kyber = hashlib.sha3_256(K_kyber_bob + pk_kyber).digest()  # ciphertext simulado

    # Alice desencapsula
    K_kyber_alice = hashlib.sha3_256(sk_kyber[:32] + ct_kyber).digest()
    # En una implementación real, K_kyber_alice == K_kyber_bob

    # === Clave híbrida combinada ===
    # RFC draft-ietf-tls-hybrid-design-09
    K_hibrido = hashlib.sha3_256(K_ecdh + K_kyber_bob).digest()

    return {
        'pk_ecdh_bytes': 32,
        'pk_kyber_bytes': 1184,  # Kyber-768
        'ct_kyber_bytes': 1088,  # Kyber-768
        'K_hibrido_hex': K_hibrido.hex()[:32] + '...',
        'overhead_vs_solo_ecdh': 1184 + 1088,  # bytes extra
    }

r = kex_hibrido_sim()
print('Intercambio de clave híbrido X25519 + ML-KEM-768:')
print(f'  pk ECDH: {r["pk_ecdh_bytes"]} bytes')
print(f'  pk Kyber-768: {r["pk_kyber_bytes"]} bytes')
print(f'  ct Kyber-768: {r["ct_kyber_bytes"]} bytes')
print(f'  Overhead vs solo ECDH: +{r["overhead_vs_solo_ecdh"]} bytes')
print(f'  Clave híbrida: {r["K_hibrido_hex"]}')
print(f'\n  RFC: draft-ietf-tls-hybrid-design')
print(f'  Adoptado en: Chrome 124+ (X25519Kyber768), Firefox 130+, Cloudflare')
```

---

## Evaluación de impacto por sector

```python
sectores = [
    {
        'sector': 'Banca / Finanzas',
        'riesgo': 'CRÍTICO',
        'datos_sensibles': 'Transacciones, contratos, datos de clientes',
        'horizonte_secreto': '10-30 años',
        'estado_migracion': 'En piloto (2024-2025), obligatoria por reguladores 2027',
        'estandar_referencia': 'CNSA 2.0 (NSA), EBA guidelines',
    },
    {
        'sector': 'Salud',
        'riesgo': 'ALTO',
        'datos_sensibles': 'Historiales médicos, genómica',
        'horizonte_secreto': 'Décadas (HIPAA: 50 años)',
        'estado_migracion': 'Planificación iniciada, poca urgencia percibida',
        'estandar_referencia': 'NIST SP 1800-38',
    },
    {
        'sector': 'Defensa / Gobierno',
        'riesgo': 'CRÍTICO',
        'datos_sensibles': 'Secretos de estado, comunicaciones militares',
        'horizonte_secreto': '25-100 años',
        'estado_migracion': 'Mandatorio desde CNSA 2.0 (NSA 2022)',
        'estandar_referencia': 'CNSA 2.0: ML-KEM, ML-DSA, XMSS (hash)',
    },
    {
        'sector': 'PKI / Certificados',
        'riesgo': 'ALTO',
        'datos_sensibles': 'Claves raíz, certificados de CA',
        'horizonte_secreto': 'Depende de la CA (5-25 años)',
        'estado_migracion': 'IETF drafts activos, CA/Browser Forum 2025',
        'estandar_referencia': 'RFC 9629 (ML-DSA en X.509)',
    },
    {
        'sector': 'IoT / Dispositivos embebidos',
        'riesgo': 'MEDIO',
        'datos_sensibles': 'Telemetría, comandos de control',
        'horizonte_secreto': 'Vida útil del dispositivo (5-20 años)',
        'estado_migracion': 'Gran reto: firmware difícil de actualizar',
        'estandar_referencia': 'NIST IR 8425 (PQC para IoT)',
    },
]

print('Análisis de impacto por sector:')
print('=' * 80)
for s in sectores:
    print(f'\n[{s["sector"]}] — Riesgo: {s["riesgo"]}')
    print(f'  Datos en riesgo: {s["datos_sensibles"]}')
    print(f'  Horizonte de secreto: {s["horizonte_secreto"]}')
    print(f'  Estado de migración: {s["estado_migracion"]}')
    print(f'  Estándar de referencia: {s["estandar_referencia"]}')
```

---

## Checklist de migración PQC

```python
checklist_migracion = {
    'Fase 1: Inventario (Ahora)': [
        '□ Identificar todos los sistemas que usan criptografía de clave pública',
        '□ Catalogar datos con vida útil > 5 años y su nivel de sensibilidad',
        '□ Mapear dependencias: librerías (OpenSSL, BouncyCastle), HSMs, PKI',
        '□ Identificar restricciones de hardware (IoT, embedded, HSMs legacy)',
        '□ Evaluar riesgo HNDL para cada categoría de dato',
    ],
    'Fase 2: Preparación (2025-2026)': [
        '□ Actualizar OpenSSL ≥ 3.x con OQS-Provider (liboqs)',
        '□ Implementar agility criptográfica (cambiar algoritmo sin redeploy)',
        '□ Testar ML-KEM-768 + X25519 híbrido en entornos de staging',
        '□ Formar al equipo de seguridad en criptografía de retículas',
        '□ Actualizar políticas: no nuevos sistemas con RSA<4096 sin plan PQC',
    ],
    'Fase 3: Migración (2026-2028)': [
        '□ Desplegar TLS híbrido (X25519Kyber768) en todos los servicios externos',
        '□ Migrar PKI interna: nuevas CAs con ML-DSA, firmas de código con SLH-DSA',
        '□ Reemitir certificados de larga duración con algoritmos PQC',
        '□ Actualizar HSMs a modelos compatibles con FIPS 203/204',
        '□ Cifrar retroactivamente datos sensibles de larga duración',
    ],
    'Fase 4: Consolidación (2028-2030)': [
        '□ Eliminar RSA y ECDH en todos los sistemas internos',
        '□ Solo PQC en nuevos deployments',
        '□ Auditoría externa de criptografía post-cuántica',
        '□ Plan de respuesta ante rotura de algún algoritmo PQC (agilidad)',
    ],
}

for fase, tareas in checklist_migracion.items():
    print(f'\n{fase}:')
    for t in tareas:
        print(f'  {t}')
```

---

## OpenSSL + OQS: implementación práctica

```python
openssl_oqs_example = """
# Instalación de liboqs y OQS-Provider para OpenSSL 3.x
# (requiere compilar desde fuente o usar paquetes experimentales)

# 1. Instalar dependencias
# apt-get install cmake libssl-dev

# 2. Compilar liboqs
# git clone --depth 1 https://github.com/open-quantum-safe/liboqs
# cmake -DCMAKE_INSTALL_PREFIX=/opt/oqs liboqs
# make -j4 && make install

# 3. Compilar OQS-Provider
# git clone --depth 1 https://github.com/open-quantum-safe/oqs-provider
# cmake -DCMAKE_PREFIX_PATH=/opt/oqs .
# make && sudo make install

# 4. Usar ML-KEM en TLS 1.3
# openssl s_server -groups mlkem768 -cert cert.pem -key key.pem
# openssl s_client -groups mlkem768 -connect localhost:4433

# 5. Python con liboqs-python
# pip install liboqs-python (experimental)

try:
    import oqs
    kem = oqs.KeyEncapsulation('Kyber768')
    pk = kem.generate_keypair()
    ct, K_enc = kem.encap_secret(pk)
    K_dec = kem.decap_secret(ct)
    assert K_enc == K_dec
    print('ML-KEM-768 funcional via liboqs-python')
    print(f'  pk: {len(pk)} bytes, ct: {len(ct)} bytes, K: {len(K_enc)} bytes')
except ImportError:
    print('liboqs-python no instalado.')
    print('Instalar: pip install liboqs-python (requiere liboqs compilado)')
    print()
    print('Alternativas sin compilar:')
    print('  - pyca/cryptography >= 42 (ML-KEM en desarrollo)')
    print('  - pqcrypto (Python puro, más lento)')
"""
print(openssl_oqs_example)
```

---

## El futuro: más allá de los estándares actuales

```python
horizonte_pqc = {
    '2024-2026': [
        'Adopción masiva de ML-KEM + X25519 híbrido en TLS',
        'FIPS 206 (FALCON) para firmas de alta velocidad',
        'Primeros HSMs certificados FIPS 140-3 con PQC',
    ],
    '2027-2030': [
        'Phase-out de RSA/ECDH en sistemas federales USA (CNSA 2.0)',
        'Posible migración a ML-KEM puro (sin híbrido)',
        'Nuevas rondas NIST para firmas PQC adicionales (LESS, MAYO, UOV)',
    ],
    '2030+': [
        'NIST PQC Round 2 para KEMs alternativos (si Kyber se rompe)',
        'XMSS/LMS para firmas de código de larga duración (ya estandarizados)',
        'Integración QKD + PQC en redes de alta seguridad',
        'Evaluación continua ante avances en algoritmos cuánticos',
    ],
}

print('\nHorizonte futuro de PQC:')
for periodo, hitos in horizonte_pqc.items():
    print(f'\n[{periodo}]')
    for h in hitos:
        print(f'  • {h}')

print('\n⚠️  Recordatorio crucial:')
print('La seguridad de PQC es conjetural, no probada matemáticamente.')
print('La única garantía real es la agilidad criptográfica:')
print('diseñar sistemas que puedan cambiar de algoritmo sin rediseño completo.')
```

---

**Referencias:**
- NIST, *FIPS 203: ML-KEM* (agosto 2024) — estándar oficial
- NIST, *FIPS 204: ML-DSA* (agosto 2024) — estándar oficial
- NSA, *CNSA 2.0* (2022) — hoja de ruta para sistemas de defensa
- Bernstein & Lange, *Nature* 549, 188 (2017) — "Post-quantum cryptography"
- Mosca, *npj Quantum Information* 4, 22 (2018) — estimación de riesgo cuántico
- IETF, *draft-ietf-tls-hybrid-design* — TLS híbrido PQC+clásico
