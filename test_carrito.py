import pytest
from carrito import agregar_producto

def test_agregar_producto_normal():
    resultado = agregar_producto({}, "Cuaderno", 10000.0, 2)
    assert resultado["total"] == 20000.0
    assert resultado["items"]["Cuaderno"] == 2

def test_agregar_producto_existente():
    carrito = {"items": {"Cuaderno": 1}, "total": 10000.0}
    resultado = agregar_producto(carrito, "Regla", 1500.0, 1)
    assert resultado["total"] == 11500.0
    assert resultado["items"]["Regla"] == 1

def test_agregar_producto_limite_uno():
    resultado = agregar_producto({}, "Borrador", 500.0, 1)
    assert resultado["total"] == 500.0
    assert resultado["items"]["Borrador"] == 1

def test_agregar_producto_limite_vacio():
    resultado = agregar_producto({}, "Marcador", 2000.0, 5)
    assert len(resultado["items"]) == 1
    assert resultado["total"] == 10000.0

def test_agregar_producto_error_negativo():
    carrito = {"items": {"Cuaderno": 1}, "total": 10000.0}
    with pytest.raises(ValueError, match="La cantidad debe ser mayor a cero"):
        agregar_producto(carrito, "Cuaderno", 10000.0, -2)

def test_agregar_producto_error_cero():
    # Prueba para el valor neutro 0 (pendiente P-05)
    carrito = {"items": {"Cuaderno": 1}, "total": 10000.0}
    with pytest.raises(ValueError, match="La cantidad debe ser mayor a cero"):
        agregar_producto(carrito, "Cuaderno", 10000.0, 0)

def test_agregar_producto_inmutabilidad_en_error():
    # El diccionario original no cambia al fallar (Escenario 2 de la historia)
    carrito = {"items": {"Cuaderno": 1}, "total": 10000.0}
    try:
        agregar_producto(carrito, "Cuaderno", 10000.0, -2)
    except ValueError:
        pass
    assert carrito == {"items": {"Cuaderno": 1}, "total": 10000.0}
def test_agregar_producto_inmutabilidad_exito():
    # Validar que el .copy() funciona: un agregado exitoso no muta el original
    carrito = {"items": {"Cuaderno": 1}, "total": 10000.0}
    resultado = agregar_producto(carrito, "Regla", 1500.0, 1)
    
    assert carrito == {"items": {"Cuaderno": 1}, "total": 10000.0}
    assert resultado["items"]["Regla"] == 1