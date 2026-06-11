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

```bash
redpyne <número_de_issue>
```

### Ejemplo

```bash
redpyne 123456

# en modo desarrollo con uv
uv run redpyne 123456
```

Esto genera:

- `123456.json` — datos completos del issue en formato JSON.
- `attachments/` — directorio con todos los archivos adjuntos del issue.

## Licencia

MIT
