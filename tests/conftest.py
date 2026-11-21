"""Datos sintéticos y carritos de partida para las pruebas (semana 7).

Origen: datos sintéticos generados con IA (Claude) y revisados a mano.
Contexto: tienda escolar y de mercado en Colombia, precios en pesos.
No hay personas reales, teléfonos ni datos de contacto.
"""

import pytest


@pytest.fixture
def carrito_vacio():
    return {"items": {}, "total": 0.0}


@pytest.fixture
def carrito_con_cuaderno():
    return {"items": {"Cuaderno": 1}, "total": 10000.0}


@pytest.fixture
def catalogo_sintetico():
    return [
        # caso normal
        {"producto": "Cuaderno argollado", "precio": 8500.0, "cantidad": 2},
        # tilde y punto en el nombre
        {"producto": "Lápiz No. 2", "precio": 1200.0, "cantidad": 5},
        # ñ y centavos
        {"producto": "Piña oro", "precio": 4500.5, "cantidad": 2},
        # Ñ mayúscula y decimales que no son exactos en binario
        {"producto": "Ñame criollo", "precio": 3999.9, "cantidad": 3},
        # apóstrofo y cantidad en el límite (1)
        {"producto": "Panela D'Lujo", "precio": 5200.0, "cantidad": 1},
    ]
