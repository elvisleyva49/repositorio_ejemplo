import pyodbc

class Database:
    @staticmethod
    def get_connection():
        connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=.;"
            "DATABASE=CasaDeCambioDBTest;"
            "UID=sa;"
            "PWD=sa"
        )
        return pyodbc.connect(connection_string)

    @staticmethod
    def conversion_rates():
        return {
            'USD': {
                'EUR': 0.92,
                'PEN': 3.70
            },
            'EUR': {
                'USD': 1.09,
                'PEN': 4.02
            },
            'PEN': {
                'USD': 0.27,
                'EUR': 0.25
            }
        }