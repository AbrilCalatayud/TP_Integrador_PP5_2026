from enum import Enum

class EstadoAviso(Enum):
    PENDIENTE = "PENDIENTE"
    ACEPTADO = "ACEPTADO"
    DESCARTADO = "DESCARTADO"

class TipoSituacion(Enum):
    INUNDACION = "INUNDACION"
    INCENDIO = "INCENDIO"
    ACCIDENTE_VIAL = "ACCIDENTE_VIAL"

class GravedadEstimada(Enum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"