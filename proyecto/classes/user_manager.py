from config.database import Database

class UserManager:
    @staticmethod
    def verify_credentials(username, password):
        try:
            conn = Database.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT UserId, Username, PasswordHash FROM Users WHERE Username = ?", username)
            user = cursor.fetchone()
            
            if user and password == user.PasswordHash:
                return user
            return None
            
        finally:
            if 'cursor' in locals() and cursor is not None:
                cursor.close()
            if 'conn' in locals() and conn is not None:
                conn.close()