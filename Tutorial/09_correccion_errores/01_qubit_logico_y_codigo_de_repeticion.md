# Qubit Lógico y Código de Repetición

## 1. Por qué hace falta corrección

Los qubits físicos actuales son criaturas extremadamente frágiles, lo cual los somete a errores esporádicos inducidos por fluctuaciones magnéticas o interacciones térmicas. En la computación clásica, los transistores sufren de ruidos minúsculos, pero la termodinámica les permite ignorarlos limpiamente. Un qubit, al albergar amplitudes continuas entre cero y uno, se ve forzado a asimilar cualquier pequeñísimo empuje parasitario (decoherencia térmica, rotaciones de fase), corrompiendo en el acto los algoritmos.

Si queremos computación cuántica escalable (como poder descifrar claves de encriptación complejas RSA), no basta con apilar más qubits de la misma pésima fidelidad: necesitamos agruparlos lógicamente para blindar la información cuántica matemática que albergan frente a errores físicos.

## 2. Qubit físico frente a qubit lógico

- **Qubit físico:** Es la pieza real de hardware de nivel más atómico imaginable en el chip (por ejemplo, una lámina de transmón superconductor o un único átomo atrapado por láser). 
- **Qubit Lógico:** Es un "qubit matemático virtual" perfecto, que habita colectivamente de manera redundante repartida a lo largo de un conjunto entrelazado de qubits físicos. Su objetivo es detectar que "uno de sus soldados físicos ha sufrido una herida" y ser capaz de sanarlo antes de que la herida afecte a la información lógica global.

## 3. El muro fundamental cuántico: El Teorema de No-Clonación

La idea más evidente para hacer respaldos y corregir errores en ordenadores clásicos es, sencillamente, **copiar y pegar**. Si almacenas el bit lógicamente como $000$ o como $111$, bastará usar una regla de mayoría: si lees $010$, deduces que hubo un error en el segundo bit y debes forzarlo de nuevo a un $0$.

Sin embargo, el **Teorema de No-Clonación** cuántica estipula la imposibilidad física y matemática absoluta de crear una fotocopia independiente de un estado cuántico arbitrario desconocido $|\psi\rangle = \alpha|0\rangle + \beta|1\rangle$.

¿Cómo hacemos redundancia sin poder fotocopiar? **Entrelazando**. En vez de copiar el estado, clonamos indirectamente el conocimiento subyacente usando compuertas $CNOT$. 

Así, mapamos el estado puramente cuántico en el espacio protegido de 3 qubits, creando así un Código Repetidor:
$$|\psi\rangle = \alpha|0\rangle + \beta|1\rangle \quad \xrightarrow{\text{Codificación}} \quad |\psi_{log}\rangle = \alpha|000\rangle + \beta|111\rangle$$
*(Nótese que el estado **no es** $(\alpha|0\rangle + \beta|1\rangle) \otimes (\alpha|0\rangle + \beta|1\rangle) \otimes (\dots)$, lo cual violaría el teorema de no clonación, sino un único estado de base de múltiples partículas).*

## 4. Medición Diferencial o Medición de "Síndrome"

Aquí chocamos con el segundo muro infranqueable cuántico: el problema de la lectura destructiva. Si sospechamos que un rayo cósmico golpeó nuestro hardware y cambió la superposición a $\alpha|100\rangle + \beta|011\rangle$ (flipeando el primer qubit físico de $|0\rangle$ a $|1\rangle$), **no podemos mirar directamente los 3 qubits físicos para ver quién se equivocó**.
Si los leemos y medimos, ¡colapsaremos probabilísticamente las amplitudes ricas y preciosas $\alpha$ y $\beta$ de manera catastrófica y final a la base binaria! Perderemos nuestro super-poder de superposición a cambio de averiguar quién tenía el error.

Para arreglar un error sin mirar el estado, la Corrección Cuántica extrae el llamado **Síndrome**:
Usamos Qubits extra (Qubits de Síndrome o Auxiliares / Ancilares) y aplicamos compuertas CNOT entre nuestro preciado registro de datos lógico (los 3 de la base) empujando información diferencial al ancilar. Es decir, le preguntamos cuánticamente a la máquina sin mirarla a los ojos: *"Máquina, no me digas si eres $0$ o $1$, por favor dime únicamente **si el Qubit 1 y el Qubit 2 son diferentes entre sí**"*.
Al medir únicamente la ancila, extraemos paridad. Si son distintos, detectaste el error y sabes a quien aplicar la puerta correctora (puerta $X$ de bit-flip).

## 5. El Límite del código de repetición

El modelo $\alpha|000\rangle + \beta|111\rangle$ introducido arriba es estupendo, solucionando los errores clásicos (el Bit-Flip de Pauli $X$). Pero el mundo cuántico posee un terror inaudito de una variante propia adicional: el **Phase-Flip** de Pauli $Z$, donde $ |+\rangle $ viaja azarosamente hacia $ |-\rangle $. Para esto, necesitaremos codificar en la base Hadamard y dar el paso hacia códigos bidimensionales mucho más engrosados, como el **Código de Shor** de 9 qubits o los **Surface Codes** que estudiarás más adelante.

## 6. Ideas clave

- El Teorema de No-clonación prohíbe realizar una redudancia simple y directa (aislada) típica en ingeniería clásica. Debemos **Entrelazar** a manera profunda el conocimiento y crear una "macro partícula virtual" que sostenga la información unida.
- La Medición del Síndrome nos enseña un arte sutil y de pura magia técnica: es posible "medir el error sin observar accidentalmente la información oculta", midiendo paridades o diferencias relativas protegiendo así las fases de coherencia originales.

## Navegacion

- Anterior: [Traza parcial y entropia](../08_informacion_cuantica/02_traza_parcial_y_entropia.md)
- Siguiente: [Codigo de Shor: intuicion](02_codigo_de_shor_intuicion.md)
