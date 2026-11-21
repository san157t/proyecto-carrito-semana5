"""Casos diseñados con particiones, límites y tabla de decisión (semana 7).

El esperado de cada fila sale de la regla del cliente o del contrato del README
(ver registro_pruebas.md), nunca de ejecutar el código.
"""

import math

import pytest

from carrito import (
    PrecioNoDisponibleError,
    _validar_cantidad,
    _validar_precio,
    _validar_producto,
    agregar_producto,
)

# Mensajes esperados: texto del cliente (HU-01, HU-02) y del contrato.
MSG_NEGATIVA = "^La cantidad no puede ser negativa$"
MSG_CERO = "^La cantidad debe ser mayor a cero$"
MSG_PRECIO = "^El precio debe ser un número positivo$"
MSG_SIN_PRECIO = "^Precio no disponible$"
MSG_PRODUCTO = "^El nombre del producto no puede estar vacío$"


# ---------- Función 1: _validar_cantidad (HU-01) ----------


@pytest.mark.parametrize(
    "cantidad",
    [
        pytest.param(-100, id="negativa-grande"),  # partición: negativos
        pytest.param(-2, id="negativa-del-criterio"),  # HU-01 escenario 2
        pytest.param(-1, id="limite-ultimo-negativo"),  # borde: justo bajo 0
    ],
)
def test_cantidad_negativa_lanza_value_error(cantidad):
    with pytest.raises(ValueError, match=MSG_NEGATIVA):
        _validar_cantidad(cantidad)


def test_cantidad_cero_lanza_value_error():
    # Borde 0: el cliente no lo definió (P-05); se bloquea por supuesto
    with pytest.raises(ValueError, match=MSG_CERO):
        _validar_cantidad(0)


@pytest.mark.parametrize(
    "cantidad",
    [
        pytest.param(2.5, id="decimal"),  # no es entero
        pytest.param(True, id="booleano"),  # bool es int en Python, no vale
        pytest.param("3", id="texto"),  # texto con aspecto de número
        pytest.param(None, id="none"),  # ausencia de valor
    ],
)
def test_cantidad_tipo_invalido_lanza_type_error(cantidad):
    with pytest.raises(TypeError):
        _validar_cantidad(cantidad)


@pytest.mark.parametrize(
    "cantidad, total_esperado",
    [
        pytest.param(1, 1500.0, id="limite-primer-valido"),  # borde: 1 x 1.500
        pytest.param(2, 3000.0, id="dos-HU05-escenario1"),  # HU-05: 2 Regla
        pytest.param(3, 4500.0, id="tres-HU05-escenario2"),  # HU-05: 3 Regla
        pytest.param(100, 150000.0, id="grande"),  # partición válida alta
    ],
)
def test_cantidad_valida_suma_exacta(carrito_vacio, cantidad, total_esperado):
    resultado = agregar_producto(carrito_vacio, "Regla", 1500.0, cantidad)
    assert resultado["items"] == {"Regla": cantidad}
    assert resultado["total"] == pytest.approx(total_esperado)


# ---------- Función 2: _validar_precio (HU-02, HU-03 y contrato) ----------


def test_precio_none_lanza_precio_no_disponible():
    # HU-02: sin precio se muestra «Precio no disponible»
    with pytest.raises(PrecioNoDisponibleError, match=MSG_SIN_PRECIO):
        _validar_precio(None)


def test_precio_no_disponible_es_un_value_error():
    # Decisión de diseño del README: el código que captura ValueError sigue vivo
    assert issubclass(PrecioNoDisponibleError, ValueError)


@pytest.mark.parametrize(
    "precio",
    [
        pytest.param(0, id="cero-limite"),  # borde: último inválido (contrato)
        pytest.param(-5.0, id="negativo"),  # partición: negativos
        pytest.param(math.nan, id="nan"),  # no es un número usable
        pytest.param(math.inf, id="infinito"),  # no es finito
        pytest.param(-math.inf, id="menos-infinito"),  # no es finito
    ],
)
def test_precio_invalido_lanza_value_error(precio):
    with pytest.raises(ValueError, match=MSG_PRECIO):
        _validar_precio(precio)


def test_precio_minimo_positivo_es_valido(carrito_vacio):
    # Borde: primer valor válido sobre 0
    resultado = agregar_producto(carrito_vacio, "Caramelo", 0.01, 1)
    assert resultado["total"] == pytest.approx(0.01)


@pytest.mark.parametrize(
    "precio",
    [
        pytest.param(True, id="booleano"),  # bool no es un precio
        pytest.param("10000", id="texto"),  # texto con aspecto de número
        pytest.param([], id="lista"),  # tipo sin relación
    ],
)
def test_precio_tipo_invalido_lanza_type_error(precio):
    with pytest.raises(TypeError):
        _validar_precio(precio)


# ---------- Función 3: _validar_producto (contrato) ----------


@pytest.mark.parametrize(
    "producto",
    [
        pytest.param("", id="vacio"),  # texto vacío
        pytest.param("   ", id="solo-espacios"),  # solo espacios
    ],
)
def test_producto_vacio_lanza_value_error(producto):
    with pytest.raises(ValueError, match=MSG_PRODUCTO):
        _validar_producto(producto)


@pytest.mark.parametrize(
    "producto",
    [
        pytest.param(None, id="none"),  # ausencia de valor
        pytest.param(123, id="numero"),  # tipo equivocado
    ],
)
def test_producto_tipo_invalido_lanza_type_error(producto):
    with pytest.raises(TypeError):
        _validar_producto(producto)


# ---------- Función 4: agregar_producto (combina condiciones) ----------


@pytest.mark.parametrize(
    "carrito, producto, precio, cantidad, items, total",
    [
        pytest.param(
            {}, "Cuaderno", 10000.0, 2,
            {"Cuaderno": 2}, 20000.0,
            id="R1-carrito-sin-claves",
        ),  # HU-01 escenario 1
        pytest.param(
            {"items": {"Cuaderno": 1}, "total": 10000.0}, "Regla", 1500.0, 1,
            {"Cuaderno": 1, "Regla": 1}, 11500.0,
            id="R1-producto-nuevo",
        ),  # se agrega un producto distinto
        pytest.param(
            {"items": {"Cuaderno": 1}, "total": 10000.0}, "Cuaderno", 10000.0, 2,
            {"Cuaderno": 3}, 30000.0,
            id="R1-producto-existente",
        ),  # el producto ya estaba: se suma la cantidad
        pytest.param(
            {}, "Café de Huila", 1499.9, 3,
            {"Café de Huila": 3}, 4499.7,
            id="R1-decimales",
        ),  # HU-05: decimales (centavos: pregunta P-06)
    ],
)
def test_agregar_producto_valido_suma_total(
    carrito, producto, precio, cantidad, items, total
):
    resultado = agregar_producto(carrito, producto, precio, cantidad)
    assert resultado["items"] == items
    assert resultado["total"] == pytest.approx(total)


# Tabla de decisión: prioridad producto > precio > cantidad (decisión de diseño).
@pytest.mark.parametrize(
    "producto, precio, cantidad, error, mensaje",
    [
        pytest.param(
            "", 1000.0, 1, ValueError, MSG_PRODUCTO,
            id="R2-producto-vacio",
        ),  # producto inválido, lo demás válido
        pytest.param(
            "", None, -2, ValueError, MSG_PRODUCTO,
            id="R2-producto-gana-a-todo",
        ),  # producto inválido con precio y cantidad también inválidos
        pytest.param(
            "Lápiz", None, 1, PrecioNoDisponibleError, MSG_SIN_PRECIO,
            id="R3-sin-precio",
        ),  # HU-02 y HU-03
        pytest.param(
            "Lápiz", None, -2, PrecioNoDisponibleError, MSG_SIN_PRECIO,
            id="R3-sin-precio-gana-a-cantidad",
        ),  # precio se valida antes que cantidad
        pytest.param(
            "Lápiz", -5.0, 1, ValueError, MSG_PRECIO,
            id="R4-precio-negativo",
        ),  # precio inválido, producto y cantidad válidos
        pytest.param(
            "Lápiz", -5.0, -2, ValueError, MSG_PRECIO,
            id="R4-precio-gana-a-cantidad",
        ),  # precio inválido con cantidad también inválida
        pytest.param(
            "Cuaderno", 10000.0, -2, ValueError, MSG_NEGATIVA,
            id="R5-cantidad-negativa",
        ),  # HU-01 escenario 2
        pytest.param(
            "Cuaderno", 10000.0, 0, ValueError, MSG_CERO,
            id="R6-cantidad-cero",
        ),  # supuesto P-05
    ],
)
def test_error_lanza_el_tipo_correcto_y_no_modifica_el_carrito(
    carrito_con_cuaderno, producto, precio, cantidad, error, mensaje
):
    with pytest.raises(error, match=mensaje):
        agregar_producto(carrito_con_cuaderno, producto, precio, cantidad)
    assert carrito_con_cuaderno == {"items": {"Cuaderno": 1}, "total": 10000.0}


# ---------- Datos sintéticos (fixture catalogo_sintetico) ----------


def test_catalogo_sintetico_suma_total_y_conserva_nombres(
    carrito_vacio, catalogo_sintetico
):
    carrito = carrito_vacio
    for fila in catalogo_sintetico:
        carrito = agregar_producto(
            carrito, fila["producto"], fila["precio"], fila["cantidad"]
        )
    assert carrito["items"] == {
        "Cuaderno argollado": 2,
        "Lápiz No. 2": 5,
        "Piña oro": 2,
        "Ñame criollo": 3,
        "Panela D'Lujo": 1,
    }
    # 17.000 + 6.000 + 9.001 + 11.999,70 + 5.200 calculado a mano
    assert carrito["total"] == pytest.approx(49200.7)
