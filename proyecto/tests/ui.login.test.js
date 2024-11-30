// ui.login.test.js
const { test, expect } = require('@playwright/test');

test('intentar iniciar sesión con credenciales inválidas', async ({ page }) => {
    await page.goto('http://localhost:5000');

    // Llenar el formulario con credenciales inválidas
    await page.fill('input[name="username"]', 'usuario_invalido');
    await page.fill('input[name="password"]', 'contraseña_invalida');

    // Hacer clic en el botón de inicio de sesión
    await page.click('button[type="submit"]');

    // Verificar que se muestre un mensaje de error
    const errorMessage = await page.locator('.alert-danger'); // Selecciona el mensaje de error
    await expect(errorMessage).toBeVisible();
});