from behave import given, when, then

# Given un usuario no registrado
@given(u'un usuario no registrado')
def step_impl(context):
    context.user_registered = False

# When proporciona datos válidos
@when(u'proporciona datos válidos')
def step_impl(context):
    # Lógica para registrar un usuario
    context.user_registered = True

# Then el usuario se registra exitosamente
@then(u'el usuario se registra exitosamente')
def step_impl(context):
    assert context.user_registered is True

# When proporciona datos incompletos
@when(u'proporciona datos incompletos')
def step_impl(context):
    # Lógica para manejar datos incompletos
    context.error_message = "Campos requeridos"

# Then se muestra un mensaje indicando los campos requeridos
@then(u'se muestra un mensaje indicando los campos requeridos')
def step_impl(context):
    assert context.error_message == "Campos requeridos"

# Given un usuario con credenciales válidas
@given(u'un usuario con credenciales válidas')
def step_impl(context):
    context.username = "valid_user"
    context.password = "valid_password"
    context.user_credentials_valid = True

# When ingresa su nombre de usuario y contraseña correctos
@when(u'ingresa su nombre de usuario y contraseña correctos')
def step_impl(context):
    # Lógica para iniciar sesión
    if context.user_credentials_valid:
        context.logged_in = True

# Then accede al sistema correctamente
@then(u'accede al sistema correctamente')
def step_impl(context):
    assert context.logged_in is True

# Given un usuario con credenciales inválidas
@given(u'un usuario con credenciales inválidas')
def step_impl(context):
    context.username = "invalid_user"
    context.password = "wrong_password"
    context.user_credentials_valid = False

# When intenta iniciar sesión
@when(u'intenta iniciar sesión')
def step_impl(context):
    # Lógica para manejar credenciales incorrectas
    if not context.user_credentials_valid:
        context.login_result = "Credenciales incorrectas"

# Then se muestra un mensaje de error indicando credenciales incorrectas
@then(u'se muestra un mensaje de error indicando credenciales incorrectas')
def step_impl(context):
    assert context.login_result == "Credenciales incorrectas"

# Given un usuario registrado
@given(u'un usuario registrado')
def step_impl(context):
    context.username = "existing_user"
    context.email = "user@example.com"
    context.password = "securepassword"
    context.updated_user = context

# When actualiza su dirección de correo electrónico
@when(u'actualiza su dirección de correo electrónico')
def step_impl(context):
    context.new_email = "newemail@example.com"
    context.updated_user.email = context.new_email

# Then los cambios se guardan exitosamente
@then(u'los cambios se guardan exitosamente')
def step_impl(context):
    assert context.updated_user.email == context.new_email
