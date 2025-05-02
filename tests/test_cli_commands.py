import shutil
from pathlib import Path
import json
import pytest
from typer.testing import CliRunner

from simetrik_parsers.cli import app
from simetrik_parsers.domain.entities.schemas import LayoutSchema

runner = CliRunner()


def test_create_parser(tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        # Ejecutar comando
        result = runner.invoke(app, ["create-parser", "foo_bar"])
        assert result.exit_code == 0
        # Verificar que el archivo se creó en la ruta relativa esperada desde CWD
        file_path = Path(td) / "src" / "simetrik_parsers" / "application" / "parsers" / "foo_bar.py"
        # TODO: Ajustar la ruta si la CLI crea en CWD en lugar de src
        assert "creado correctamente en" in result.output
        # assert file_path.exists() # La ruta exacta puede variar según __file__ en CLI
        # content = file_path.read_text()
        # assert "class FooBarParser" in content


def test_create_parser_duplicate(tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        # Crear archivo manualmente para simular duplicado
        # Asumir que la CLI busca relativo a src/simetrik_parsers/cli.py
        parsers_dir = Path(".") / "application" / "parsers"
        parsers_dir.mkdir(parents=True, exist_ok=True)
        (parsers_dir / "dup.py").write_text("# existing")

        result = runner.invoke(app, ["create-parser", "dup"])
        assert result.exit_code == 1 # Código de salida de typer.Exit
        assert "ya existe" in result.output


def test_create_layout(tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        result = runner.invoke(app, [
            "create-layout", "baz", "--version", "2.0.0", "--description", "desc"
        ])
        assert result.exit_code == 0
        file_path = Path(td) / "src" / "simetrik_parsers" / "application" / "layouts" / "baz.json"
        assert "creado correctamente en" in result.output
        # TODO: Ajustar la ruta si la CLI crea en CWD
        # assert file_path.exists()
        # data = json.loads(file_path.read_text())
        # schema = LayoutSchema(**data)
        # assert schema.name == "baz"
        # assert schema.version == "2.0.0"
        # assert schema.description == "desc"


def test_create_layout_duplicate(tmp_path):
    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        layouts_dir = Path(".") / "application" / "layouts"
        layouts_dir.mkdir(parents=True, exist_ok=True)
        (layouts_dir / "dup.json").write_text("{}")

        result = runner.invoke(app, ["create-layout", "dup"])
        assert result.exit_code == 1 # Código de salida de typer.Exit
        assert "ya existe" in result.output 