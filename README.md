# Bitbucket API - Descargador de Archivos y Generador de Reportes

Este script permite descargar archivos modificados de un commit específico en un repositorio de Bitbucket Cloud y generar reportes de seguridad.

## Requisitos

- Python 3.x
- Credenciales de OAuth2 de Bitbucket Cloud

## Configuración

1. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
OAUTH_CLIENT_ID=tu_client_id
OAUTH_CLIENT_SECRET=tu_client_secret
BITBUCKET_COMMIT=hash_del_commit
BITBUCKET_WORKSPACE=nombre_del_workspace
BITBUCKET_REPO_SLUG=nombre_del_repositorio
BITBUCKET_PROJECT_KEY=clave_del_proyecto
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Uso

Ejecuta el script:

```bash
python main.py
```

El script:
1. Obtendrá la información del commit especificado
2. Listará los archivos modificados en ese commit
3. Descargará los archivos en el directorio `repo_files/`
4. Generará un reporte de seguridad en Bitbucket con métricas como:
   - Duración del análisis
   - Estado de seguridad (seguro para merge)
   - Número de vulnerabilidades encontradas

## Estructura del Proyecto

```
.
├── .env                    # Variables de entorno (no incluido en git)
├── .gitignore             # Archivos ignorados por git
├── README.md              # Este archivo
├── main.py                # Script principal
├── requirements.txt       # Dependencias del proyecto
└── repo_files/           # Directorio donde se descargan los archivos
```

## Notas

- Los archivos se descargan manteniendo la estructura de directorios original del repositorio
- Se requiere un token de acceso OAuth2 válido con permisos de lectura al repositorio
- Los reportes de seguridad se generan automáticamente después de descargar los archivos

## Referencias

- [Documentación de OAuth en Bitbucket Cloud](https://support.atlassian.com/bitbucket-cloud/docs/use-oauth-on-bitbucket-cloud/)
- [Variables y Secretos en Bitbucket Cloud](https://support.atlassian.com/bitbucket-cloud/docs/variables-and-secrets/)
- [API de Reportes de Bitbucket Cloud](https://developer.atlassian.com/cloud/bitbucket/rest/api-group-reports/#api-repositories-workspace-repo-slug-commit-commit-reports-reportid-put) 