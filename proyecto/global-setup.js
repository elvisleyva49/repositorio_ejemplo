// global-setup.js
const { chromium } = require('playwright');

module.exports = async () => {
    const browser = await chromium.launch();
    const context = await browser.newContext();
    await context.tracing.start({ screenshots: true, snapshots: true });
    await browser.close();
};