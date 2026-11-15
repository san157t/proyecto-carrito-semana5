# Informe de revisión de código y seguridad

Proyecto: Optimización del Carrito de Compras
Estudiante: Santiago Alarcón Alarcón
Fecha: 2026-11-14
Commit revisado: d1d1461 (antes de las correcciones)

## 1. Herramientas y criterios

- **Linter:** ruff 0.17.5 con las reglas E, F, B, S y W. Configuración en `pyproject.toml`.
- **Auditoría de dependencias:** pip-audit 2.10.1 sobre `requirements-dev.txt`. Resultado: sin vulnerabilidades conocidas.
- **Lista de revisión:** la de la semana 6 (corrección y pruebas, diseño y legibilidad, seguridad).
- **Revisión con IA:** `claude` en un chat nuevo, con el prompt de la sección 3.

### Puntos de seguridad revisados

| Punto | ¿Aplica? | Resultado |
|---|---|---|
| Inyección (consultas con parámetros) | No: el proyecto no tiene base de datos ni arma consultas ni comandos con texto del usuario | Sin hallazgos |
| Secretos (código, historial, .gitignore, .env.example) | Sí | Sin claves en el código ni en el historial (`git log -p --all` solo muestra la línea `.env` de `.gitignore`). `.env` ya estaba ignorado; faltaba `.env.example` (H-06) |
| Contraseñas (scrypt, bcrypt o argon2 con sal) | No: no se guardan usuarios ni contraseñas | Sin hallazgos |
| Control de acceso (rol verificado y prueba de abuso) | No: no hay usuarios ni roles | La prueba de abuso equivalente es la de entradas hostiles (H-01 a H-03) |
| Dependencias (existen, necesarias, versión fijada, pip-audit) | Sí | El código no usa librerías externas. Las herramientas de desarrollo tienen versión fijada y pip-audit no reporta vulnerabilidades (H-06) |

## 2. Tabla de hallazgos

| Id | Archivo y línea | Problema | Categoría | Severidad | Corrección | Commit |
|---|---|---|---|---|---|---|
| H-01 | carrito.py:8-19 | `precio` sin validar: `-5.0` reduce el total, `nan` e infinito lo corrompen; el README decía «decimal positivo» | A04 Diseño inseguro / validación de entradas | Media | `_validar_precio` y pruebas de abuso | `42fe9a8` |
| H-02 | carrito.py:8-19 | `cantidad` acepta `2.5` y `True` (en Python `True` es un `int`); el contrato dice entero. Con texto o `None` fallaba solo por accidente (`TypeError` al comparar con `<`) | Validación de entradas | Media | `_validar_cantidad` exige entero y rechaza `bool`; pruebas de abuso | `42fe9a8` |
| H-03 | carrito.py:8-19 | `producto` acepta texto vacío o solo espacios | Validación de entradas | Baja | `_validar_producto` y pruebas | `42fe9a8` |
| H-04 | carrito.py:8 y 16 | E501: línea de 89 caracteres (límite 88) | Estilo | Baja | Firma y diccionario en varias líneas | `42fe9a8` |
| H-05 | carrito.py:10, 15, 18; test_carrito.py:41, 47, 49 | W293 y W292: espacios en líneas en blanco y falta de salto de línea final | Estilo | Baja | `ruff --fix`; en las pruebas solo cambia el formato, no su lógica | `1700470 y 42fe9a8` |
| H-06 | raíz del repo | Sin `pyproject.toml`, sin versiones fijadas y sin `.env.example` | Configuración / dependencias | Baja | Se agregan `pyproject.toml`, `requirements-dev.txt` y `.env.example` | `5539a09` |
| H-07 | carrito.py | Funciones sin docstring | Mantenibilidad | Baja | Docstrings con qué hacen, qué reciben, qué devuelven y qué errores lanzan; el ejemplo se comprueba con doctest | `42fe9a8` |
| H-08 | carrito.py:11-14 | El resultado descarta cualquier clave del carrito distinta de `items` y `total` (por ejemplo `cupon`) | Corrección (pérdida de datos) | Media | `{**carrito, ...}` y prueba `test_conserva_otras_claves_del_carrito` | `d865ce5` y `dc12ea2` |

**Severidad:** alta (permite acceder o cambiar datos sin permiso, o expone secretos), media (error probable o riesgo con condiciones), baja (estilo o mantenibilidad).

### Avisos del linter no corregidos

| Regla | Archivo y línea | Por qué se mantiene |
|---|---|---|
| S101 | test_carrito.py y test_carrito_abuso.py (todos los `assert`) | `assert` es la forma normal de comprobar en pytest. Se ignora solo en `test_*.py` desde `pyproject.toml` |

## 3. Revisión con IA

**Asistente:** `claude`, en un chat nuevo. Se le pasó `carrito.py` del commit d1d1461 con las líneas numeradas, sin las pruebas. Prompt exacto:

```text
Actúa como revisor de código senior con enfoque en seguridad.
Revisa el siguiente archivo Python (carrito.py) con estos criterios:
1. Corrección y pruebas.
2. Diseño y legibilidad.
3. Seguridad: inyección, secretos, contraseñas, control de acceso,
   dependencias y validación de entradas.

Entrégame:
- Una tabla de hallazgos con las columnas: Id, línea, problema,
  categoría, severidad (alta, media o baja) y corrección sugerida.
- Dos secciones separadas: "Problemas seguros" (que puedas demostrar
  con una entrada concreta) y "Sospechas" (que podrían no ser reales).
- Si un criterio no aplica, dilo y explica por qué.
- No inventes líneas ni funciones que no estén en el código.

Contexto: es un carrito de compras en Python con funciones y
diccionarios. Historia HU-01: el carrito no acepta cantidades negativas.
Las líneas del código vienen numeradas.

Código:
```

| Hallazgo de la IA | ¿Real o falso positivo? | Cómo lo verifiqué |
|---|---|---|
| IA-H-01: precio negativo, cero, `nan` o `inf` (líneas 8 y 17); la clasifica Alta | Real | Contra d1d1461: totales `-5.0`, `nan` e `inf`. Corregido (H-01). Difiero en dos cosas: yo rechazo el precio 0 porque el contrato dice «positivo», y dejo la severidad en Media porque no da acceso ni expone datos |
| IA-H-02: cantidad `2.5`, `inf` o `True` pasa la validación (líneas 4-6) | Real | `2.5` da total `25.0`; `inf` da `items: inf`; `True` cuenta como 1. Corregido (H-02) |
| IA-H-03: con texto o `None` lanza `TypeError` y no `ValueError` (línea 5) | Real, baja | Traceback `'<' not supported between instances of 'str' and 'int'`. Ahora hay un `TypeError` intencional con mensaje claro |
| IA-H-04: se descartan claves del carrito (líneas 11-14) | Real | `agregar_producto({"items": {}, "total": 0.0, "cupon": "DESC10"}, "pan", 10.0, 1)` no devuelve `cupon`. Corregido (H-08) |
| IA-H-05: dinero con `float` | Real, aplazado | `0.1 + 0.2` da `0.30000000000000004`. Ver pendientes |
| IA-H-06: el precio por producto se pierde | Real, de diseño, aplazado | Agregar `pan` a 10.0 y luego a 99.0 da `items: {"pan": 2}` y `total: 109.0`. Ver pendientes |
| IA-H-07: `producto` sin validar | Real | Nombre `''` aceptado. Corregido (H-03) |
| IA-H-08: «no hay pruebas ni documentación» | Parcialmente falso positivo | Solo le pasé `carrito.py`, así que no vio que `test_carrito.py` ya tenía 8 pruebas. Los docstrings sí faltaban: corregido (H-07) |
| IA-S-01: producto vacío por falta de validación en el llamador | Real (repite IA-H-07) | Mismo caso que IA-H-07 |
| IA-S-02: falta de control de acceso | Falso positivo | No hay usuarios, sesiones ni roles; ver tabla de puntos revisados |
| IA-S-03: entero enorme en `cantidad` | No confirmada | `10**30` se procesa sin error; sería una regla de negocio (cantidad máxima) que no existe en los requisitos |
| IA-S-04: la copia con `.copy()` es superficial | Falso positivo hoy | Los valores de `items` son enteros inmutables; lo cubre la prueba `inmutabilidad_exito` |
| IA-S-05: `carrito=None` falla con `AttributeError` | Real, menor, aplazado | `agregar_producto(None, "X", 10.0, 1)` lanza `AttributeError`. Ver pendientes |
| IA-S-06: condición de carrera entre hilos | Falso positivo | La función no muta el carrito recibido ni comparte estado |
| Código corregido que propone la IA | Rechazado | Lo probé contra mis 8 pruebas y fallan las 8: exige `Decimal` (rechaza el `float`) y cambia `items` a diccionarios con `precio` y `cantidad`, lo que rompe el contrato de HU-01 |

**Lo que la IA no encontró:** la IA no señaló que `total` se toma del carrito recibido sin recalcularlo: `agregar_producto({"items": {}, "total": -1000.0}, "X", 10.0, 1)` devuelve `total: -990.0`, así que un carrito manipulado conserva su total falso. Lo vi en una primera revisión que hice antes de este chat, lo reproduje yo mismo en consola y el chat nuevo de revisión no lo mencionó. Queda en pendientes.

**Evidencia de pruebas primero:** las pruebas de abuso entraron antes que la corrección. El commit `ef70c8d` las agregó y 11 fallaron contra el código anterior (todas con «DID NOT RAISE»); `42fe9a8` las puso en verde. Con H-08 se repitió: `d865ce5` agregó la prueba y falló (1 failed, 22 passed) y `dc12ea2` la corrigió. Resultado final: 23 pruebas pasan, ruff sin avisos y pip-audit sin vulnerabilidades.

## 4. Pendientes

| Pendiente | Por qué no se corrigió todavía | Plan |
|---|---|---|
| Guardar el precio por ítem y recalcular el total en lugar de confiar en el `total` recibido (IA-H-06 y lo que la IA no encontró) | Cambia la estructura del carrito y el contrato de HU-01 | Rediseñar junto con HU-05 |
| Usar `Decimal` para el dinero (IA-H-05) | Rompe la compatibilidad con las pruebas actuales, que comparan con `float` | Hacerlo en HU-05 (suma exacta) con pruebas nuevas |
| Cantidad 0: se bloquea por ahora | Pregunta P-05 sin respuesta de Carlos | Confirmar con Carlos y ajustar contrato y pruebas |
| Validar la estructura del carrito recibido (IA-S-05, `carrito=None`) | Fuera del alcance de HU-01 | Agregar validación cuando haya más funciones |
| Cantidad máxima por producto (IA-S-03) | No hay requisito que la defina | Preguntar a Carlos si se necesita |

**Claves expuestas:** Ninguna.

