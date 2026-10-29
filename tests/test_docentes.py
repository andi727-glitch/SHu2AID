import json

import pytest
import yaml
import xml.etree.ElementTree as ET

from docentes import RepositorioDocentes, DocenteNoEncontrado, DocenteDuplicado, DocenteError
from formatos import exportar


@pytest.fixture
def repo():
    r = RepositorioDocentes()
    r.crear("1", "Ana Pérez", "Redes")
    r.crear("2", "Luis Gómez", "Software")
    return r


def test_crear(repo):
    d = repo.crear("3", "Marta", "Bases de datos")
    assert repo.obtener("3") == d


def test_crear_duplicado(repo):
    with pytest.raises(DocenteDuplicado):
        repo.crear("1", "Otro", "X")


def test_crear_campos_vacios(repo):
    with pytest.raises(DocenteError):
        repo.crear("9", "", "X")


def test_listar(repo):
    assert len(repo.listar()) == 2


def test_obtener_inexistente(repo):
    with pytest.raises(DocenteNoEncontrado):
        repo.obtener("99")


def test_actualizar(repo):
    repo.actualizar("1", nombre="Ana López")
    assert repo.obtener("1").nombre == "Ana López"
    assert repo.obtener("1").especialidad == "Redes"


def test_eliminar(repo):
    repo.eliminar("1")
    with pytest.raises(DocenteNoEncontrado):
        repo.obtener("1")


def test_exportar_json(repo):
    datos = json.loads(exportar(repo.listar(), "json"))
    assert datos[0]["numero_empleado"] == "1"


def test_exportar_yaml(repo):
    datos = yaml.safe_load(exportar(repo.listar(), "yaml"))
    assert datos["docentes"][1]["nombre"] == "Luis Gómez"


def test_exportar_xml(repo):
    raiz = ET.fromstring(exportar(repo.listar(), "xml"))
    assert len(raiz.findall("docente")) == 2


def test_formato_invalido(repo):
    with pytest.raises(ValueError):
        exportar(repo.listar(), "csv")