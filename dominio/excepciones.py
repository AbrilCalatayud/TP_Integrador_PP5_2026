class DatoInvalidoError(Exception):
    pass


class JustificacionInvalidaError(DatoInvalidoError):
    pass


class OperacionNoPermitidaError(Exception):
    pass


class AutorNoValidoError(OperacionNoPermitidaError):
    pass