Feature: Gestión de transacciones
  Descripción: Permite registrar depósitos, retiros y transferencias entre cuentas.

  Scenario: Registrar un depósito en una cuenta existente
    Given un usuario tiene una cuenta activa
    When el usuario deposita 500 en su cuenta
    Then el saldo de la cuenta aumenta en 500

  Scenario: Registrar un retiro exitoso
    Given un usuario tiene 1000 en su cuenta
    When el usuario retira 200
    Then el saldo disminuye en 200

  Scenario: Intentar registrar un retiro mayor al saldo disponible
    Given un usuario tiene 300 en su cuenta
    When intenta retirar 500
    Then se muestra un mensaje indicando fondos insuficientes
