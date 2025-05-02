# simetrik-parsers

![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)

**Simetrik Parsers** es un SDK y herramienta de línea de comandos en Python para generar *stubs* de parsers que transforman datos no estructurados o semi-estructurados en un entorno controlado por Simetrik (Startup SaaS).

---

## 🛠 Instalación

1. Inicializa el proyecto y fija la versión de Python:
   ```bash
   uv init . && uv python pin 3.13
   ```
2. Añade las dependencias:
   ```bash
   uv add typer pydantic requests pandas pyarrow xlrd rarfile openpyxl fastparquet \ 
          cryptography beautifulsoup4 python-dotenv boto3 --dev ruff
   ```
3. Sincroniza y activa el entorno virtual:
   ```bash
   uv sync
   source .venv/bin/activate
   ```

## 📦 Uso

La CLI se expone como el comando `simetrik-parsers`. Ejecuta:

```bash
simetrik-parsers --help
```

### create-parser

Genera un *stub* de parser en:
```
src/simetrik_parsers/application/parsers/<nombre>.py
```

```bash
simetrik-parsers create-parser <nombre_del_parser>
``` 

```yaml
# Ejemplo de stub generado:
from simetrik_parsers.domain.base.base_parser import BaseParser

class MiParser(BaseParser):
    """Parser mi_parser"""
    def parse(self, input_file, args):
        """Implementa la lógica de parseo"""
        return []
```

## 📂 Estructura del Proyecto

```
src/
└── simetrik_parsers/
    ├── cli.py
    ├── domain/
    │   ├── base/
    │   │   └── base_parser.py
    │   └── entities/
    │       └── schemas.py
    └── application/
        └── parsers/
            └── <parser>.py

pyproject.toml
uv.lock
README.md
```  

---

## 🚀 Desarrollo

- Revisa el código con **Ruff**:
  ```bash
  uv run ruff .
  ```
- Agrega nuevos parsers con `create-parser`.
- Abre un PR al repositorio público y sigue las guías de estilo.

## 📄 Licencia

MIT License.
