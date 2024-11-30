Feature: Gestión de cuentas
  Descripción: Permite a los usuarios crear, eliminar y consultar cuentas.

  Scenario: Crear una cuenta exitosa
    Given un usuario sin cuenta registrada
    When el usuario proporciona los datos válidos para la cuenta
    Then la cuenta se crea exitosamente

  Scenario: Intentar crear una cuenta sin datos válidos
    Given un usuario intenta registrar una cuenta
    When el usuario no completa todos los campos requeridos
    Then se muestra un error indicando datos faltantes

  Scenario: Consultar el saldo de una cuenta existente
    Given un usuario con una cuenta registrada
    When el usuario consulta el saldo de su cuenta
    Then se muestra el saldo actual

  Scenario: Consultar el saldo de una cuenta inexistente
    Given un usuario sin cuentas registradas
    When el usuario intenta consultar el saldo
    Then se muestra un mensaje indicando que no existen cuentas
