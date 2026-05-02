# Módulo 48 — Procesamiento Cuántico del Lenguaje Natural (QNLP)

El **Quantum Natural Language Processing** (QNLP) es uno de los campos más originales de la computación cuántica aplicada: combina lingüística matemática, teoría de categorías y circuitos cuánticos parametrizados para representar y clasificar significado. A diferencia del NLP clásico, donde los modelos son redes neuronales masivas que aprenden correlaciones estadísticas, QNLP propone una correspondencia estructural profunda entre la gramática de las frases y la estructura de los circuitos cuánticos.

La idea central proviene del trabajo de Coecke, Sadrzadeh y Clark (2010): los diagramas de cuerda que usamos para razonar sobre categorías monoidas compactas son los mismos que describen la semántica composicional del lenguaje. Eso no es una analogía superficial — es un isomorfismo matemático que permite traducir frases en circuitos cuánticos sin pérdida de estructura.

---

## Índice

1. [Lingüística categorial y pregrupos de Lambek](#1-pregrupos)
2. [DisCoCat — semántica distribucional composicional](#2-discocat)
3. [Circuitos cuánticos como diagramas de cuerda](#3-circuitos)
4. [lambeq — pipeline completo](#4-lambeq)
5. [Entrenamiento híbrido clásico-cuántico](#5-entrenamiento)
6. [Estado del arte 2025](#6-estado-arte)
7. [Ejercicios](#7-ejercicios)
8. [Referencias](#8-referencias)

---

## 1. Lingüística Categorial y Pregrupos de Lambek {#1-pregrupos}

### 1.1 Gramáticas de tipos

Joachim Lambek desarrolló en los años 50 y posteriormente en los 90 un sistema formal para asignar **tipos gramaticales** a las palabras, de modo que una frase es gramaticalmente correcta si y solo si su secuencia de tipos se reduce a un único tipo atómico $s$ (sentence, frase).

Los dos tipos básicos son:
- $n$ — nombre (sustantivo, sintagma nominal)
- $s$ — frase completa gramatical

A partir de ellos se construyen tipos compuestos con dos operaciones de división:
- $n \cdot r^{-1}$ (o $n/r$): necesita un $r$ a la derecha para reducirse a $n$
- $l^{-1} \cdot n$ (o $r\backslash n$): necesita un $r$ a la izquierda

En notación de pregrupo, $l$ y $r$ son los **adjoints** izquierdo y derecho de un tipo. Las reducciones que permiten simplificar son:

$$l \cdot l^r \leq 1 \qquad l^l \cdot l \leq 1$$

### 1.2 Ejemplo: frase simple

Consideremos la frase "Alice ama a Bob". Los tipos asignados son:

| Palabra | Tipo pregrupo |
|---------|---------------|
| Alice   | $n$ |
| ama     | $n^r \cdot s \cdot n^l$ |
| (a) Bob | $n$ |

La reducción se produce concatenando:

$$n \cdot (n^r \cdot s \cdot n^l) \cdot n$$

Aplicando $n \cdot n^r \leq 1$ por la izquierda y $n^l \cdot n \leq 1$ por la derecha:

$$1 \cdot s \cdot 1 = s \checkmark$$

La frase es gramaticalmente válida y su tipo final es $s$.

### 1.3 Diagramas de flechas (cup-cap notation)

Las reducciones se visualizan como **diagramas de tazas y tapas** (cups and caps). Cada contracción $n \cdot n^r \leq 1$ se dibuja como una taza que conecta los dos tipos. El diagrama para "Alice ama a Bob" tiene la forma:

```
Alice    ama        Bob
  n   n^r·s·n^l    n
  |    |   |   |   |
   \___|   |   |__/
       |   |
       s   (reducción completa)
```

Este diagrama es precisamente lo que en la teoría de categorías se llama un **morphismo en una categoría monoide compacta**. Y eso es exactamente la estructura de los circuitos cuánticos con estados de Bell.

### 1.4 Frases más complejas

Para frases con adjetivos, adverbios o cláusulas relativas, los tipos se extienden. Un adjetivo tiene tipo $n \cdot n^l$ (modifica un sustantivo a su derecha). Un adverbio de verbo transitivo tiene tipo $(n^r \cdot s \cdot n^l)^r \cdot (n^r \cdot s \cdot n^l)$. La potencia expresiva del pregrupo es equivalente a las gramáticas libres de contexto en cuanto a cobertura del lenguaje natural, pero con una semántica composicional mucho más limpia.

---

## 2. DisCoCat — Semántica Distribucional Composicional {#2-discocat}

### 2.1 El modelo de Coecke-Sadrzadeh-Clark (2010)

El paper "Mathematical Foundations for a Compositional Distributional Model of Meaning" (Coecke, Sadrzadeh, Clark, 2010) introduce el marco DisCoCat (*Distributional Compositional Categorical*). La idea clave:

> La semántica de una frase se obtiene aplicando un **funtor monoide** $F$ desde la categoría gramatical (pregrupos) hacia la categoría semántica (espacios vectoriales con producto tensorial).

El mapeo es:
- Cada tipo básico $n$ se mapea a un espacio vectorial $N$ (espacio de significado de nombres)
- Cada tipo básico $s$ se mapea a $S$ (espacio de significado de frases)
- Cada palabra mapea a un tensor en el espacio producto correspondiente a su tipo
- Las reducciones gramaticales (cups) mapean a contracciones tensoriales

Para el verbo transitivo "ama" con tipo $n^r \cdot s \cdot n^l$, su significado es un tensor:

$$\overrightarrow{\text{ama}} \in N \otimes S \otimes N$$

El significado de la frase completa se calcula como contracción tensorial:

$$\overrightarrow{\text{frase}} = \overrightarrow{\text{Alice}} \otimes \overrightarrow{\text{ama}} \otimes \overrightarrow{\text{Bob}}$$

con contracciones según las cups del diagrama gramatical.

### 2.2 Diagramas de cuerda (string diagrams)

Los **string diagrams** son una notación gráfica bidimensional para morfismos en categorías monoide. En DisCoCat:

- Los cables verticales representan tipos/espacios vectoriales
- Las cajas representan palabras (morfismos)
- Las cups representan contracciones tensoriales (reducciones gramaticales)

```
  Alice    ama       Bob
  ┌───┐  ┌─────┐   ┌───┐
  │ f │  │  g  │   │ h │
  └───┘  └──┬──┘   └───┘
    │    ╭──╯──╮     │
    ╰────╯  S  ╰─────╯
            │
          frase
```

La belleza matemática es que esta notación es **isomorfa** a la de los circuitos cuánticos: los cables son qubits, las cajas son puertas, y los estados de Bell (pares entrelazados EPR) hacen el papel de las cups.

### 2.3 Espacios vectoriales de significado

En la práctica, los vectores de significado para las palabras se obtienen de corpus de texto mediante métodos distribucionales (co-ocurrencia, word2vec, etc.). Los nombres viven en $\mathbb{R}^n$ o $\mathbb{C}^n$, y los verbos transitivos en $\mathbb{R}^{n \times m \times n}$.

DisCoCat garantiza que la composición semántica respeta la estructura gramatical: el significado del todo es función del significado de las partes más la estructura sintáctica. Esto contrasta con los transformers, donde la estructura gramatical está implícita pero no garantizada.

---

## 3. Circuitos Cuánticos como Diagramas de Cuerda {#3-circuitos}

### 3.1 El isomorfismo cuántico

La categoría de circuitos cuánticos (con estados y medidas) es una categoría monoide compacta. Las cups corresponden a estados de Bell $|\Phi^+\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$. Esto significa que cualquier diagrama DisCoCat se puede implementar directamente como circuito cuántico.

El mapeo explícito es:
- Tipo $n$ (dimensión $d_n$) → $\log_2 d_n$ qubits
- Tipo $s$ (dimensión $d_s$) → $\log_2 d_s$ qubits
- Palabra con tipo $n^r \cdot s \cdot n^l$ → operación cuántica en $2\log_2 d_n + \log_2 d_s$ qubits

### 3.2 Circuitos IQP (Instantaneous Quantum Polynomial)

La arquitectura elegida para QNLP en lambeq son los **circuitos IQP** (*Instantaneous Quantum Polynomial-time*). Su estructura es:

```
|0⟩ ─── H ── Rz(θ₁) ── [entanglement] ── Rz(θ₂) ── H ── M
|0⟩ ─── H ── Rz(φ₁) ── [entanglement] ── Rz(φ₂) ── H ── M
...
```

Cada qubit comienza en $|0\rangle$, recibe una puerta Hadamard, luego rotaciones $R_z(\theta)$ con parámetros entrenables, capa de entrelazamiento (CX gates), más rotaciones, y finalmente Hadamard seguido de medida.

### 3.3 Mapeo pregrupo → qubit

Para una frase de longitud $L$ palabras con tipos pregrupo asignados, el número total de qubits es:

$$n_{\text{qubits}} = n_s + \sum_{w=1}^{L} n_w$$

donde $n_s = \log_2 d_s$ (qubits para el tipo frase) y $n_w$ depende del tipo de cada palabra. En la implementación estándar con $d_n = 2$ (1 qubit por nombre) y $d_s = 2$ (1 qubit para frase):

- Nombre (tipo $n$): 1 qubit
- Verbo intransitivo (tipo $n^r \cdot s$): 2 qubits
- Verbo transitivo (tipo $n^r \cdot s \cdot n^l$): 3 qubits

Para "Alice ama a Bob" ($n + n^r s n^l + n$): $1 + 3 + 1 = 5$ qubits antes de contracciones → 1 qubit de salida.

### 3.4 Parámetros entrenables

El número de parámetros es proporcional a la longitud de la frase. Para un circuito IQP con $p$ capas de rotación por qubit:

$$n_{\text{params}} = p \cdot n_{\text{qubits}}$$

Frases cortas (~5 palabras) tienen ~10–20 parámetros. Frases largas (~20 palabras) tienen ~40–80 parámetros. Esto es mínimo comparado con redes neuronales clásicas, pero es viable en hardware cuántico actual.

---

## 4. lambeq — Pipeline Completo {#4-lambeq}

### 4.1 Instalación y componentes

```bash
pip install lambeq
```

lambeq (Meichanetzidis et al., 2021) es la librería de Quantinuum para QNLP. Su pipeline completo:

```
Texto → BobcatParser → Diagrama DisCoCat → Reescritura → Circuito IQP → Entrenamiento
```

### 4.2 Parsing con BobcatParser

```python
from lambeq import BobcatParser

parser = BobcatParser(verbose='text')

# Parsear una frase
sentence = "Alice loves Bob"
diagram = parser.sentence2diagram(sentence)
diagram.draw()
```

BobcatParser es un parser neuronal entrenado en Penn Treebank que devuelve árboles de constituyentes convertidos automáticamente a diagramas de pregrupo. Funciona en inglés con alta precisión (~95% en oraciones estándar).

### 4.3 Conversión a circuito cuántico

```python
from lambeq import IQPAnsatz, AtomicType

# Definir dimensiones de los tipos atómicos
N = AtomicType.NOUN       # 1 qubit
S = AtomicType.SENTENCE   # 1 qubit

ansatz = IQPAnsatz({N: 1, S: 1}, n_layers=1, n_single_qubit_params=3)

# Convertir diagrama a circuito
circuit = ansatz(diagram)
circuit.draw()
```

### 4.4 Dataset de clasificación food/IT

El dataset estándar de demostración de QNLP clasifica frases en dos categorías:
- **food** (comida): "Alice likes pasta", "Bob eats sushi"
- **IT** (tecnología): "Alice programs computers", "Bob codes software"

```python
from lambeq import Dataset

# Frases de ejemplo
train_sentences = [
    "Alice likes pasta",        # food
    "Bob eats sushi",           # food
    "Alice programs computers", # IT
    "Bob codes software",       # IT
    "Mary enjoys pizza",        # food
    "John writes code",         # IT
]
train_labels = [[1, 0], [1, 0], [0, 1], [0, 1], [1, 0], [0, 1]]

# Parsear todas las frases
diagrams = parser.sentences2diagrams(train_sentences)
circuits = [ansatz(d) for d in diagrams]
```

### 4.5 NumpyModel y SPSAOptimizer

Para entrenamiento en simulación clásica (sin hardware cuántico):

```python
from lambeq import NumpyModel, SPSAOptimizer, BinaryCrossEntropyLoss
import numpy as np

# Modelo basado en simulación NumPy
model = NumpyModel.from_diagrams(circuits)
model.initialise_weights()

# Función de pérdida
loss = BinaryCrossEntropyLoss()

# Optimizador SPSA (Simultaneous Perturbation Stochastic Approximation)
optimizer = SPSAOptimizer(
    model=model,
    loss_fn=loss,
    hyperparams={'a': 0.05, 'c': 0.06, 'A': 0.001 * 100},
    evaluate_functions={'acc': lambda y_hat, y: np.mean(
        np.round(y_hat) == y
    )}
)

# Entrenamiento
EPOCHS = 100
for epoch in range(EPOCHS):
    optimizer.backward(zip(circuits, train_labels))
    if epoch % 10 == 0:
        train_loss = optimizer.loss
        print(f"Epoch {epoch}: loss = {train_loss:.4f}")
```

---

## 5. Entrenamiento Híbrido Clásico-Cuántico {#5-entrenamiento}

### 5.1 SPSA Optimizer

El optimizador **SPSA** (Simultaneous Perturbation Stochastic Approximation, Spall 1992) es especialmente adecuado para circuitos cuánticos porque no requiere gradientes exactos. En lugar de evaluar $\partial L / \partial \theta_i$ para cada parámetro, SPSA estima el gradiente perturbando todos los parámetros simultáneamente:

$$\hat{g}_k(\theta) = \frac{L(\theta_k + c_k \Delta_k) - L(\theta_k - c_k \Delta_k)}{2 c_k} \Delta_k^{-1}$$

donde $\Delta_k$ es un vector de perturbaciones aleatorias $\pm 1$ (Bernoulli). Esto requiere solo **2 evaluaciones del circuito** por paso, independientemente del número de parámetros.

La actualización de parámetros es:

$$\theta_{k+1} = \theta_k - a_k \hat{g}_k(\theta_k)$$

con schedules $a_k = a/(A+k+1)^\alpha$ y $c_k = c/k^\gamma$. Los valores estándar son $\alpha=0.602$, $\gamma=0.101$.

### 5.2 Función de coste cross-entropy binaria

Para clasificación binaria (food vs IT), la función de pérdida es:

$$\mathcal{L} = -\frac{1}{N}\sum_{i=1}^{N}\left[y_i \log \hat{y}_i + (1-y_i)\log(1-\hat{y}_i)\right]$$

donde $\hat{y}_i$ es la probabilidad de medir $|1\rangle$ en el qubit de salida del circuito para la frase $i$.

### 5.3 Backprop a través del circuito cuántico

Cuando se usa un backend diferenciable (como PennyLane o PyTorch con lambeq), los gradientes se calculan mediante la regla del cambio de parámetro:

$$\frac{\partial \langle O \rangle}{\partial \theta} = \frac{1}{2}\left[\langle O \rangle_{\theta + \pi/2} - \langle O \rangle_{\theta - \pi/2}\right]$$

Esta regla es exacta para puertas de rotación $R(\theta) = e^{-i\theta P/2}$ con $P^2 = I$.

### 5.4 Resultados típicos

En el dataset food/IT con ~100 frases de entrenamiento y 30 de test:

| Modelo | Accuracy test | Parámetros |
|--------|---------------|------------|
| NumpyModel (simulación) | ~90–95% | ~50–100 |
| QPU real (H1-1 Quantinuum) | ~85–92% | ~50–100 |
| Modelo clásico baseline (log. reg.) | ~88% | ~100+ |

El hecho de que QNLP alcance resultados comparables al baseline clásico con datasets pequeños es prometedor, aunque la ventaja cuántica genuina aún no está demostrada en datasets grandes.

### 5.5 Uso con PennyLane (backend diferenciable)

```python
from lambeq import PennyLaneModel

# Usar backend PennyLane con diferenciación automática
model = PennyLaneModel.from_diagrams(circuits, probabilities=True)
model.initialise_weights()

import torch
optimizer_torch = torch.optim.Adam(model.parameters(), lr=0.01)

for epoch in range(100):
    optimizer_torch.zero_grad()
    preds = model(circuits)
    labels_tensor = torch.tensor(train_labels, dtype=torch.float32)
    loss_val = torch.nn.functional.binary_cross_entropy(preds, labels_tensor)
    loss_val.backward()
    optimizer_torch.step()
```

---

## 6. Estado del Arte 2025 {#6-estado-arte}

### 6.1 Quantinuum QNLP en hardware H2

Quantinuum (antes Honeywell Quantum Solutions) ha ejecutado experimentos QNLP reales en su procesador **H2** (56 qubits atrapados en ion, fidelidad de puerta de 2 qubits >99.9%). Los resultados más recientes (2024–2025) muestran:

- Clasificación de frases con hasta 12 qubits en hardware real
- Fidelidades suficientes para detectar señal por encima del ruido en clasificación binaria
- Primer experimento de QNLP fault-tolerant en progreso con H2-1

El trabajo de Lorenz et al. (2023) demostró clasificación de sentimientos en hardware cuántico con 103 circuitos sobre un dataset de 130 frases, obteniendo 87% de accuracy.

### 6.2 IBM NLP Research

IBM Research ha explorado QNLP desde ángulos diferentes, principalmente mediante **Quantum Kernel Methods** para NLP. En lugar de mapear frases a circuitos paramétricos, computan kernels cuánticos $K(x, x') = |\langle \psi(x) | \psi(x') \rangle|^2$ y los usan en SVMs clásicas. Resultados en 2024 muestran mejoras sobre kernels clásicos en datasets de baja dimensión.

### 6.3 Limitaciones actuales

**El problema principal: frases cortas.** Con los procesadores cuánticos actuales (50–100 qubits, profundidad limitada por decoherencia), solo se pueden procesar frases de ~5–10 palabras. Una frase de 20 palabras requeriría ~40+ qubits con circuitos de profundidad ~20, que excede la capacidad de los sistemas actuales sin corrección de errores.

| Limitación | Impacto |
|------------|---------|
| Pocos qubits (<100) | Frases cortas únicamente |
| Decoherencia | Profundidad de circuito limitada |
| Sin corrección de errores | Ruido degrada la señal |
| Datasets pequeños | No se conoce la escala |
| Parsing solo en inglés | BobcatParser solo funciona en inglés |

### 6.4 ¿Existe ventaja cuántica en QNLP?

Esta es la pregunta del millón. Los argumentos a favor de ventaja cuántica en QNLP son:

1. **Argumento estructural**: Los diagramas de cuerda de DisCoCat y los circuitos cuánticos son isomorfos; el hardware cuántico implementa la semántica composicional de forma natural.

2. **Argumento de dimensionalidad**: El espacio de Hilbert de $n$ qubits tiene dimensión $2^n$, permitiendo representar vectores semánticos exponencialmente más ricos que en NLP clásico con los mismos recursos físicos.

3. **Argumento de entrelazamiento**: Las correlaciones semánticas entre palabras distantes en una frase podrían capturarse eficientemente con entrelazamiento cuántico.

Sin embargo, los contraargumentos son fuertes: los transformers clásicos actuales (GPT-4, Llama 3) tienen miles de millones de parámetros y procesan textos arbitrariamente largos. La ventaja cuántica en NLP, si existe, probablemente no aparecerá hasta la era de computación cuántica tolerante a fallos con millones de qubits lógicos.

El consenso en 2025 es que QNLP es un campo científicamente riguroso e importante para entender qué puede hacer la computación cuántica, pero que la ventaja práctica sobre LLMs clásicos está al menos a una o dos décadas de distancia.

---

## 7. Ejercicios {#7-ejercicios}

### Ejercicio 1: Clasificación binaria simple con lambeq

Implementa un clasificador QNLP para el dataset food/IT usando lambeq con las siguientes especificaciones:
- 60 frases de entrenamiento, 20 de test
- IQPAnsatz con 1 capa, 1 qubit por nombre, 1 qubit por frase
- NumpyModel con SPSAOptimizer, 200 épocas
- Reporta accuracy train y test cada 20 épocas

```python
# Punto de partida
from lambeq import BobcatParser, IQPAnsatz, AtomicType, NumpyModel
from lambeq import SPSAOptimizer, BinaryCrossEntropyLoss

# Tu código aquí...
# 1. Parsear frases con BobcatParser
# 2. Crear circuitos con IQPAnsatz
# 3. Entrenar y evaluar
```

**Pregunta de análisis**: ¿Cuántos qubits usa el circuito más grande de tu dataset? ¿Y el más pequeño?

### Ejercicio 2: Diagrama de frase compleja

Construye manualmente el diagrama DisCoCat (tipos pregrupo y cups) para la frase:

> "The big cat that Alice feeds likes fish"

1. Asigna tipos pregrupo a cada palabra (usa: $n$, $s$, $n^r$, $n^l$, $n \cdot n^l$ para adjetivos, $(n^r \cdot s \cdot n^l)^r \cdot n^r \cdot s \cdot n^l$ para cláusula relativa)
2. Dibuja el diagrama de cups
3. Verifica que se reduce a tipo $s$
4. Calcula el número de qubits que requeriría este circuito con $d_n = 2$, $d_s = 2$

### Ejercicio 3: Comparativa clásico-cuántico

Implementa dos clasificadores para el dataset food/IT y compáralos:

**Clasificador A (clásico)**: Regresión logística con vectores TF-IDF de las frases.

**Clasificador B (cuántico)**: Modelo lambeq NumpyModel.

Compara:
- Accuracy en test con 20, 50 y 100 frases de entrenamiento
- Tiempo de entrenamiento
- Número de parámetros
- Curva de aprendizaje (accuracy vs número de ejemplos)

**Hipótesis a contrastar**: ¿El modelo cuántico necesita menos datos para alcanzar el mismo rendimiento? ¿Por qué o por qué no?

### Ejercicio 4: Clasificación con error gramatical

Investiga qué ocurre cuando una frase tiene un error gramatical que impide el parsing correcto:

1. Intenta parsear "Alice love Bob" (error de concordancia sujeto-verbo) con BobcatParser
2. Intenta parsear "the eat cat fish" (orden incorrecto)
3. ¿Qué devuelve el parser? ¿Genera algún diagrama? ¿Es válido?
4. Propón una estrategia robusta para manejar frases mal formadas en un pipeline QNLP de producción (considera: preprocesado, corrección automática, fallback a modelos clásicos)

---

## 8. Referencias {#8-referencias}

1. **Coecke, B., Sadrzadeh, M., Clark, S.** (2010). *Mathematical Foundations for a Compositional Distributional Model of Meaning*. Linguistic Analysis, 36(1-4):345-384. — Fundamento teórico de DisCoCat.

2. **Meichanetzidis, K., et al.** (2020). *Quantum Natural Language Processing on Near-Term Quantum Computers*. arXiv:2005.04147. — Paper fundacional de lambeq y circuitos IQP para QNLP.

3. **Lorenz, R., et al.** (2021). *QNLP in Practice: Running Compositional Models of Meaning on a Quantum Computer*. Journal of Artificial Intelligence Research, 76:1305-1342. — Primera implementación en hardware cuántico real.

4. **Clark, S.** (2021). *Something Old, Something New: Grammar-based CCG Parsing with Transformer Models*. arXiv:2109.10044. — BobcatParser, el parser neuronal de lambeq.

5. **Lambek, J.** (1999). *Type Grammar Revisited*. Logical Aspects of Computational Linguistics. Springer. — Pregrupos de Lambek.

6. **Spall, J.C.** (1992). *Multivariate Stochastic Approximation Using a Simultaneous Perturbation Gradient Approximation*. IEEE Transactions on Automatic Control, 37(3):332-341. — SPSA Optimizer.

7. **Coecke, B., et al.** (2023). *Grammar-Aware Question-Answering on Quantum Computers*. arXiv:2303.15778. — Estado del arte reciente de Quantinuum.

8. **lambeq Documentation** (2024). https://cqcl.github.io/lambeq/ — Documentación oficial con tutoriales y API reference.

---

*Módulo 48 | ComputacionCuantica | Nivel: Avanzado | Prerrequisitos: Módulos 11 (VQE/QAOA), 35 (computación adiabática), conocimientos básicos de lingüística*
