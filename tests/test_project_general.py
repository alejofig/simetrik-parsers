import os
import pytest
import json

from simetrik_parsers import hello
from simetrik_parsers.domain.base.base_parser import BaseParser
from simetrik_parsers.domain.entities.schemas import ScriptSchema, LayoutSchema, PipelineDefinition
from simetrik_parsers.cli import app
from typer.testing import CliRunner

# Dummy parser for testing BaseParser
class DummyParser(BaseParser):
    def parse(self, input_file, args):
        return ["parsed"]

runner = CliRunner()

def test_hello():
    assert hello() == "Hello from simetrik-parsers!"

def test_base_parser_not_implemented():
    with pytest.raises(NotImplementedError):
        BaseParser().parse(b"", {})

def test_dummy_parser_parse_and_cleanup(tmp_path):
    parser = DummyParser({}, {})
    # Temp dir creado por BaseParser
    assert os.path.isdir(parser.temp_dir)
    result = parser.parse(b"", {})
    assert result == ["parsed"]
    parser.cleanup()
    assert not os.path.isdir(parser.temp_dir)

def test_schemas_minimal():
    # ScriptSchema mínimo
    s = ScriptSchema(
        name="test",
        description="",
        version="1.0",
        type="ESTANDAR",
        pipeline=PipelineDefinition()
    )
    assert s.name == "test"
    # LayoutSchema mínimo
    l = LayoutSchema(
        name="layout",
        description="",
        version="1.0",
        pipeline=PipelineDefinition(),
        dict_columns={}
    )
    assert l.name == "layout"

def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "create-layout" in result.output
    assert "create-parser" in result.output

def test_cli_individual_help():
    res1 = runner.invoke(app, ["create-parser", "--help"])
    assert "Genera un nuevo parser" in res1.output
    res2 = runner.invoke(app, ["create-layout", "--help"])
    assert "Crea un nuevo layout" in res2.output 