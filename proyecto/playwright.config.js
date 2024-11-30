const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
    testDir: './tests', // Tu directorio de pruebas
    use: {
        slowMo: 4000, // Ralentiza la ejecución en 4000 ms por acción
        video: 'on', // Habilita la grabación de video para todas las pruebas
        trace: 'on-first-retry', // Habilita el trazado en el primer reintento
        coverage: {
            // Configuración de cobertura
            report: ['text', 'html'],
            output: './COO/coverage',
        },
    },
    reporter: [
        ['html', { outputFolder: 'test-results/html-report', open: 'never' }], // Genera el reporte HTML
        ['list'], // Muestra un resumen en la consola
    ],
    globalSetup: './global-setup.js', // Archivo de configuración global
});