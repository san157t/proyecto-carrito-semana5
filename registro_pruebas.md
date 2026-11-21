# Registro de pruebas: tabla de casos y pruebas de la IA

Proyecto: Optimización del Carrito de Compras
Estudiante: Santiago Alarcón Alarcón
Fecha: 2026-11-21

## 1. Tabla de casos

El oráculo son las historias de mi documento de requisitos de la semana 3 y,
donde el cliente no dijo nada, el contrato del README. Cuando el esperado viene
del contrato y no del cliente, la tabla lo marca como «contrato».

### Regla 1: `_validar_cantidad` (HU-01, cantidades válidas)

**Regla completa (el oráculo):** HU-01. «Como cliente, quiero que el carrito no
acepte cantidades negativas para que el total refleje lo que realmente compro.»
Escenario 2: con 1 «Cuaderno» y total $10.000, al escribir cantidad -2 el sistema
muestra «La cantidad no puede ser negativa», la cantidad sigue en 1 y el total
en $10.000. El cliente no definió el 0 (P-05) ni el tipo de dato; esos salen del
contrato: el 0 se bloquea y la cantidad debe ser un entero.

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Partición inválida | Negativos | -100 | ValueError «La cantidad no puede ser negativa» | test_cantidad_negativa_lanza_value_error[negativa-grande] |
| Partición inválida | Negativo del criterio | -2 | ValueError, mismo mensaje | test_cantidad_negativa_lanza_value_error[negativa-del-criterio] |
| Límite | Último negativo | -1 | ValueError, mismo mensaje | test_cantidad_negativa_lanza_value_error[limite-ultimo-negativo] |
| Límite | Cero (contrato, P-05) | 0 | ValueError «La cantidad debe ser mayor a cero» | test_cantidad_cero_lanza_value_error |
| Límite | Primer valor válido | 1 (precio 1.500) | total 1.500 | test_cantidad_valida_suma_exacta[limite-primer-valido] |
| Partición válida | Cantidades 2, 3 y 100 | 2, 3, 100 (precio 1.500) | total 3.000, 4.500 y 150.000 | test_cantidad_valida_suma_exacta[dos-HU05-escenario1], [tres-HU05-escenario2], [grande] |
| Partición inválida | Decimal (contrato) | 2.5 | TypeError | test_cantidad_tipo_invalido_lanza_type_error[decimal] |
| Partición inválida | Booleano (contrato) | True | TypeError | test_cantidad_tipo_invalido_lanza_type_error[booleano] |
| Partición inválida | Texto (contrato) | "3" | TypeError | test_cantidad_tipo_invalido_lanza_type_error[texto] |
| Partición inválida | Ausente (contrato) | None | TypeError | test_cantidad_tipo_invalido_lanza_type_error[none] |

**Ambigüedades encontradas:** (1) Cantidad 0: Carlos nunca dijo si se elimina o
se bloquea (P-05). Decidí bloquearla con un mensaje distinto, porque 0 no es
negativo y el mensaje del cliente sería falso. (2) El cliente no habló de tipos:
rechazar decimales, booleanos y texto es una decisión mía del contrato.

### Regla 2: `_validar_precio` (HU-02, HU-03 y contrato del precio)

**Regla completa (el oráculo):** HU-02. Si «Lápiz» (ID 1045) no tiene precio, al
intentar agregarlo se ve el mensaje «Precio no disponible» y ningún código de
error. HU-03 (Must). El sistema no deja agregar un producto sin precio y el
carrito no cambia. Contrato: el precio es un número finito mayor que 0.

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Partición inválida | Sin precio | None | PrecioNoDisponibleError «Precio no disponible» | test_precio_none_lanza_precio_no_disponible |
| Partición inválida | Sin precio es un ValueError (diseño) | PrecioNoDisponibleError | subclase de ValueError | test_precio_no_disponible_es_un_value_error |
| Límite | Último inválido (contrato) | 0 | ValueError «El precio debe ser un número positivo» | test_precio_invalido_lanza_value_error[cero-limite] |
| Límite | Primer valor válido | 0.01 | total 0.01 | test_precio_minimo_positivo_es_valido |
| Partición inválida | Negativo | -5.0 | ValueError, mismo mensaje | test_precio_invalido_lanza_value_error[negativo] |
| Partición inválida | No es un número | nan | ValueError, mismo mensaje | test_precio_invalido_lanza_value_error[nan] |
| Partición inválida | No finito | inf y -inf | ValueError, mismo mensaje | test_precio_invalido_lanza_value_error[infinito], [menos-infinito] |
| Partición inválida | Tipo equivocado | True, "10000", [] | TypeError | test_precio_tipo_invalido_lanza_type_error[booleano], [texto], [lista] |

**Ambigüedades encontradas:** (1) Precio 0: el cliente no dijo si un producto
gratis es válido. Lo rechacé por contrato. (2) Centavos (P-06): Carlos no
confirmó si los precios llevan centavos, así que probé decimales como 1.499,90
con `pytest.approx`. (3) P-10: Carlos dijo «yo creo que lo mejor es…» sobre no
permitir agregar un producto sin precio; lo tomé como regla, pero queda
pendiente. (4) El cliente no dijo cómo llega un producto «sin precio» al código;
decidí representarlo con `None`.

### Regla 3: `_validar_producto` (contrato del nombre)

**Regla completa (el oráculo):** el nombre del producto es un texto no vacío.
Esta regla viene de mi revisión de seguridad de la semana 6, no del cliente.

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Partición inválida | Texto vacío | "" | ValueError «El nombre del producto no puede estar vacío» | test_producto_vacio_lanza_value_error[vacio] |
| Límite | Solo espacios | "   " | ValueError, mismo mensaje | test_producto_vacio_lanza_value_error[solo-espacios] |
| Partición inválida | Ausente | None | TypeError | test_producto_tipo_invalido_lanza_type_error[none] |
| Partición inválida | Tipo equivocado | 123 | TypeError | test_producto_tipo_invalido_lanza_type_error[numero] |
| Partición válida | Nombres con tildes, Ñ y apóstrofo | datos sintéticos | se agregan con su nombre intacto | test_catalogo_sintetico_suma_total_y_conserva_nombres |

**Ambigüedades encontradas:** el cliente no habló del nombre. Los espacios solos
cuentan como vacío por decisión mía.

### Regla 4: `agregar_producto` (combina producto, precio y cantidad)

**Regla completa (el oráculo):** HU-01, HU-03 y HU-05. Agregar un producto suma
`precio × cantidad` al total y devuelve un carrito nuevo. HU-05: 2 «Regla» de
$1.500 dan $3.000 y 3 «Regla» dan $4.500. Si el producto, el precio o la cantidad
son inválidos, se lanza un error y el carrito no cambia (HU-01 escenario 2 y
HU-03).

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Partición válida | Carrito sin claves | {}, Cuaderno, 10.000, 2 | items {Cuaderno: 2}, total 20.000 | test_agregar_producto_valido_suma_total[R1-carrito-sin-claves] |
| Partición válida | Producto nuevo en carrito con items | Cuaderno 1 + Regla 1.500 x 1 | total 11.500 | test_agregar_producto_valido_suma_total[R1-producto-nuevo] |
| Partición válida | Producto que ya estaba | Cuaderno 1 + Cuaderno 10.000 x 2 | Cuaderno 3, total 30.000 | test_agregar_producto_valido_suma_total[R1-producto-existente] |
| Partición válida | Decimales (HU-05) | Café de Huila 1.499,90 x 3 | total 4.499,70 (approx) | test_agregar_producto_valido_suma_total[R1-decimales] |
| Partición válida | Catálogo sintético | 5 productos | total 49.200,70 (approx) | test_catalogo_sintetico_suma_total_y_conserva_nombres |

**Ambigüedades encontradas:** el orden en que se revisan los errores. El cliente
no dijo qué hacer si hay varios errores a la vez. Decidí la prioridad producto,
luego precio, luego cantidad (el orden de los argumentos). Si esa decisión cambia,
la tabla de decisión cambia con ella.

**Tabla de decisión.** Con 3 condiciones (producto válido: sí/no; precio:
disponible y válido / None / inválido; cantidad: válida / negativa / cero) hay 18
combinaciones. Con la prioridad producto > precio > cantidad se simplifican a 6
reglas; «–» significa que la condición no importa.

| Regla | Producto válido | Precio | Cantidad | Resultado esperado | Prueba que lo cubre |
|---|---|---|---|---|---|
| R1 | Sí | Válido | Válida | Carrito nuevo con total actualizado | test_agregar_producto_valido_suma_total[R1-*] |
| R2 | No | – | – | ValueError por producto vacío; carrito intacto | test_error_lanza_el_tipo_correcto_y_no_modifica_el_carrito[R2-producto-vacio], [R2-producto-gana-a-todo] |
| R3 | Sí | None | – | PrecioNoDisponibleError; carrito intacto | ...[R3-sin-precio], [R3-sin-precio-gana-a-cantidad] |
| R4 | Sí | Inválido | – | ValueError por precio; carrito intacto | ...[R4-precio-negativo], [R4-precio-gana-a-cantidad] |
| R5 | Sí | Válido | Negativa | ValueError «no puede ser negativa»; carrito intacto | ...[R5-cantidad-negativa] |
| R6 | Sí | Válido | Cero | ValueError «debe ser mayor a cero»; carrito intacto | ...[R6-cantidad-cero] |

Las filas «gana-a-todo» y «gana-a-cantidad» comprueban la simplificación: dos
condiciones inválidas a la vez producen el error de la condición de mayor
prioridad.

## 2. Pruebas de la IA descartadas o corregidas

**Prompt usado:** [PEGA AQUÍ EL PROMPT QUE USASTE O UN RESUMEN FIEL, Y ENLAZA LA
ENTRADA DE LA BITÁCORA]

| Prueba generada | Decisión | Por qué | En su lugar |
|---|---|---|---|
| test_agregar_producto_error_negativo (semana 5): esperaba «La cantidad debe ser mayor a cero» con -2 | Corregida | El esperado salió del código, no de la regla. HU-01 escenario 2 pide «La cantidad no puede ser negativa» | Esperado «La cantidad no puede ser negativa» (commit 8b9fb2f, antes de tocar el código) |
| test_agregar_producto_inmutabilidad_en_error (semana 5): mismo esperado con -2 | Corregida | Mismo defecto: el esperado salió del código | Mismo texto del cliente (commit 8b9fb2f) |
| | | | |

**Decisión:** Conservada, Corregida o Descartada.

## 3. Romper el código a propósito

| Cambio introducido | Archivo y línea | ¿Alguna prueba falló? | Qué hice |
|---|---|---|---|
| | | | |

## 4. Datos de prueba

**Origen:** sintéticos generados con IA (Claude) y revisados por mí. Confirmo que
no hay datos de personas reales.

**Casos difíciles incluidos:** tilde («Lápiz», «Café»), ñ y Ñ («Piña oro», «Ñame
criollo»), apóstrofo («Panela D'Lujo»), punto dentro del nombre («Lápiz No. 2»),
decimales con centavos (4.500,50 y 3.999,90, que no son exactos en binario),
cantidad en el límite (1), texto vacío y solo espacios, precio y cantidad en cero,
`nan` e infinito, y tipos equivocados. Contexto local: productos y precios en
pesos colombianos de una tienda escolar y de mercado. Los datos están en el
fixture `catalogo_sintetico` de `tests/conftest.py`.
