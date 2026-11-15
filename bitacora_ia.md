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
