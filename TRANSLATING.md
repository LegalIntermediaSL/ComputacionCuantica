# Translation Guide — ComputacionCuantica

This guide explains how to contribute translations of the course materials.

## Current status

| Language | Status | Modules translated | Contributor |
|----------|--------|-------------------|-------------|
| Spanish (ES) | ✅ Complete | 01–40 | @LegalIntermediaSL |
| English (EN) | 🚧 In progress | 01–05 | — |
| Portuguese (PT) | 📋 Planned | — | — |
| French (FR) | 📋 Planned | — | — |

## How to contribute a translation

### 1. Pick a module

Check the table above and the [open issues](https://github.com/LegalIntermediaSL/ComputacionCuantica/issues?q=label%3Atranslation) to avoid duplicate work.

Comment on the relevant issue (or open a new one) to claim the module.

### 2. File structure

Translations go in a language-specific folder:

```
Tutorial/
  en/
    01_fundamentos/
      README.md   ← English translation of Tutorial/01_fundamentos/README.md
  pt/
    ...
Ejercicios/
  en/
    ejercicios_basicos.md
```

### 3. Translation guidelines

- **Keep LaTeX math identical** — do not translate mathematical expressions
- **Keep code blocks unchanged** — Python/Qiskit code does not need translation
- **Translate comments** inside code blocks (lines starting with `#`)
- **Use the same heading structure** — same `##` / `###` hierarchy
- **Terminology:** use established quantum computing terms; for disputed translations, add a footnote:
  > *qubit: also "cúbit" (Spanish) — we use "qubit" throughout for international consistency*

### 4. Modules available for translation (priority order)

#### English translation — Módulo 01 (Qubits y estados)

Source: [`Tutorial/01_fundamentos/README.md`](Tutorial/01_fundamentos/README.md)

Key terms to standardize:

| Spanish | English |
|---------|---------|
| estado fundamental | ground state |
| cúbit / qubit | qubit |
| superposición | superposition |
| entrelazamiento | entanglement |
| puerta | gate |
| circuito | circuit |
| medición | measurement |
| esfera de Bloch | Bloch sphere |
| operador unitario | unitary operator |
| base computacional | computational basis |
| estado mixto | mixed state |
| traza parcial | partial trace |

#### Módulo 02 — Qiskit básico

Source: [`Tutorial/02_qiskit_basico/README.md`](Tutorial/02_qiskit_basico/README.md)

*Code examples are already in English (Qiskit API). Only prose sections need translation.*

#### Módulo 03 — Entrelazamiento

Source: [`Tutorial/03_entrelazamiento/README.md`](Tutorial/03_entrelazamiento/README.md)

#### Módulo 04 — Qiskit Runtime

Source: [`Tutorial/04_qiskit/README.md`](Tutorial/04_qiskit/README.md)

#### Módulo 05 — Algoritmos clásicos

Source: [`Tutorial/05_algoritmos/README.md`](Tutorial/05_algoritmos/README.md)

### 5. Submit your translation

1. Fork the repository
2. Create a branch: `translation/en-modulo-01`
3. Add translated files under `Tutorial/en/` (or the appropriate language)
4. Open a Pull Request using the template: title `[TRANSLATION EN] Módulo 01`
5. In the PR description, note any terminology decisions you made

### 6. Review process

Translations are reviewed for:
- Mathematical accuracy (LaTeX unchanged)
- Technical terminology consistency
- Clarity and readability in target language

---

*Thank you for helping make quantum computing education accessible to more people!*
