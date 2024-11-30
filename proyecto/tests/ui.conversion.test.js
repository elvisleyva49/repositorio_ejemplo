const { test, expect } = require('@playwright/test');

test.describe('Pruebas de Conversión', () => {

    test('mostrar advertencia al enviar formulario vacío', async ({ page }) => {
        await page.goto('http://localhost:5000/conversion');
        await page.waitForTimeout(1000); // Espera después de cargar la página

        // Hacer clic en el botón de convertir sin llenar el formulario
        await page.click('button[type="submit"]');
        await page.waitForTimeout(1500); // Espera para que el mensaje de advertencia aparezca

        // Verificar el mensaje de advertencia en el campo "Monto"
        const montoInput = page.locator('input[name="monto"]');
        const isInvalid = await montoInput.evaluate((input) => input.validity.valueMissing);
        expect(isInvalid).toBeTruthy(); // Verifica que el campo "Monto" tiene el estado de valor faltante

        // Verificar que el campo tiene el foco
        const isFocused = await montoInput.evaluate((input) => document.activeElement === input);
        expect(isFocused).toBeTruthy();
    });

    test('no permitir envío con monto negativo', async ({ page }) => {
        await page.goto('http://localhost:5000/conversion');
        await page.waitForTimeout(1000); // Espera después de cargar la página

        // Introducir un monto negativo
        await page.fill('input[name="monto"]', '-100');
        await page.waitForTimeout(500); // Espera después de rellenar el campo
        await page.selectOption('select[name="divisa_origen"]', 'USD');
        await page.waitForTimeout(500); // Espera después de seleccionar la divisa de origen
        await page.selectOption('select[name="divisa_destino"]', 'EUR');
        await page.waitForTimeout(500); // Espera después de seleccionar la divisa de destino

        // Hacer clic en el botón de convertir
        await page.click('button[type="submit"]');
        await page.waitForTimeout(1500); // Espera después del clic para verificar los resultados

        // Verificar que el formulario no se envía
        await expect(page).toHaveURL('http://localhost:5000/conversion'); // Verifica que sigue en la misma página
    });

    test('enviar formulario con datos válidos', async ({ page }) => {
        await page.goto('http://localhost:5000/conversion');
        await page.waitForTimeout(1000); // Espera después de cargar la página

        // Llenar el formulario con datos válidos
        await page.fill('input[name="monto"]', '100');
        await page.waitForTimeout(500); // Espera después de rellenar el campo
        await page.selectOption('select[name="divisa_origen"]', 'USD');
        await page.waitForTimeout(500); // Espera después de seleccionar la divisa de origen
        await page.selectOption('select[name="divisa_destino"]', 'EUR');
        await page.waitForTimeout(500); // Espera después de seleccionar la divisa de destino

        // Hacer clic en el botón de convertir
        await page.click('button[type="submit"]');
        await page.waitForTimeout(1500); // Espera después del clic para verificar los resultados

        // Verificar que la conversión se realizó
        await expect(page).toHaveURL('http://localhost:5000/conversion'); // Ajusta la URL si es necesario
    });

    test('mostrar mensaje de error por valor inválido en el campo "Monto"', async ({ page }) => {
        await page.goto('http://localhost:5000/conversion');
        await page.waitForTimeout(1000); // Espera después de cargar la página

        // Seleccionar el campo "Monto"
        const montoInput = page.locator('input[name="monto"]');
        await page.waitForTimeout(500); // Espera antes de rellenar el campo

        // Asignar un valor inválido directamente al elemento
        await montoInput.evaluate((input) => input.value = '4366345.34543512--34');
        await page.waitForTimeout(500); // Espera después de asignar el valor inválido

        // Intentar enviar el formulario
        await page.click('button[type="submit"]');
        await page.waitForTimeout(1500); // Espera después del clic para verificar los resultados

        // Verificar que el campo tiene un error de tipo inválido
        const isInvalid = await montoInput.evaluate((input) => !input.checkValidity());
        expect(isInvalid).toBeTruthy();

        // Verificar el mensaje de validación nativo
        const validationMessage = await montoInput.evaluate((input) => input.validationMessage);
        expect(validationMessage).not.toBe('');
    });
});
