from config.database import Database
from datetime import datetime
from datetime import datetime

class TransactionManager:
    @staticmethod
    def register_transaction(user_id, divisa_origen, divisa_destino, monto, tasa_conversion, monto_convertido):
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            TransactionManager.fecha = datetime.now()
            fecha = TransactionManager.fecha
            cursor.execute("""INSERT INTO Transactions (UserId, FromCurrency, ToCurrency, Amount, Rate, Result, TransactionDate) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                user_id, divisa_origen, divisa_destino, monto, tasa_conversion, 
                monto_convertido, fecha)
            
            conn.commit()
            return True
            
        except Exception as e:
            # Manejo de excepciones: devolver un mensaje de error
            return {"error": str(e)}
        
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'conn' in locals() and conn is not None:
                conn.close()

    @staticmethod
    def get_user_transactions(user_id):
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Transactions WHERE UserId = ? ORDER BY TransactionDate DESC", (user_id,))
            return cursor.fetchall()
        
        except Exception as e:
            # Manejo de excepciones: devolver un mensaje de error
            return {"error": str(e)}
        
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'conn' in locals() and conn is not None:
                conn.close()