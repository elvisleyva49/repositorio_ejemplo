def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"login" in response.data  # Verifica si el texto 'login' está presente

def test_login(client, mocker):
    # Crear un objeto mock para simular la respuesta de la base de datos
    class MockUser:
        def __init__(self, user_id, username, password_hash):
            self.UserId = user_id
            self.Username = username
            self.PasswordHash = password_hash

    # Crear el objeto mock que representa un usuario con un PasswordHash
    mock_user = MockUser(1, 'admin', 'admin123')  # Contraseña simulada

    # Mockear la consulta a la base de datos para devolver el mock de usuario
    mock_cursor = mocker.patch('pyodbc.connect')
    mock_cursor.return_value.cursor.return_value.fetchone.return_value = mock_user

    # Datos del formulario de login
    data = {'username': 'admin', 'password': 'admin123'}
    response = client.post('/login', data=data)

    # Imprimir la URL de redirección para depuración
    print("Redirección a:", response.location)

    # Aserciones
    assert response.status_code == 302  # Redirección esperada
    assert response.location.endswith('/dashboard')  # Redirige a dashboard

