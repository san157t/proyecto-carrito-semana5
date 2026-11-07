# Bitácora de uso de IA - Semana 5
**Estudiante:** Santiago Alarcón Alarcón
**Proyecto:** Optimización del Carrito de Compras

| Fecha | Sugerencia o Prompt | Decisión | Razón | Verificación |
|---|---|---|---|---|
| 07/11/26 | Prompt: "Actúa como analista y redactor. Escribe el contrato de la función para el README basándote en la HU-01 de mi documento, incluyendo firma, entradas, salidas y 3 ejemplos." | Aceptada | El contrato de Claude (el modelo) era claro, pero le agregué manualmente el supuesto explícito sobre la cantidad 0 para alinearlo con la pregunta P-05. | Validé contra la rúbrica que estuvieran los casos límite y ejemplos completos antes del código. |
| 07/11/26 | Prompt: "Escribe una implementación base en Python que muta el diccionario de entrada usando simples `if` para que las pruebas pasen rápidamente." | Aceptada | Quería llegar al verde sin complicarme. El código propuesto mutaba el diccionario directamente pero cumplía las 5 pruebas. | Ejecuté las pruebas y todas pasaron (estado verde). |
| 07/11/26 | Prompt: "Propón un refactor para esta función usando buenas prácticas de diccionarios, evitando la mutación original y simplificando con el método .get()." | Aceptada | El refactor mejoró el código creando una copia (`.copy()`), lo que evita efectos secundarios indeseados. | Corrí las pruebas después del refactor y validé que seguían pasando (verde). |
| 07/11/26 | Sugerencia propia tras revisión: "Necesito agregar pruebas para validar que la cantidad 0 tire error adecuado y que el carrito no mute si la función falla, y corregir el código." | Ajustada | Le pedí a Claude que me ayudara con la prueba de inmutabilidad (sugirió un bloque try-except) y agregué la prueba del 0. | Ejecuté las pruebas nuevas en rojo, corregí el mensaje de error del código y verifiqué el verde total. |

### Reflexión final
El asistente de código (Claude) fue clave para estructurar el contrato inicial y acelerar la creación de las pruebas TDD, ahorrándome tiempo en la escritura repetitiva de aserciones. Sin embargo, el error principal que atraparon mis pruebas fue un fallo de lógica en el mensaje de excepción: al agregar la prueba para el límite de valor `0`.
