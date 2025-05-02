from typing import List, Dict, Any


class BaseParser:
    """Clase abstracta para todos los parsers. Deben extender e implementar `parse()`."""

    def __init__(self, *args, **kwargs):
        import tempfile, shutil
        # Configura directorio temporal
        self.temp_dir = tempfile.mkdtemp()
        self._shutil = shutil

    def parse(self, input_file: Any, args: Dict[str, Any]) -> List[Any]:
        """Recibe un archivo y argumentos; retorna lista de archivos transformados."""
        raise NotImplementedError("`parse` debe ser implementado por la subclase")

    def cleanup(self):
        """Elimina el directorio temporal asociado al parser."""
        self._shutil.rmtree(self.temp_dir, ignore_errors=True)
