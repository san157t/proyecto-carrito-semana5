## Funcionalidad de la semana 5

**Historia de usuario (HU-01):** Como cliente, quiero que el carrito no acepte cantidades negativas para que el total refleje lo que realmente compro.

**Criterios de aceptación:**
* Escenario 1: Cantidad válida. Dado que «Cuaderno» cuesta $10.000, cuando escribo cantidad 2, entonces el total del carrito es $20.000.
* Escenario 2 (error): Cantidad negativa. Dado que el carrito tiene 1 «Cuaderno» y un total de $10.000, cuando escribo cantidad -2 con el teclado, entonces el sistema muestra un error, la cantidad sigue en 1 y el total sigue en $10.000.

**Contrato de la función:**
* **Firma:** `def agregar_producto(carrito: dict, producto: str, precio: float, cantidad: int) -> dict:`
* **Entradas:** `carrito` (diccionario con estado actual), `producto` (cadena de texto), `precio` (decimal positivo), `cantidad` (entero).
* **Salidas:** Un diccionario actualizado con los ítems y el nuevo total calculado.
* **Supuestos y casos límite:** La cantidad mínima válida es `1`. Se asume (pendiente de confirmar P-05 con Carlos) que la cantidad 0 también se bloquea y lanza excepción. Cualquier cantidad menor a `1` lanzará un error explícito. Si el carrito entra vacío `{}`, se inicializan sus claves.
* **Ejemplos:**
  1. Entrada normal: `({}, "Cuaderno", 10000.0, 2)` -> Salida: `{"items": {"Cuaderno": 2}, "total": 20000.0}`
  2. Entrada existente: `({"items": {"Cuaderno": 1}, "total": 10000.0}, "Regla", 1500.0, 1)` -> Salida: `{"items": {"Cuaderno": 1, "Regla": 1}, "total": 11500.0}`
  3. Entrada error: `({"items": {"Cuaderno": 1}, "total": 10000.0}, "Cuaderno", 10000.0, -2)` -> Salida: Lanza `ValueError`.

**Cómo ejecutar las pruebas:**
Ejecuta el siguiente comando en la raíz del proyecto:
`pytest test_carrito.py -v`
