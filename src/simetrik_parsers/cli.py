from pathlib import Path
from textwrap import dedent
import typer
from typer import Typer, echo
import json

app = Typer()


@app.command()
def create_layout(
    name: str,
    version: str = "1.0.0",
    description: str = ""
):
    """Crea un nuevo layout JSON en application/layouts/{name}.json (relativo a CWD)"""
    # Directorio donde se guardarán los layouts, relativo a CWD
    layouts_dir = Path.cwd() / "application" / "layouts"
    layouts_dir.mkdir(parents=True, exist_ok=True)
    file_path = layouts_dir / f"{name}.json"
    # Si ya existe, abortar
    if file_path.exists():
        echo(f"El layout '{name}' ya existe.")
        raise typer.Exit(code=1)
    # Importar esquema y crear instancia
    from simetrik_parsers.domain.entities.schemas import LayoutSchema, PipelineDefinition
    schema = LayoutSchema(
        name=name,
        description=description,
        version=version,
        pipeline=PipelineDefinition()
    )
    # Escribir JSON formateado (compatible con Pydantic v2)
    data = schema.model_dump()
    file_path.write_text(json.dumps(data, indent=4, ensure_ascii=False))
    echo(f"Layout '{name}' creado correctamente en {file_path}")


@app.command()
def create_parser(name: str):
    """Genera un nuevo parser en application/parsers/{name}.py (relativo a CWD)"""
    # Directorio donde se guardarán los parsers, relativo a CWD
    parsers_dir = Path.cwd() / "application" / "parsers"
    parsers_dir.mkdir(parents=True, exist_ok=True)
    file_path = parsers_dir / f"{name}.py"
    # Si ya existe, abortar
    if file_path.exists():
        echo(f"El parser '{name}' ya existe.")
        raise typer.Exit(code=1)
    # Nombre de la clase (CamelCase)
    class_name = "".join(word.capitalize() for word in name.split("_")) + "Parser"
    # Contenido del stub con dedent
    content = dedent(
        f"""\
from simetrik_parsers.domain.base.base_parser import BaseParser

class {class_name}(BaseParser):
    '''Parser {name}'''
    def parse(self, input_file, args):
        '''Implementa la lógica de parseo'''
        # TODO: implementar lógica de parseo
        return []
"""
    )
    # Escribir el archivo
    file_path.write_text(content)
    echo(f"Parser '{name}' creado correctamente en {file_path}")


if __name__ == "__main__":
    app()
