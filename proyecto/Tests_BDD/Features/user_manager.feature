Feature: Gestión de usuarios
  Descripción: Permite a los usuarios registrarse, iniciar sesión y actualizar sus datos.

  Scenario: Registrar un usuario exitosamente
    Given un usuario no registrado
    When proporciona datos válidos
    Then el usuario se registra exitosamente

  Scenario: Intentar registrar un usuario con datos incompletos
    Given un usuario no registrado
    When proporciona datos incompletos
    Then se muestra un mensaje indicando los campos requeridos

  Scenario: Iniciar sesión exitosamente
    Given un usuario con credenciales válidas
    When ingresa su nombre de usuario y contraseña correctos
    Then accede al sistema correctamente

  Scenario: Intentar iniciar sesión con credenciales incorrectas
    Given un usuario con credenciales inválidas
    When intenta iniciar sesión
    Then se muestra un mensaje de error indicando credenciales incorrectas

  Scenario: Actualizar información de usuario
    Given un usuario registrado
    When actualiza su dirección de correo electrónico
    Then los cambios se guardan exitosamente
