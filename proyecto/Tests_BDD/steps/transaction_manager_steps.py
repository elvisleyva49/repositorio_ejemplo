from behave import given, when, then

# Simulación de cuentas y saldos
accounts = {
    "user1": {"balance": 1000},  # Usuario con cuenta activa y saldo inicial de 1000
    "user2": {"balance": 300},   # Usuario con saldo de 300
}

@given(u'un usuario tiene una cuenta activa')
def step_impl(context):
    # Asegurarse de que el usuario tiene una cuenta activa (por ejemplo, user1)
    context.user = "user1"


@given(u'un usuario tiene 1000 en su cuenta')
def step_impl(context):
    # Asegurarse de que el usuario tiene un saldo de 1000
    context.user = "user1"
    accounts[context.user] = {"balance": 1000}

@given(u'un usuario tiene 300 en su cuenta')
def step_impl(context):
    # Asegurarse de que el usuario tiene un saldo de 300
    context.user = "user2"
    accounts[context.user] = {"balance": 300}

@when(u'el usuario deposita 500 en su cuenta')
def step_impl(context):
    # Registrar un depósito de 500 en la cuenta del usuario
    if context.user in accounts:
        accounts[context.user]["balance"] += 500
        context.result = "Depósito exitoso"
    else:
        context.result = "Cuenta inexistente"

@when(u'intenta depositar 500')
def step_impl(context):
    # Intentar depositar en una cuenta inexistente
    if context.user in accounts:
        accounts[context.user]["balance"] += 500
        context.result = "Depósito exitoso"
    else:
        context.result = "Cuenta inexistente"

@when(u'el usuario retira 200')
def step_impl(context):
    # Registrar un retiro de 200 en la cuenta del usuario
    if context.user in accounts and accounts[context.user]["balance"] >= 200:
        accounts[context.user]["balance"] -= 200
        context.result = "Retiro exitoso"
    else:
        context.result = "Fondos insuficientes"

@when(u'intenta retirar 500')
def step_impl(context):
    # Intentar retirar más de lo disponible en la cuenta
    if context.user in accounts and accounts[context.user]["balance"] >= 500:
        accounts[context.user]["balance"] -= 500
        context.result = "Retiro exitoso"
    else:
        context.result = "Fondos insuficientes"

@then(u'el saldo de la cuenta aumenta en 500')
def step_impl(context):
    # Verificar que el saldo ha aumentado en 500
    assert accounts[context.user]["balance"] == 1500  # Saldo inicial + 500

@then(u'se muestra un mensaje de error indicando cuenta inexistente')
def step_impl(context):
    # Verificar que el mensaje de error sea el esperado
    assert context.result == "Cuenta inexistente"

@then(u'el saldo disminuye en 200')
def step_impl(context):
    # Verificar que el saldo ha disminuido en 200
    assert accounts[context.user]["balance"] == 800  # Saldo inicial - 200

@then(u'se muestra un mensaje indicando fondos insuficientes')
def step_impl(context):
    # Verificar que se muestre el mensaje de fondos insuficientes
    assert context.result == "Fondos insuficientes"
