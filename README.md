# Optimización del Carrito de Compras

## 1. Qué es

Módulo en Python que agrega productos a un carrito de compras y mantiene el
total, validando cantidades, precios y nombres. Hace parte del proyecto final del
seminario de IA generativa para desarrolladores y cubre la historia de usuario
**HU-01**: el carrito no acepta cantidades negativas.

El carrito es un diccionario `{"items": {producto: cantidad}, "total": float}`.
La función `agregar_producto` no modifica el carrito que recibe: devuelve uno nuevo.

## 2. Requisitos

- Python 3.10 o superior.
- Solo para desarrollo (pruebas, linter y auditoría): `pytest`, `ruff` y
  `pip-audit`, con versión fijada en `requirements-dev.txt`.
- El código del carrito no tiene dependencias externas.

## 3. Instalación

```bash
git clone https://github.com/san157t/proyecto-carrito-semana5.git
cd proyecto-carrito-semana5
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

El proyecto todavía no usa variables de entorno. `.env.example` explica cómo
agregarlas más adelante; `.env` está en `.gitignore`.

## 4. Ejecución

El proyecto es un módulo, no una aplicación con interfaz. Se usa importando la función:

```python
from carrito import agregar_producto

carrito = agregar_producto({}, "Cuaderno", 10000.0, 2)
print(carrito)   # {'items': {'Cuaderno': 2}, 'total': 20000.0}
```

**Contrato de `agregar_producto(carrito, producto, precio, cantidad) -> dict`**

| Entrada | Regla | Si no se cumple |
|---|---|---|
| `carrito` | dict con `items` y `total`; puede ser `{}`; se conservan sus otras claves | no se modifica nunca |
| `producto` | texto no vacío | `TypeError` / `ValueError` |
| `precio` | número finito mayor que 0 | `TypeError` / `ValueError` |
| `cantidad` | entero mayor o igual a 1 (0 y negativos se bloquean; ver P-05) | `TypeError` / `ValueError("La cantidad debe ser mayor a cero")` |

Ejemplos:

1. `({}, "Cuaderno", 10000.0, 2)` → `{"items": {"Cuaderno": 2}, "total": 20000.0}`
2. `({"items": {"Cuaderno": 1}, "total": 10000.0}, "Regla", 1500.0, 1)`
   → `{"items": {"Cuaderno": 1, "Regla": 1}, "total": 11500.0}`
3. `({"items": {"Cuaderno": 1}, "total": 10000.0}, "Cuaderno", 10000.0, -2)`
   → lanza `ValueError` y el carrito original no cambia.

**Historia HU-01.** Como cliente, quiero que el carrito no acepte cantidades
negativas para que el total refleje lo que realmente compro.

- *Escenario 1:* «Cuaderno» cuesta $10.000; con cantidad 2, el total es $20.000.
- *Escenario 2 (error):* con 1 «Cuaderno» ($10.000) y cantidad -2, el sistema
  muestra un error, la cantidad sigue en 1 y el total sigue en $10.000.

## 5. Pruebas

```bash
pytest                 # pruebas y ejemplos de los docstrings
ruff check .           # linter (reglas E, F, B, S, W)
pip-audit -r requirements-dev.txt   # vulnerabilidades en dependencias
```

## 6. Estructura

```text
.
├── carrito.py                  # lógica y validaciones
├── test_carrito.py             # pruebas de la semana 5 (HU-01)
├── test_carrito_abuso.py       # pruebas de entradas hostiles (semana 6)
├── pyproject.toml              # configuración de ruff y pytest
├── requirements-dev.txt        # herramientas con versión fijada
├── .env.example                # plantilla de variables de entorno (vacía)
├── bitacora_ia.md              # bitácora de uso de IA
├── revision_seguridad.md       # informe de revisión de código y seguridad
├── LICENSE                     # licencia MIT
└── README.md
```

## 7. Uso de IA

Usé un asistente de IA para proponer pruebas, borradores de la implementación y del
refactor, y como segunda revisión de seguridad. Cada propuesta se verificó antes de
aceptarla: ejecutando las pruebas, el linter y comandos que reproducen cada hallazgo.
Las decisiones, con su razón y verificación, están en
[`bitacora_ia.md`](bitacora_ia.md); los hallazgos y su clasificación en
[`revision_seguridad.md`](revision_seguridad.md).

## 8. Autor y licencia

Santiago Alarcón Alarcón. Proyecto académico del seminario de IA generativa.
Licencia: MIT (ver el archivo [`LICENSE`](LICENSE)).
