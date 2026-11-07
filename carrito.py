def agregar_producto(carrito: dict, producto: str, precio: float, cantidad: int) -> dict:
    if cantidad < 1:
        raise ValueError("La cantidad debe ser mayor a cero")
    
    nuevo_carrito = {
        "items": carrito.get("items", {}).copy(),
        "total": carrito.get("total", 0.0)
    }
    
    nuevo_carrito["items"][producto] = nuevo_carrito["items"].get(producto, 0) + cantidad
    nuevo_carrito["total"] += precio * cantidad
    
    return nuevo_carrito
