from config.database import Database
from decimal import Decimal

class AccountManager:
    def get_account_balances(user_id):
        conn = None
        cursor = None
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT BalanceUSD, BalanceEUR, BalancePEN FROM Accounts WHERE UserId = ?",
                (user_id,)
            )
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener los balances: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()


    @staticmethod
    def update_balances(user_id, divisa_origen, divisa_destino, monto, monto_convertido):
        try:
            print(f"Iniciando actualización de balances para UserId: {user_id}")
            print(f"Divisa origen: {divisa_origen}, Divisa destino: {divisa_destino}, Monto: {monto}, Monto convertido: {monto_convertido}")
            
            conn = Database.get_connection()
            cursor = conn.cursor()
            print("Conexión a la base de datos establecida correctamente.")

            # Obtener el balance de la divisa de origen
            print(f"Obteniendo balance de {divisa_origen}...")
            cursor.execute(f"SELECT Balance{divisa_origen} FROM Accounts WHERE UserId = ?", (user_id,))
            balance_origen = cursor.fetchone()
            print(f"Resultado de balance de {divisa_origen}: {balance_origen}")
            
            if balance_origen is None:
                print("No se encontró el balance de la divisa de origen.")
                raise ValueError("No se encontró la cuenta del usuario.")
            
            balance_origen = Decimal(balance_origen[0])
            print(f"Balance de origen convertido a Decimal: {balance_origen}")

            if balance_origen >= monto:
                nuevo_balance_origen = balance_origen - monto
                print(f"Nuevo balance de {divisa_origen}: {nuevo_balance_origen}")
                
                # Actualiza el balance de la divisa de origen
                cursor.execute(f"UPDATE Accounts SET Balance{divisa_origen} = ? WHERE UserId = ?", 
                            (nuevo_balance_origen, user_id))
                print(f"Balance de {divisa_origen} actualizado en la base de datos.")

                # Obtener el balance de la divisa de destino
                print(f"Obteniendo balance de {divisa_destino}...")
                cursor.execute(f"SELECT Balance{divisa_destino} FROM Accounts WHERE UserId = ?", (user_id,))
                balance_destino = cursor.fetchone()
                print(f"Resultado de balance de {divisa_destino}: {balance_destino}")
                
                if balance_destino is None:
                    print("No se encontró el balance de la divisa de destino.")
                    raise ValueError("No se encontró la cuenta de destino.")

                balance_destino = Decimal(balance_destino[0])
                print(f"Balance de destino convertido a Decimal: {balance_destino}")

                nuevo_balance_destino = balance_destino + monto_convertido
                print(f"Nuevo balance de {divisa_destino}: {nuevo_balance_destino}")

                # Actualiza el balance de la divisa de destino
                cursor.execute(f"UPDATE Accounts SET Balance{divisa_destino} = ? WHERE UserId = ?", 
                            (nuevo_balance_destino, user_id))
                print(f"Balance de {divisa_destino} actualizado en la base de datos.")

                conn.commit()
                print("Transacción confirmada (commit).")
                return True

            print("El balance de origen no es suficiente para realizar la transacción.")
            return False

        except Exception as e:
            print(f"Error encontrado: {e}")
            return {"error": str(e)}

        finally:
            print("Cerrando recursos...")
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
                print("Cursor cerrado.")
            if 'conn' in locals() and conn is not None:
                conn.close()
                print("Conexión cerrada.")
