"""Carrito de compras: lógica de HU-01, HU-02 y HU-03.

El carrito es un diccionario ``{"items": {producto: cantidad}, "total": float}``.
Las funciones no modifican el carrito recibido: devuelven uno nuevo.
"""

import math

CANTIDAD_MINIMA = 1
MENSAJE_CANTIDAD_INVALIDA = "La cantidad debe ser mayor a cero"
MENSAJE_CANTIDAD_NEGATIVA = "La cantidad no puede ser negativa"
MENSAJE_PRECIO_INVALIDO = "El precio debe ser un número positivo"
MENSAJE_PRECIO_NO_DISPONIBLE = "Precio no disponible"
MENSAJE_PRODUCTO_INVALIDO = "El nombre del producto no puede estar vacío"


class PrecioNoDisponibleError(ValueError):
    """El producto no tiene precio en el catálogo (HU-02 y HU-03)."""


def _validar_cantidad(cantidad: int) -> None:
    """Comprueba que la cantidad sea un entero mayor o igual a CANTIDAD_MINIMA.

    Raises:
        TypeError: si ``cantidad`` no es un entero (``True`` y ``2.5`` no valen).
        ValueError: con «La cantidad no puede ser negativa» si ``cantidad`` es
            menor que 0 (HU-01), o con «La cantidad debe ser mayor a cero» si
            es 0 (supuesto, pendiente P-05).
    """
    if isinstance(cantidad, bool) or not isinstance(cantidad, int):
        raise TypeError("La cantidad debe ser un número entero")
    if cantidad < 0:
        raise ValueError(MENSAJE_CANTIDAD_NEGATIVA)
    if cantidad < CANTIDAD_MINIMA:
        raise ValueError(MENSAJE_CANTIDAD_INVALIDA)


def _validar_precio(precio: float) -> None:
    """Comprueba que el precio exista, sea finito y mayor que cero.

    Raises:
        PrecioNoDisponibleError: si ``precio`` es ``None``, es decir, el
            producto no tiene precio (HU-02 y HU-03).
        TypeError: si ``precio`` no es un número (``True`` tampoco vale).
        ValueError: si ``precio`` es cero, negativo, ``nan`` o infinito.
    """
    if precio is None:
        raise PrecioNoDisponibleError(MENSAJE_PRECIO_NO_DISPONIBLE)
    if isinstance(precio, bool) or not isinstance(precio, (int, float)):
        raise TypeError("El precio debe ser un número")
    if not math.isfinite(precio) or precio <= 0:
        raise ValueError(MENSAJE_PRECIO_INVALIDO)


def _validar_producto(producto: str) -> None:
    """Comprueba que el nombre del producto sea un texto no vacío.

    Raises:
        TypeError: si ``producto`` no es un texto.
        ValueError: si ``producto`` está vacío o solo tiene espacios.
    """
    if not isinstance(producto, str):
        raise TypeError("El nombre del producto debe ser un texto")
    if not producto.strip():
        raise ValueError(MENSAJE_PRODUCTO_INVALIDO)


def agregar_producto(
    carrito: dict, producto: str, precio: float, cantidad: int
) -> dict:
    """Agrega un producto al carrito y devuelve un carrito nuevo.

    No modifica el carrito recibido y conserva sus otras claves. Si el producto
    ya estaba, suma la cantidad. Las validaciones se hacen en este orden:
    producto, precio y cantidad; si una falla, el carrito no cambia.

    Args:
        carrito: ``{"items": {producto: cantidad}, "total": float}``.
            Puede ser ``{}``, en cuyo caso se inicializa vacío.
        producto: nombre del producto (texto no vacío).
        precio: precio unitario, número finito mayor que cero. ``None``
            significa que el producto no tiene precio.
        cantidad: unidades a agregar, entero mayor o igual a 1.

    Returns:
        Un carrito nuevo con los ítems actualizados y el total recalculado
        (``total + precio * cantidad``).

    Raises:
        PrecioNoDisponibleError: si ``precio`` es ``None`` («Precio no
            disponible»). Es un ``ValueError``.
        TypeError: si algún argumento tiene un tipo inválido.
        ValueError: si ``cantidad`` < 1 (con mensaje distinto para los
            negativos y para el 0), ``precio`` <= 0 (o no es finito)
            o ``producto`` está vacío.

    Example:
        >>> agregar_producto({}, "Cuaderno", 10000.0, 2)
        {'items': {'Cuaderno': 2}, 'total': 20000.0}
    """
    _validar_producto(producto)
    _validar_precio(precio)
    _validar_cantidad(cantidad)

    nuevo_carrito = {
        **carrito,
        "items": carrito.get("items", {}).copy(),
        "total": carrito.get("total", 0.0),
    }
    items = nuevo_carrito["items"]
    items[producto] = items.get(producto, 0) + cantidad
    nuevo_carrito["total"] += precio * cantidad

    return nuevo_carrito
