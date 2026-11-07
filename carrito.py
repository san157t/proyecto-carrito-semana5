CANTIDAD_MINIMA = 1
MENSAJE_CANTIDAD_INVALIDA = "La cantidad debe ser mayor a cero"

def _validar_cantidad(cantidad: int) -> None:
    if cantidad < CANTIDAD_MINIMA:
        raise ValueError(MENSAJE_CANTIDAD_INVALIDA)

def agregar_producto(carrito: dict, producto: str, precio: float, cantidad: int) -> dict:
    _validar_cantidad(cantidad)
    
    nuevo_carrito = {
        "items": carrito.get("items", {}).copy(),
        "total": carrito.get("total", 0.0)
    }
    
    nuevo_carrito["items"][producto] = nuevo_carrito["items"].get(producto, 0) + cantidad
    nuevo_carrito["total"] += precio * cantidad
    
    return nuevo_carrito
