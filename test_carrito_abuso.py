"""Pruebas de abuso de entradas (revisión de seguridad, semana 6).

Cada prueba corresponde a un hallazgo de revision_seguridad.md.
"""

import math

import pytest

from carrito import agregar_producto

CARRITO = {"items": {"Cuaderno": 1}, "total": 10000.0}


@pytest.mark.parametrize("precio", [-5.0, 0, 0.0])
def test_precio_negativo_o_cero_es_rechazado(precio):
    # H-01: un precio negativo reducía el total del carrito.
    with pytest.raises(ValueError, match="El precio debe ser un número positivo"):
        agregar_producto(CARRITO, "Regla", precio, 1)


@pytest.mark.parametrize("precio", [math.nan, math.inf, -math.inf])
def test_precio_no_finito_es_rechazado(precio):
    # H-01: nan o infinito dejaban el total corrupto.
    with pytest.raises(ValueError, match="El precio debe ser un número positivo"):
        agregar_producto(CARRITO, "Regla", precio, 1)


@pytest.mark.parametrize("cantidad", [2.5, True, "3", None])
def test_cantidad_que_no_es_entero_es_rechazada(cantidad):
    # H-02: 2.5 y True (que es un int en Python) se aceptaban.
    with pytest.raises(TypeError):
        agregar_producto(CARRITO, "Regla", 1500.0, cantidad)


@pytest.mark.parametrize("producto", ["", "   "])
def test_producto_vacio_es_rechazado(producto):
    # H-03: se aceptaban nombres vacíos.
    with pytest.raises(ValueError, match="no puede estar vacío"):
        agregar_producto(CARRITO, producto, 1500.0, 1)


def test_entrada_invalida_no_modifica_el_carrito_original():
    with pytest.raises(ValueError):
        agregar_producto(CARRITO, "Regla", -5.0, 1)

    assert CARRITO == {"items": {"Cuaderno": 1}, "total": 10000.0}
