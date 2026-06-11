# redpyne

Herramienta de línea de comandos para descargar issues de Redmine junto con sus archivos adjuntos.

## Requisitos

- Python 3.12 o superior

## Instalación

### Con pip

Directamente desde el repositorio de GitHub:

```bash
pip install git+https://github.com/fvarrui/redpyne.git
```

### Con uv

```bash
uv tool install git+https://github.com/fvarrui/redpyne.git
```

### Modo desarrollo

```bash
git clone https://github.com/fvarrui/redpyne.git
cd redpyne

# con pip
pip install -e .

# con uv
uv sync
```

## Configuración

Antes de usar la herramienta, es necesario crear el fichero de configuración en el perfil del usuario.

### Ubicación

| Sistema operativo | Ruta                                  |
|-------------------|---------------------------------------|
| Windows           | `%USERPROFILE%\.redpyne\config.ini`   |
| Linux / macOS     | `~/.redpyne/config.ini`               |

### Contenido

```ini
[redmine]
url = https://tu-instancia-redmine.ejemplo.com

; Opción A: autenticación por API token (recomendado)
api_token = tu_api_token

; Opción B: autenticación por usuario y contraseña
; username = tu_usuario
; password = tu_contraseña
```

El API token se puede obtener en Redmine desde **Mi cuenta → API access key**.

## Uso

```
redpyne [opciones] <número_de_issue>
```

| Opción | Descripción |
|---|---|
| `--output DIR` | Directorio padre donde se creará el directorio de la issue (por defecto: directorio actual). |
| `--url URL` | URL base de Redmine (sobreescribe el config). |
| `--api-token TOKEN` | API token de Redmine (sobreescribe el config). |
| `--username USER` | Usuario de Redmine (sobreescribe el config). |
| `--password PASS` | Contraseña de Redmine (sobreescribe el config). |

### Ejemplos

```bash
# Crea ./123456/issue.json y ./123456/attachments/
redpyne 123456

# Crea ./proyectos/123456/issue.json y ./proyectos/123456/attachments/
redpyne --output proyectos 123456

# Sin fichero de configuración, pasando las credenciales por parámetro
redpyne --url https://redmine.ejemplo.com --api-token abc123 123456

# En modo desarrollo con uv
uv run redpyne 123456
```

### Estructura de salida

Siempre se crea un directorio con el ID de la issue. Dentro, el fichero `issue.json` y, si hay adjuntos, el directorio `attachments/`.

```
[--output DIR/]<id>/
  issue.json
  attachments/
    documento.pdf
    imagen.png
```

## Licencia

MIT
