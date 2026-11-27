# Bitácora de uso de IA - Semana 5
**Estudiante:** Santiago Alarcón Alarcón
**Proyecto:** Optimización del Carrito de Compras

| Fecha | Sugerencia o Prompt | Decisión | Razón | Verificación |
|---|---|---|---|---|
| 07/11/26 | Prompt: "Escribe 5 pruebas automatizadas para la HU-01 de agregar_producto." | Aceptada | Las usé para iniciar el ciclo TDD. El commit inicial en rojo (e2f280b) demostró que las pruebas fallaban al no existir la función `agregar_producto`. | Ejecuté `pytest` y validé que fallaran como se esperaba en el paso rojo. |
| 07/11/26 | Prompt: "Escribe la implementación base para que pasen las pruebas." | Ajustada | La IA generó un código que mutaba el diccionario original. Lo ajusté en mi máquina local para usar `.copy()` y `.get()` antes del commit verde (6e6bf5a). | Las pruebas pasaron a verde localmente antes de registrar el commit. |
| 07/11/26 | Sugerencia de IA: "Implementar una clase Carrito que maneje Decimal internamente y un método cambiar_cantidad." | Rechazada | Mantuve diccionarios y funciones porque así lo definí en mi contrato del README y el cambio a clases obligaba a rehacer pruebas y contrato. | Revisé el contrato del README y las 5 pruebas ya escritas para confirmar la consistencia. |
| 07/11/26 | Prompt: "Sugiere un refactor para el código actual." | Aceptada | El asistente propuso varias mejoras. Apliqué una parte: extraje el valor mágico 1 a `CANTIDAD_MINIMA`, el mensaje a una constante y la validación a `_validar_cantidad`. | Verifiqué con pytest: las 7 pruebas que existían en ese momento seguían en verde (commit 9ba60c1). |
| 07/11/26 | Prompt: "¿Es segura mi prueba de inmutabilidad usando try/except: pass?" | Aceptada | La IA me explicó que era un falso positivo. El commit 808ecc0 trajo la octava prueba (éxito) y posteriormente corregí la prueba de error usando `pytest.raises(ValueError)`. | Corrí pytest y comprobé que las 8 pruebas evalúan la inmutabilidad y los errores de forma estricta. |

### Reflexión final
Las pruebas automatizadas me dieron seguridad para refactorizar la validación hacia la función interna `_validar_cantidad` sin romper la lógica. En este proceso, ninguna prueba falló por un error en el código de producción, ya que la implementación base era robusta. El verdadero error que atrapé —y que descubrí leyendo el código, no por un fallo en la consola— fue que mi prueba de inmutabilidad original era débil: el bloque `try/except: pass` habría marcado verde aunque la función no lanzara la excepción. Esto me enseñó que una prueba mal escrita otorga una falsa seguridad. Para la siguiente historia (HU-05), escribiré las aserciones con más cuidado y usaré la librería `Decimal` en lugar de `float` para evitar problemas de precisión monetaria (como que 0.1 * 3 resulte en 0.30000000000000004).
## Semana 6

| Fecha | Sugerencia o Prompt | Decisión | Razón | Verificación |
|---|---|---|---|---|
| 14/11/26 | Prompt de revisión de código y seguridad sobre `carrito.py` (commit d1d1461, con líneas numeradas); texto completo en `revision_seguridad.md`, sección 3 | Ajustada | La IA entregó 8 hallazgos y 6 sospechas. Acepté los 7 que pude reproducir y descarté como falsos positivos el control de acceso, la copia superficial y la condición de carrera. «No hay pruebas» era falso porque solo le pasé `carrito.py`. | Reproduje cada hallazgo en la consola contra d1d1461 y los clasifiqué en la sección 3 de `revision_seguridad.md`. |
| 14/11/26 | Sugerencia de IA: agregar `_validar_precio`, `_validar_cantidad` y `_validar_producto` con docstrings | Aceptada | Corrige precio negativo, `nan`, cantidad `2.5` o `True` y nombre vacío, que eran reales. Leí cada función y puedo explicarlas. | Escribí primero las pruebas de abuso (11 fallaron, commit ef70c8d) y luego pasaron las 22 pruebas con ruff y pip-audit limpios (commit 42fe9a8). |
| 14/11/26 | Código corregido completo que propuso la IA (con `Decimal` y `items` como diccionarios) | Rechazada | Rompe el contrato de HU-01 y mis pruebas, que usan `float` y `items[producto] == cantidad`; además el cambio de `Decimal` corresponde a HU-05. | Lo ejecuté contra `test_carrito.py` y fallaron las 8 pruebas. |
| 14/11/26 | Hallazgo de IA: el carrito descarta claves distintas de `items` y `total` (H-08) | Aceptada | Es un hallazgo real (el cupón se perdía) y la corrección es de una línea sin cambiar el contrato. | Prueba primero: 1 failed (commit d865ce5). Luego `{**carrito}` y 23 pruebas en verde (commit dc12ea2). |

**Agente de código:** no usé ningún agente en esta semana.

## Semana 7: de los requisitos a las pruebas

### Prompt 1

| Ficha | Contenido |
|---|---|
| Número y propósito | 1. Comprobar con evidencia dos defectos entre requisitos y código |
| Herramienta | Claude |
| Prompt exacto | ayudame a hacer el trabajo de la seman 7 |
| Resumen de la respuesta | Me dio comandos `git grep` y `git log -S`. Primero dijo que no podía abrir el repo y luego que sí. |
| Qué verificaste | Corrí los comandos yo. «no puede ser negativa» y «Precio no disponible» no aparecen en el código y `git log -S` salió vacío. El mensaje del código era «debe ser mayor a cero», en 3 pruebas. Leí HU-01, HU-02 y HU-03 en el documento de requisitos. |
| Defectos encontrados | La IA contradijo lo que dijo sobre el acceso al repo. Tuve que confirmar yo cada hecho con mi terminal. |
| Qué corregiste | Usé solo la evidencia de mi salida y del documento. |

### Prompt 2

| Ficha | Contenido |
|---|---|
| Número y propósito | 2. Pruebas desde las reglas del cliente (rojo) y código (verde) |
| Herramienta | Claude |
| Prompt exacto | bueno dame el paso de lo q falt apa entregar el trabajo |
| Resumen de la respuesta | Propuso `tests/test_reglas_cliente.py`, dos mensajes de cantidad y `PrecioNoDisponibleError`, con el orden producto, precio, cantidad. |
| Qué verificaste | Rojo `8b9fb2f`, luego verde `ebf15f5`. Comprobé el diff de `test_carrito.py` (solo 2 líneas) y `pytest` + `ruff`. |
| Defectos encontrados | Trabajé primero en la carpeta equivocada (`proyecto_carrito_corregido`) y varios commits salieron con «nothing to commit». Las pruebas viejas tenían el esperado sacado del código. `test_agregar_producto_existente` no prueba un producto existente. |
| Qué corregiste | Rehice las ediciones en el repo correcto. Decisiones que acepté: dos mensajes de cantidad, `PrecioNoDisponibleError` y el orden producto, precio, cantidad. |

### Prompt 3

| Ficha | Contenido |
|---|---|
| Número y propósito | 3. Pruebas de diseño de casos (paquete de la semana 7) |
| Herramienta | Claude |
| Prompt exacto | ayudame a verificar las pruebas |
| Resumen de la respuesta | Un zip con `conftest.py`, `test_casos_diseno.py` y `registro_pruebas.md` (commit `e58ae28`). |
| Qué verificaste | 69 pruebas en verde. Después rompí el código a propósito (prompt 4). |
| Defectos encontrados | Pasaron todas a la primera, así que no probaban nada hasta verlas fallar. |
| Qué corregiste | No modifiqué el paquete; lo validé rompiendo el código (prompt 4). |

### Prompt 4

| Ficha | Contenido |
|---|---|
| Número y propósito | 4. Romper el código a propósito |
| Herramienta | Claude |
| Prompt exacto | ayudame a encontrar los fallos |
| Resumen de la respuesta | 4 rupturas: quitar `if precio is None`, `<= 0`, cambiar el orden de validación y quitar `.copy()`. |
| Qué verificaste | Resultados: 7, 3, 3 y 1 pruebas fallaron. Cada ruptura se deshizo con `git restore carrito.py`. |
| Defectos encontrados | La IA predijo 9 fallos y fueron 7: `test_precio_no_disponible_es_un_value_error` protege la jerarquía de la excepción. La inmutabilidad en éxito depende de **una sola prueba**. No probé mover el producto. |
| Qué corregiste | Registré todo en `registro_pruebas.md` (`bb40066`, `ac8c3b9`). |

**`crear_historial.sh`:**si generó commits.

**Reflexión final:** la ia me ayudo mucho con el control de las prubeas y los fallos.