import pytest
from unittest.mock import patch
from datetime import datetime
from classes.transaction_manager import TransactionManager
from config.database import Database

@pytest.fixture
def mock_database_connection():
    with patch.object(Database, 'get_connection') as mock_connection:
        mock_cursor = mock_connection.return_value.cursor.return_value
        mock_cursor.execute.return_value = None
        mock_connection.return_value.commit.return_value = None
        yield mock_connection

def test_register_transaction_success(mock_database_connection):#Prueba que el registro de una transacción se realice correctamente.
    result = TransactionManager.register_transaction(
        1, "USD", "EUR", 100.00, 0.9, 90.00
    )
    assert result is True

#Prueba que el método maneja correctamente los errores de base de datos durante el registro de una transacción.
def test_register_transaction_database_error(mock_database_connection):
    mock_database_connection.side_effect = Exception("Error de base de datos")
    result = TransactionManager.register_transaction(1, "USD", "EUR", 100.00, 0.9, 90.00)
    assert "error" in result
    assert result["error"] == "Error de base de datos"
#Prueba que la obtención de transacciones de un usuario se realice correctamente.
def test_get_user_transactions_success(mock_database_connection):
    mock_cursor = mock_database_connection.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [
        (1, 1, "USD", "EUR", 100.00, 0.9, 90.00, datetime.now()),
        (2, 1, "EUR", "JPY", 200.00, 123.0, 24600.00, datetime.now())
    ]
    transactions = TransactionManager.get_user_transactions(1)
    assert len(transactions) == 2

#Prueba que el método maneja correctamente los errores de base de datos durante la obtención de transacciones de un usuario.
def test_get_user_transactions_database_error(mock_database_connection):
    mock_database_connection.side_effect = Exception("Error de base de datos")
    transactions = TransactionManager.get_user_transactions(1)
    assert "error" in transactions
    assert transactions["error"] == "Error de base de datos"