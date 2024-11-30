// ui.cotizar.test.js
const { test, expect } = require('@playwright/test');

test('cargar la página de cotización correctamente', async ({ page }) => {
    await page.goto('http://localhost:5000/cotizar'); // Asegúrate de que el servidor esté corriendo

    // Verificar que el título esté presente
    const title = await page.locator('h2.text-center'); // Ajusta según tu HTML
    await expect(title).toHaveText('Cotizar Conversión');

    // Verificar que el formulario esté visible
    const form = await page.locator('form');
    await expect(form).toBeVisible();
});

test('cotizar una conversión con datos válidos', async ({ page }) => {
    await page.goto('http://localhost:5000/cotizar');

    // Llenar el formulario con datos válidos
    await page.fill('input[name="monto"]', '100'); // Monto a convertir
    await page.selectOption('select[name="divisa_origen"]', 'USD'); // Divisa original
    await page.selectOption('select[name="divisa_destino"]', 'EUR'); // Divisa a convertir

    // Hacer clic en el botón de cotizar
    await page.click('button[type="submit"]');

    // Verificar que se muestre el resultado de la cotización
    const montoOriginal = await page.locator('p:has-text("Monto Original:")'); 
    await expect(montoOriginal).toBeVisible();
    await expect(montoOriginal).toContainText('100.0 USD'); // Ajusta según lo que se muestra

    const divisaDestino = await page.locator('p:has-text("Divisa a Convertir:")'); 
    await expect(divisaDestino).toBeVisible();
    await expect(divisaDestino).toContainText('EUR'); // Verifica que sea la divisa esperada

    const montoConvertido = await page.locator('p:has-text("Monto Convertido:")'); 
    await expect(montoConvertido).toBeVisible();
    await expect(montoConvertido).toContainText('92.00 EUR'); // Ajusta según el valor que se espera
});

test('mostrar advertencia al enviar formulario vacío', async ({ page }) => {
    await page.goto('http://localhost:5000/cotizar');

    // Hacer clic en el botón de cotizar sin llenar el formulario
    await page.click('button[type="submit"]');

    // Esperar que el navegador muestre un error de validación en el campo "Monto"
    const montoInput = page.locator('input[name="monto"]');
    const isInvalid = await montoInput.evaluate((input) => input.validity.valueMissing);
    expect(isInvalid).toBeTruthy(); // Verifica que el campo "Monto" tiene el estado de valor faltante

    // También puedes verificar el foco en el campo que falló la validación
    const isFocused = await montoInput.evaluate((input) => document.activeElement === input);
    expect(isFocused).toBeTruthy(); // Verifica que el campo "Monto" tiene el foco
});