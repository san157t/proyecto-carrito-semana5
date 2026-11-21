# Optimización del Carrito de Compras

## 1. Qué es

Módulo en Python que agrega productos a un carrito de compras y mantiene el
total, validando cantidades, precios y nombres. Hace parte del proyecto final del
seminario de IA generativa para desarrolladores y cubre tres historias de usuario
del documento de requisitos:

- **HU-01**: el carrito no acepta cantidades negativas.
- **HU-02**: si un producto no tiene precio, se muestra «Precio no disponible».
- **HU-03**: un producto sin precio no se puede agregar y el carrito no cambia.

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

Las validaciones se hacen en este orden: producto, precio y cantidad. Si una
falla, el carrito original no cambia.

| Entrada | Regla | Si no se cumple |
|---|---|---|
| `carrito` | dict con `items` y `total`; puede ser `{}`; se conservan sus otras claves | no se modifica nunca |
| `producto` | texto no vacío | `TypeError` / `ValueError` |
| `precio` | número finito mayor que 0; `None` significa que el producto no tiene precio | `None`: `PrecioNoDisponibleError("Precio no disponible")`; otros casos: `TypeError` / `ValueError` |
| `cantidad` | entero mayor o igual a 1 | menor que 0: `ValueError("La cantidad no puede ser negativa")`; igual a 0: `ValueError("La cantidad debe ser mayor a cero")`; no entero: `TypeError` |

`PrecioNoDisponibleError` hereda de `ValueError`, así que el código que ya
captura `ValueError` sigue funcionando.

Ejemplos:

1. `({}, "Cuaderno", 10000.0, 2)` → `{"items": {"Cuaderno": 2}, "total": 20000.0}`
2. `({"items": {"Cuaderno": 1}, "total": 10000.0}, "Regla", 1500.0, 1)`
   → `{"items": {"Cuaderno": 1, "Regla": 1}, "total": 11500.0}`
3. `({"items": {"Cuaderno": 1}, "total": 10000.0}, "Cuaderno", 10000.0, -2)`
   → lanza `ValueError("La cantidad no puede ser negativa")` y el carrito original no cambia.
4. `({"items": {"Cuaderno": 1}, "total": 10000.0}, "Lápiz", None, 1)`
   → lanza `PrecioNoDisponibleError("Precio no disponible")` y el carrito original no cambia.

**Historia HU-01.** Como cliente, quiero que el carrito no acepte cantidades
negativas para que el total refleje lo que realmente compro.

- *Escenario 1:* «Cuaderno» cuesta $10.000; con cantidad 2, el total es $20.000.
- *Escenario 2 (error):* con 1 «Cuaderno» ($10.000) y cantidad -2, el sistema
  muestra «La cantidad no puede ser negativa», la cantidad sigue en 1 y el total
  sigue en $10.000.

**Historia HU-02.** Como cliente, quiero ver un aviso de que el precio no está
disponible para entender por qué no puedo agregar el producto.

- *Escenario 1:* «Lápiz» (ID 1045) no tiene precio; al intentar agregarlo se ve
  «Precio no disponible» y ningún código de error.
- *Escenario 2 (error):* «Regla» también perdió su precio; al intentar agregarla
  con cantidad 3 se ve el mismo mensaje.

**Historia HU-03.** Como cliente, quiero que el sistema no me deje agregar un
producto sin precio para que el total no quede incompleto.

- *Escenario 1:* con el carrito vacío y total $0, intentar agregar «Lápiz» sin
  precio deja el carrito vacío y el total en $0.
- *Escenario 2 (error):* con 1 «Cuaderno» y total $10.000, intentar agregar
  «Lápiz» sin precio deja solo el «Cuaderno» y el total en $10.000.

**Supuestos y preguntas pendientes con el cliente**

- **P-05, cantidad 0:** Carlos no dijo qué hacer con la cantidad 0. Se bloquea,
  con un mensaje distinto («debe ser mayor a cero»), porque 0 no es negativo.
- **P-10, producto sin precio:** Carlos dijo «yo creo que lo mejor es…», no una
  regla firme. Se asume que un producto sin precio no se puede agregar.
- **Precio sin precio (`None`):** el módulo recibe el precio como argumento, así
  que «sin precio» se representa con `None`. Es una decisión de diseño propia.
- Las historias HU-04 a HU-08 (seguir comprando, alertas y registro) no están
  implementadas todavía.

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
├── tests/
│   ├── test_carrito.py         # pruebas de la semana 5 (HU-01)
│   ├── test_carrito_abuso.py   # pruebas de entradas hostiles (semana 6)
│   └── test_reglas_cliente.py  # reglas del cliente HU-01, HU-02, HU-03 (semana 7)
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