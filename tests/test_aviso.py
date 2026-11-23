from datetime import datetime, timedelta
import pytest

from dominio.aviso import Aviso
from dominio.enums import EstadoAviso, GravedadEstimada, TipoSituacion
from dominio.excepciones import (AutorNoValidoError, CampoVacioError, DatoInvalidoError, OperacionNoPermitidaError)
from dominio.reportante_institucional import ReportanteInstitucional


@pytest.fixture
def reportante_titular() -> ReportanteInstitucional:
    return ReportanteInstitucional(id=1, nombre="Laura Gómez", institucion="Defensa Civil")


@pytest.fixture
def otro_reportante() -> ReportanteInstitucional:
    return ReportanteInstitucional(id=2, nombre="Carlos Pérez", institucion="Bomberos Voluntarios")


@pytest.fixture
def fecha_base() -> datetime:
    return datetime(2026, 11, 22, 10, 0, 0)


@pytest.fixture
def aviso_pendiente(reportante_titular, fecha_base):
    return Aviso(
        reportante = reportante_titular,
        ubicacion = "Av. San Martín 1250",
        tipo_situacion = TipoSituacion.INUNDACION,
        gravedad_estimada = GravedadEstimada.ALTA,
        descripcion = "Calzada anegada con obstrucción total del tránsito.",
        fecha_hora = fecha_base,
    )


def test_aviso_recien_registrado_esta_pendiente_sin_notas_ni_descarte(aviso_pendiente, reportante_titular, fecha_base):
    assert aviso_pendiente.estado == EstadoAviso.PENDIENTE
    assert aviso_pendiente.notas == []
    assert aviso_pendiente.descarte is None
    assert aviso_pendiente.reportante == reportante_titular
    assert aviso_pendiente.fecha_hora == fecha_base


@pytest.mark.parametrize(
    ("ubicacion", "descripcion"),
    [
        ("", "Descripción válida"),
        ("Calle Falsa 123", ""),
    ],
)
def test_rechaza_registro_de_aviso_con_campos_obligatorios_vacios(reportante_titular, fecha_base, ubicacion, descripcion):
    with pytest.raises(CampoVacioError):
        Aviso(
            reportante=reportante_titular,
            ubicacion=ubicacion,
            tipo_situacion=TipoSituacion.INCENDIO,
            gravedad_estimada=GravedadEstimada.MEDIA,
            descripcion=descripcion,
            fecha_hora=fecha_base,
        )


def test_rechaza_creacion_de_reportante_con_id_no_positivo():
    with pytest.raises(DatoInvalidoError):
        ReportanteInstitucional(id=0, nombre="Ana", institucion="Salud")


def test_r2_agregar_nota_en_aviso_pendiente_conserva_autor_y_fecha_hora(aviso_pendiente, reportante_titular, fecha_base):
    fecha_nota = fecha_base + timedelta(minutes=15)

    aviso_pendiente.agregar_nota(autor=reportante_titular, texto="El nivel del agua subió 30 centímetros.", fecha_hora=fecha_nota)

    assert aviso_pendiente.estado == EstadoAviso.PENDIENTE
    assert len(aviso_pendiente.notas) == 1
    nota = aviso_pendiente.notas[0]
    assert nota.autor == reportante_titular
    assert nota.texto == "El nivel del agua subió 30 centímetros."
    assert nota.fecha_hora == fecha_nota


def test_agregar_dos_notas_conserva_ambas_en_orden_de_llegada(aviso_pendiente, reportante_titular, fecha_base):
    fecha_nota_1 = fecha_base + timedelta(minutes=10)
    fecha_nota_2 = fecha_base + timedelta(minutes=25)

    aviso_pendiente.agregar_nota(autor=reportante_titular, texto="Primera ampliación del reporte.", fecha_hora=fecha_nota_1)
    aviso_pendiente.agregar_nota(autor=reportante_titular, texto="Segunda ampliación.", fecha_hora=fecha_nota_2)

    assert len(aviso_pendiente.notas) == 2
    assert aviso_pendiente.notas[0].texto == "Primera ampliación del reporte."
    assert aviso_pendiente.notas[0].fecha_hora == fecha_nota_1
    assert aviso_pendiente.notas[1].texto == "Segunda ampliación."
    assert aviso_pendiente.notas[1].fecha_hora == fecha_nota_2


def test_rechaza_nota_de_otro_reportante_y_mantiene_estado_y_notas_vacias(aviso_pendiente, otro_reportante, fecha_base):
    with pytest.raises(AutorNoValidoError):
        aviso_pendiente.agregar_nota(autor=otro_reportante, texto="Intento de nota de un tercero.", fecha_hora=fecha_base + timedelta(minutes=5))

    assert aviso_pendiente.estado == EstadoAviso.PENDIENTE
    assert aviso_pendiente.notas == []


def test_rechaza_nota_con_texto_vacio_y_mantiene_estado_y_notas_vacias(aviso_pendiente, reportante_titular, fecha_base):
    with pytest.raises(CampoVacioError):
        aviso_pendiente.agregar_nota(autor=reportante_titular, texto="", fecha_hora=fecha_base + timedelta(minutes=5))

    assert aviso_pendiente.estado == EstadoAviso.PENDIENTE
    assert aviso_pendiente.notas == []


def test_agregar_nota_no_modifica_datos_originales_del_aviso(aviso_pendiente, reportante_titular, fecha_base):
    ubicacion_original = aviso_pendiente.ubicacion
    tipo_original = aviso_pendiente.tipo_situacion
    gravedad_original = aviso_pendiente.gravedad_estimada
    descripcion_original = aviso_pendiente.descripcion

    aviso_pendiente.agregar_nota(autor=reportante_titular, texto="Se solicita móvil adicional en la esquina.", fecha_hora=fecha_base + timedelta(minutes=20))

    assert aviso_pendiente.ubicacion == ubicacion_original
    assert aviso_pendiente.tipo_situacion == tipo_original
    assert aviso_pendiente.gravedad_estimada == gravedad_original
    assert aviso_pendiente.descripcion == descripcion_original


def test_descartar_aviso_pendiente_cambia_estado_y_conserva_justificacion_y_fecha(aviso_pendiente, fecha_base):
    fecha_descarte = fecha_base + timedelta(minutes=30)

    aviso_pendiente.descartar(justificacion="Reporte duplicado de otro incidente ya atendido.", fecha_hora=fecha_descarte)

    assert aviso_pendiente.estado == EstadoAviso.DESCARTADO
    assert aviso_pendiente.descarte is not None
    assert aviso_pendiente.descarte.justificacion == "Reporte duplicado de otro incidente ya atendido."
    assert aviso_pendiente.descarte.fecha_hora == fecha_descarte


def test_rechaza_descarte_con_justificacion_vacia_y_mantiene_pendiente(aviso_pendiente, fecha_base):
    with pytest.raises(CampoVacioError):
        aviso_pendiente.descartar(justificacion="", fecha_hora=fecha_base + timedelta(minutes=10))

    assert aviso_pendiente.estado == EstadoAviso.PENDIENTE
    assert aviso_pendiente.descarte is None


def test_aviso_descartado_rechaza_nuevas_notas_y_conserva_notas_previas(aviso_pendiente, reportante_titular, fecha_base):
    aviso_pendiente.agregar_nota(autor=reportante_titular, texto="Nota previa al descarte.", fecha_hora=fecha_base + timedelta(minutes=5))

    aviso_pendiente.descartar(justificacion="Falsa alarma verificada en el lugar.", fecha_hora=fecha_base + timedelta(minutes=15))

    with pytest.raises(OperacionNoPermitidaError):
        aviso_pendiente.agregar_nota(autor=reportante_titular, texto="Nota posterior que debe rechazarse.", fecha_hora=fecha_base + timedelta(minutes=20))

    assert aviso_pendiente.estado == EstadoAviso.DESCARTADO
    assert len(aviso_pendiente.notas) == 1
    assert aviso_pendiente.notas[0].texto == "Nota previa al descarte."


def test_aviso_descartado_rechaza_segundo_descarte_y_conserva_justificacion_original(aviso_pendiente, fecha_base):
    fecha_primer_descarte = fecha_base + timedelta(minutes=15)
    aviso_pendiente.descartar(justificacion="Justificación original.", fecha_hora=fecha_primer_descarte)

    with pytest.raises(OperacionNoPermitidaError):
        aviso_pendiente.descartar(justificacion="Intento de sobrescribir el descarte.", fecha_hora=fecha_base + timedelta(minutes=40))

    assert aviso_pendiente.estado == EstadoAviso.DESCARTADO
    assert aviso_pendiente.descarte is not None
    assert aviso_pendiente.descarte.justificacion == "Justificación original."
    assert aviso_pendiente.descarte.fecha_hora == fecha_primer_descarte


def test_aviso_aceptado_rechaza_nuevas_notas_y_mantiene_estado(aviso_pendiente, reportante_titular, fecha_base):
    aviso_pendiente.aceptar()

    with pytest.raises(OperacionNoPermitidaError):
        aviso_pendiente.agregar_nota(autor=reportante_titular, texto="Intento de agregar nota tras aceptación.", fecha_hora=fecha_base + timedelta(minutes=25))

    assert aviso_pendiente.estado == EstadoAviso.ACEPTADO
    assert aviso_pendiente.notas == []


def test_aviso_aceptado_rechaza_descarte_y_mantiene_estado(aviso_pendiente, fecha_base):
    aviso_pendiente.aceptar()

    with pytest.raises(OperacionNoPermitidaError):
        aviso_pendiente.descartar(justificacion="Intento de descartar un aviso ya aceptado.", fecha_hora=fecha_base + timedelta(minutes=30))

    assert aviso_pendiente.estado == EstadoAviso.ACEPTADO
    assert aviso_pendiente.descarte is None