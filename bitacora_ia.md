# Bitácora de uso de IA - Semana 5
**Estudiante:** Santiago Alarcón Alarcón
**Proyecto:** Optimización del Carrito de Compras

| Fecha | Sugerencia o Prompt | Decisión | Razón | Verificación |
|---|---|---|---|---|
| 07/11/26 | Prompt: "Escribe 5 pruebas pytest para la HU-01 usando este contrato..." | Aceptada | Las pruebas cubrían exactamente los casos normales, límites (carrito vacío y cantidad 1) y el error esperado. | Ejecuté `pytest test_carrito.py` sin crear el código base y verifiqué que fallaran correctamente buscando la función. |
| 07/11/26 | Prompt: "Escribe la implementación en Python para que estas pruebas pasen." | Ajustada | La IA mutaba el diccionario original `carrito`, lo cual es una mala práctica. Ajusté el código para retornar un diccionario nuevo copiando el estado anterior. | Ejecuté las pruebas nuevamente y todas pasaron en verde. |
| 07/11/26 | Sugerencia (IA): "Podemos cambiar el diccionario por una clase `Carrito` con métodos orientados a objetos." | Rechazada | El contrato especificaba claramente que las entradas y salidas debían ser diccionarios para mantener la simplicidad y alinearse con el diseño previo. | Revisé el contrato del README para confirmar que no requería clases complejas. |
| 07/11/26 | Prompt: "Propón un refactor simple para el código actual sin romper las pruebas." | Aceptada | Sugirió usar el método `.get()` de los diccionarios para inicializar `"items"` y `"total"` en una sola línea, eliminando varios `if` innecesarios. | Corrí la suite de pruebas tras aplicar el refactor y validé que seguían pasando sin modificaciones. |
| 07/11/26 | Prompt: "Redacta el contrato de la función para el README basándote en la HU-01." | Ajustada | La IA omitió indicar qué sucedía si el diccionario ingresaba sin claves preexistentes. Añadí esa aclaración en los supuestos y casos límite. | Leí la rúbrica del docente para verificar que los supuestos y los 3 ejemplos estuvieran completos. |

### Reflexión final
El asistente de código fue sumamente útil para acelerar la creación de las pruebas iniciales y estructurar la lógica base, ahorrándome la configuración repetitiva de pytest. Sin embargo, mis pruebas automatizadas actuaron como una red de seguridad vital: me permitieron rechazar la sugerencia de la IA de usar clases complejas y me dieron la confianza para aplicar un refactor de código seguro (usando `.get()`). Si tuviera que hacer algo diferente, le daría a la IA instrucciones más estrictas desde el primer *prompt* sobre no mutar estructuras de datos para evitar tener que corregirlo manualmente.