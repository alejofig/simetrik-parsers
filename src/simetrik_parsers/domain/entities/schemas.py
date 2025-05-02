from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field


class PipelineStep(BaseModel):
    name: str = Field(..., description="Nombre del step de pipeline")
    args: Dict[str, Any] = Field(
        default_factory=dict, description="Argumentos del step"
    )


class PipelineDefinition(BaseModel):
    pipeline: List[PipelineStep] = Field(
        default_factory=list, description="Lista de pasos a ejecutar"
    )


class ScriptType(str, Enum):
    ESTANDAR = "ESTANDAR"
    PREDETERMINADO = "PREDETERMINADO"
    CUSTOM = "CUSTOM"


class ScriptSchema(BaseModel):
    name: str = Field(..., description="Nombre del parser")
    description: Optional[str] = Field("", description="Descripción del parser")
    version: str = Field(..., description="Versión del parser")
    type: ScriptType = Field(..., description="Tipo de parser")
    pipeline: PipelineDefinition = Field(..., description="Definición de pipeline")
    account_id: Optional[str] = Field(
        None, description="ID de cuenta (solo para CUSTOM)"
    )


class LayoutSchema(BaseModel):
    name: str = Field(..., description="Nombre del layout")
    description: Optional[str] = Field("", description="Descripción del layout")
    version: str = Field(..., description="Versión del layout")
    pipeline: PipelineDefinition = Field(
        ..., description="Definición de pipeline asociado al layout"
    )
    dict_columns: Dict[str, Dict[str, Tuple[int, int]]] = Field(
        default_factory=dict,
        description="Definiciones de columnas para parser de ancho fijo: mapeo record_type->column_name->(start,end)"
    )
