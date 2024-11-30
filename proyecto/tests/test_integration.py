import pytest
from unittest.mock import patch
from decimal import Decimal
from classes.account_manager import AccountManager
from classes.transaction_manager import TransactionManager
from classes.currency_manager import CurrencyManager
from unittest.mock import patch

@pytest.fixture
def mock_database_connection():
    with patch('config.database.Database.get_connection') as mock_connection:
        mock_cursor = mock_connection.return_value.cursor.return_value
        mock_cursor.execute.return_value = None
        yield mock_connection
def test_complete_transaction_flow(mock_database_connection):
    # Simula la obtención de balances
        with patch('classes.currency_manager.CurrencyManager.convert_currency', return_value=(Decimal("0.92"), Decimal("92.00"))):
            result = TransactionManager.register_transaction(1, "USD", "EUR", Decimal("100.00"), Decimal("0.92"), Decimal("92.00"))
            assert result is True
            # Simula la actualización de balances
            with patch('classes.account_manager.AccountManager.update_balances') as mock_update_balances:
                mock_update_balances.return_value = True
                result = AccountManager.update_balances(1, "USD", "EUR", Decimal("100.00"), Decimal("92.00"))
                assert result is True
                # Verifica que se hayan realizado las actualizaciones correctamente
                mock_cursor = mock_database_connection.return_value.cursor.return_value
                # Verificar la inserción de la transacción
                mock_cursor.execute.assert_any_call(
                    'INSERT INTO Transactions (UserId, FromCurrency, ToCurrency, Amount, Rate, Result, TransactionDate) VALUES (?, ?, ?, ?, ?, ?, ?)',        
                    1, 'USD', 'EUR', Decimal('100.00'), Decimal('0.92'), Decimal('92.00'),
                    TransactionManager.fecha
                )

'''
def test_transaction_with_insufficient_funds(mock_database_connection):
    # Simulamos el comportamiento de la base de datos
    mock_cursor = mock_database_connection.return_value.cursor.return_value
    mock_cursor.fetchone.side_effect = [Decimal("50.00"), Decimal("500.00")]  # Saldo insuficiente

    # Simula la conversión de moneda
    with patch('classes.currency_manager.CurrencyManager.convert_currency', return_value=(Decimal("0.9"), Decimal("90.00"))):
        result = TransactionManager.register_transaction(1, "USD", "EUR", Decimal("100.00"), Decimal("0.9"), Decimal("90.00"))
        assert result is False  # No se debería registrar la transacción
'''

def test_get_user_transactions_after_transaction(mock_database_connection):
    # Simula el registro de una transacción
    with patch('classes.transaction_manager.TransactionManager.register_transaction', return_value=True):
        TransactionManager.register_transaction(1, "USD", "EUR", Decimal("100.00"), Decimal("0.9"), Decimal("90.00"))

    # Simula que se obtienen las transacciones
    mock_cursor = mock_database_connection.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [
        (1, 1, "USD", "EUR", 100.00, 0.9, 90.00, "2024-01-01 12:00:00")
    ]
    
    transactions = TransactionManager.get_user_transactions(1)
    assert len(transactions) == 1
    assert transactions[0][2] == "USD"  # Verifica que la divisa de origen es correcta