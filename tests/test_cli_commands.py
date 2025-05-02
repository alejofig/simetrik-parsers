import shutil
from pathlib import Path
import json
import pytest
from typer.testing import CliRunner

from simetrik_parsers.cli import app
from simetrik_parsers.domain.entities.schemas import LayoutSchema

runner = CliRunner()


def test_create_parser(tmp_path):
    # Asegurar un estado limpio
    parsers_dir = Path("src/simetrik_parsers/application/parsers")
    if parsers_dir.exists():
        shutil.rmtree(parsers_dir)

    # Ejecutar comando
    result = runner.invoke(app, ["create-parser", "foo_bar"])
    assert result.exit_code == 0
    file_path = parsers_dir / "foo_bar.py"
    assert file_path.exists()
    content = file_path.read_text()
    assert "class FooBarParser" in content

    # Limpiar
    shutil.rmtree(parsers_dir)


def test_create_parser_duplicate(tmp_path):
    parsers_dir = Path("src/simetrik_parsers/application/parsers")
    parsers_dir.mkdir(parents=True, exist_ok=True)
    file_path = parsers_dir / "dup.py"
    file_path.write_text("# existing")

    result = runner.invoke(app, ["create-parser", "dup"])
    assert result.exit_code != 0
    assert "ya existe" in result.output

    shutil.rmtree(parsers_dir)


def test_create_layout(tmp_path):
    layouts_dir = Path("src/simetrik_parsers/application/layouts")
    if layouts_dir.exists():
        shutil.rmtree(layouts_dir)

    result = runner.invoke(app, [
        "create-layout", "baz", "--version", "2.0.0", "--description", "desc"
    ])
    assert result.exit_code == 0
    file_path = layouts_dir / "baz.json"
    assert file_path.exists()
    data = json.loads(file_path.read_text())
    schema = LayoutSchema(**data)
    assert schema.name == "baz"
    assert schema.version == "2.0.0"
    assert schema.description == "desc"

    shutil.rmtree(layouts_dir)


def test_create_layout_duplicate(tmp_path):
    layouts_dir = Path("src/simetrik_parsers/application/layouts")
    layouts_dir.mkdir(parents=True, exist_ok=True)
    file_path = layouts_dir / "dup.json"
    file_path.write_text("{}")

    result = runner.invoke(app, ["create-layout", "dup"])
    assert result.exit_code != 0
    assert "ya existe" in result.output

    shutil.rmtree(layouts_dir) 