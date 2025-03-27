import os
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_URL = "https://bitbucket.org/site/oauth2/access_token"
BITBUCKET_API_URL = "https://api.bitbucket.org/2.0"

client_id = os.getenv("OAUTH_CLIENT_ID")
client_secret = os.getenv("OAUTH_CLIENT_SECRET")
commit_hash = os.getenv("BITBUCKET_COMMIT")
workspace_slug = os.getenv("BITBUCKET_WORKSPACE")
repo_slug = os.getenv("BITBUCKET_REPO_SLUG")
project_key = os.getenv("BITBUCKET_PROJECT_KEY")


def bitbucket_create_code_insights_report(headers, workspace, repo, commit):
    """Crea un reporte de código en Bitbucket."""
    url = (
        f"{BITBUCKET_API_URL}/repositories/{workspace}/{repo}/commit/{commit}/reports/"
        f"titvo-security-scan-{uuid.uuid4()}"
    )
    payload = {
        "title": "Titvo Security Scan",
        "details": "Security scan report",
        "report_type": "SECURITY",
        "reporter": "titvo-security-scan",
        "result": "FAILED",
        "data": [
            {"title": "Duration in seconds", "type": "DURATION", "value": 14},
            {
                "title": "Safe to merge?",
                "type": "BOOLEAN",
                "value": False,
            },
            {
                "title": "Vulnerabilities",
                "type": "NUMBER",
                "value": 14,
            },
        ],
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    return response.json()


def download_file(headers, workspace, repo, file_path, commit):
    """Descarga un archivo específico del commit."""
    content_url = (
        f"{BITBUCKET_API_URL}/repositories/{workspace}/{repo}/src/{commit}/{file_path}"
    )
    response = requests.get(content_url, headers=headers, timeout=30)

    if response.status_code == 200:
        # Crear directorios si no existen
        full_path = os.path.join("repo_files", file_path)
        dirname = os.path.dirname(full_path)
        if dirname != "":
            os.makedirs(dirname, exist_ok=True)

        # Guardar el contenido directamente
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✓ Descargado: {full_path}")
        return True
    return False


def main():
    # Crear el directorio principal repo_files
    os.makedirs("repo_files", exist_ok=True)

    response = requests.post(
        ACCESS_TOKEN_URL,
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
        },
        timeout=30,
    )

    access_token = response.json().get("access_token")
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}

    # Obtener información del commit específico usando la API REST
    commit_url = f"{BITBUCKET_API_URL}/repositories/{workspace_slug}/{repo_slug}/commit/{commit_hash}"
    commit_response = requests.get(commit_url, headers=headers, timeout=30)

    if commit_response.status_code == 200:
        commit_info = commit_response.json()
        print(f"Información del commit {commit_hash}:")
        print(f"Hash: {commit_info['hash']}")
        print(f"Fecha: {commit_info['date']}")
        print(f"Mensaje: {commit_info['message']}")
        print(f"Autor: {commit_info['author']['raw']}")

        # Obtener la lista de archivos modificados
        diff_url = f"{BITBUCKET_API_URL}/repositories/{workspace_slug}/{repo_slug}/diff/{commit_hash}"
        diff_response = requests.get(diff_url, headers=headers, timeout=30)

        if diff_response.status_code == 200:
            diff_content = diff_response.text
            # Extraer los nombres de archivos del diff
            files = set()
            for line in diff_content.split("\n"):
                if line.startswith("diff --git"):
                    # El formato es: diff --git a/path/to/file b/path/to/file
                    file_path = line.split(" b/")[1]
                    files.add(file_path)

            print("\nArchivos modificados:")
            for file in sorted(files):
                print(f"- {file}")

            print("\nDescargando archivos...")
            successful_downloads = 0
            for file in sorted(files):
                if download_file(headers, workspace_slug, repo_slug, file, commit_hash):
                    successful_downloads += 1

            print(
                f"\nResumen de descargas: {successful_downloads}/{len(files)} archivos descargados exitosamente"
            )
        else:
            print(
                f"\nError al obtener los archivos modificados: {diff_response.status_code} - {diff_response.text}"
            )
        bitbucket_create_code_insights_report(headers, workspace_slug, repo_slug, commit_hash)
    else:
        print(f"No se encontró el commit con hash {commit_hash}")
        print(f"Error: {commit_response.status_code} - {commit_response.text}")


if __name__ == "__main__":
    main()
