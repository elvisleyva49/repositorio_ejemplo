Feature: Gestión de monedas
  Descripción: Permite a los usuarios consultar y convertir monedas.

  Scenario: Consultar el tipo de cambio de una moneda válida
    Given el sistema tiene acceso a tipos de cambio actualizados
    When el usuario consulta el tipo de cambio de USD a EUR
    Then se muestra el tipo de cambio actual

  Scenario: Intentar consultar el tipo de cambio de una moneda inexistente
    Given el sistema no tiene registro de la moneda XYZ
    When el usuario consulta el tipo de cambio de XYZ
    Then se muestra un mensaje de error indicando moneda desconocida

  Scenario: Consultar el tipo de cambio de EUR a USD
      Given el sistema tiene acceso a tipos de cambio actualizados
      When el usuario consulta el tipo de cambio de EUR a USD
      Then se muestra el tipo de cambio actual