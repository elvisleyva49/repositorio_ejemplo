# Despliegue y Automatización

## Despliegue

1. Primero abrimos cmd dentro del proyecto:
    ```bash
    az login -u direccion_correo@upt.pe
    ```

2. Creamos un grupo correspondiente de recursos:
    ```bash
    az group create --name GRUPO1 --location eastus
    ```

3. Creamos un plan de servicio gratuito:
    ```bash
    az appservice plan create -g GRUPO1 -n casadecambio --is-linux --sku F1
    ```

4. Desplegamos con el siguiente comando:
    ```bash
    az webapp up -n casadecambio -g GRUPO1 --runtime "PYTHON|3.9"
    ```

5. Una vez terminado este proceso, ejecutaremos un log:
    ```bash
    az webapp log tail -n casadecambio -g GRUPO1
    ```

6. Esto con el fin de que nos proporcione la IP del despliegue. Luego, nos vamos a nuestra base de datos en Azure y en el apartado de Seguridad, ingresamos esta IP para darle los permisos necesarios y que pueda funcionar correctamente.

## Implementación en GitHub y Despliegue Automatizado

1. En el terminal, ejecutaremos el siguiente comando para obtener el perfil público (Publish Profile) de nuestra aplicación web:
    ```bash
    az webapp deployment list-publishing-profiles --name casadecambio --resource-group GRUPO1 --xml
    ```

2. Abriremos en un navegador el repositorio en GitHub, nos ubicamos en la sección `Settings`, buscamos la opción `Secrets and Variables` y seleccionamos la opción `Actions`. Dentro de esta haremos click en el botón `New Repository Secret`.

3. Dentro de la ventana `New Secret`, colocaremos como nombre `AZURE_WEBAPP_PUBLISH_PROFILE` y como valor el perfil público que obtuvimos.

4. Dentro de la raíz de nuestro proyecto, creamos un archivo llamado `ci-cd.yml` con el siguiente contenido:

    ```yaml
    name: Construcción y despliegue de una aplicación Python a Azure

    env:
      AZURE_WEBAPP_NAME: miapppython  # Aqui va el nombre de su aplicación
      PYTHON_VERSION: '3.9'           # la versión de Python

    on:
      push:
        branches: [ "main" ]
      workflow_dispatch:

    permissions:
      contents: read

    jobs:
      build:
        runs-on: ubuntu-latest

        steps:
          - uses: actions/checkout@v4
          - name: Set up Python ${{ env.PYTHON_VERSION }}
            uses: actions/setup-python@v4
            with:
              python-version: ${{ env.PYTHON_VERSION }}

          - name: Install dependencies
            run: |
              python -m pip install --upgrade pip
              pip install -r requirements.txt

          - name: Package application
            run: zip -r python-app.zip .

          - name: Upload artifact for deployment job
            uses: actions/upload-artifact@v4
            with:
              name: python-app
              path: python-app.zip

      deploy:
        permissions:
          contents: none
        runs-on: ubuntu-latest
        needs: build
        environment:
          name: 'Development'
          url: ${{ steps.deploy-to-webapp.outputs.webapp-url }}

        steps:
          - name: Download artifact from build job
            uses: actions/download-artifact@v4
            with:
              name: python-app

          - name: Deploy to Azure Web App
            id: deploy-to-webapp
            uses: azure/webapps-deploy@v2
            with:
              app-name: ${{ env.AZURE_WEBAPP_NAME }}
              publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
              package: python-app.zip
    ```
