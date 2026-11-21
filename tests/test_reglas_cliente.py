import pytest

from carrito import PrecioNoDisponibleError, agregar_producto


@pytest.mark.parametrize("cantidad", [-1, -2])
def test_hu01_cantidad_negativa_mensaje_y_carrito_intacto(cantidad):
    carrito = {"items": {"Cuaderno": 1}, "total": 10000.0}
    with pytest.raises(ValueError, match="La cantidad no puede ser negativa"):
        agregar_producto(carrito, "Cuaderno", 10000.0, cantidad)
    assert carrito == {"items": {"Cuaderno": 1}, "total": 10000.0}


def test_hu02_regla_sin_precio_muestra_mensaje():
    carrito = {"items": {"Cuaderno": 1}, "total": 10000.0}
    with pytest.raises(PrecioNoDisponibleError) as error:
        agregar_producto(carrito, "Regla", None, 3)
    assert str(error.value) == "Precio no disponible"


def test_hu03_carrito_vacio_sigue_vacio():
    carrito = {"items": {}, "total": 0.0}
    with pytest.raises(PrecioNoDisponibleError):
        agregar_producto(carrito, "Lápiz", None, 1)
    assert carrito == {"items": {}, "total": 0.0}


def test_hu03_carrito_con_cuaderno_no_cambia():
    carrito = {"items": {"Cuaderno": 1}, "total": 10000.0}
    with pytest.raises(PrecioNoDisponibleError):
        agregar_producto(carrito, "Lápiz", None, 1)
    assert carrito == {"items": {"Cuaderno": 1}, "total": 10000.0}


def test_prioridad_precio_antes_que_cantidad():
    with pytest.raises(PrecioNoDisponibleError):
        agregar_producto({}, "Lápiz", None, -2)