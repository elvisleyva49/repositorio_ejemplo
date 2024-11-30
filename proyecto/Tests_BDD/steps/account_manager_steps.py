from behave import given, when, then

# Crear una lista global para simular las cuentas del usuario
accounts = []

@given(u'un usuario sin cuenta registrada')
def step_impl(context):
    # El usuario no tiene cuentas registradas
    accounts.clear()  # Limpiar cualquier cuenta previamente registrada

@given(u'un usuario intenta registrar una cuenta')
def step_impl(context):
    # El usuario intenta registrar una cuenta, pero no tiene cuenta registrada aún
    accounts.clear()  # Asegurarse de que no haya cuentas

@given(u'un usuario con una cuenta registrada')
def step_impl(context):
    # El usuario tiene una cuenta registrada
    accounts.clear()  # Limpiar cualquier cuenta previamente registrada
    accounts.append({"name": "Cuenta de ejemplo", "email": "usuario@example.com", "balance": 1000})

@given(u'un usuario sin cuentas registradas')
def step_impl(context):
    # El usuario no tiene cuentas registradas
    accounts.clear()

@when(u'el usuario proporciona los datos válidos para la cuenta')
def step_impl(context):
    # Simular la creación de una cuenta con datos válidos
    context.account = {"name": "Cuenta válida", "email": "usuario@dominio.com", "balance": 1000}
    accounts.append(context.account)  # Añadir la cuenta a la lista

@when(u'el usuario no completa todos los campos requeridos')
def step_impl(context):
    # Simular el intento de crear una cuenta sin los datos completos
    context.error = "Error: Campos incompletos"
    context.account = {"name": "", "email": ""}
    if not context.account["name"] or not context.account["email"]:
        context.error = "Error: Campos incompletos"

@when(u'el usuario consulta el saldo de su cuenta')
def step_impl(context):
    # Simular la consulta del saldo de la cuenta registrada
    context.balance = None
    for account in accounts:
        if account["name"] == "Cuenta de ejemplo":
            context.balance = account["balance"]

@when(u'el usuario intenta consultar el saldo')
def step_impl(context):
    # Intentar consultar el saldo sin cuentas registradas
    context.error_message = None
    if not accounts:
        context.error_message = "Error: No existen cuentas registradas"

@then(u'la cuenta se crea exitosamente')
def step_impl(context):
    # Verificar que la cuenta se haya creado correctamente
    assert context.account is not None
    assert context.account["name"] == "Cuenta válida"
    assert context.account["email"] == "usuario@dominio.com"
    assert context.account["balance"] == 1000

@then(u'se muestra un error indicando datos faltantes')
def step_impl(context):
    # Verificar que se haya mostrado un error debido a la falta de datos
    assert context.error == "Error: Campos incompletos"

@then(u'se muestra el saldo actual')
def step_impl(context):
    # Verificar que el saldo de la cuenta se muestre correctamente
    assert context.balance == 1000  # El saldo de la cuenta 'Cuenta de ejemplo' es 1000

@then(u'se muestra un mensaje indicando que no existen cuentas')
def step_impl(context):
    # Verificar que se muestra un mensaje de error cuando no hay cuentas
    assert context.error_message == "Error: No existen cuentas registradas"
