from behave import given, when, then

# Simulación de tipos de cambio en un diccionario
exchange_rates = {
    "USD": {"EUR": 0.85},
    "EUR": {"USD": 1.18}
}

@given(u'el sistema tiene acceso a tipos de cambio actualizados')
def step_impl(context):
    # Asegurarse de que el sistema tenga tipos de cambio actualizados
    context.exchange_rates = exchange_rates

@given(u'el sistema no tiene registro de la moneda XYZ')
def step_impl(context):
    # No hay datos para la moneda 'XYZ'
    context.exchange_rates = {}

@when(u'el usuario consulta el tipo de cambio de USD a EUR')
def step_impl(context):
    # Realizar la consulta del tipo de cambio de USD a EUR
    context.result = context.exchange_rates.get("USD", {}).get("EUR", "Tipo de cambio no disponible")

@when(u'el usuario consulta el tipo de cambio de XYZ')
def step_impl(context):
    # Intentar consultar el tipo de cambio de una moneda no registrada
    context.result = context.exchange_rates.get("XYZ", {}).get("EUR", "Tipo de cambio no disponible")

@when(u'el usuario consulta el tipo de cambio de EUR a USD')
def step_impl(context):
    # Realizar la consulta del tipo de cambio de EUR a USD
    context.result = context.exchange_rates.get("EUR", {}).get("USD", "Tipo de cambio no disponible")

@then(u'se muestra el tipo de cambio actual')
def step_impl(context):
    # Verificar que se haya mostrado el tipo de cambio
    assert context.result != "Tipo de cambio no disponible"

@then(u'se muestra un mensaje de error indicando moneda desconocida')
def step_impl(context):
    # Verificar que se muestre un mensaje de error si la moneda es desconocida
    assert context.result == "Tipo de cambio no disponible"
