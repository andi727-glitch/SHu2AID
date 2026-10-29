import json
import os
from dataclasses import dataclass, asdict


class DocenteError(Exception):
    """Error base para operaciones con docentes."""


class DocenteNoEncontrado(DocenteError):
    pass


class DocenteDuplicado(DocenteError):
    pass


@dataclass
class Docente:
    numero_empleado: str
    nombre: str
    especialidad: str

    def a_dict(self) -> dict:
        return asdict(self)


class RepositorioDocentes:
    """CRUD de docentes en memoria, con respaldo opcional en un archivo JSON."""

    def __init__(self, archivo=None):
        self._docentes: dict[str, Docente] = {}
        self._archivo = archivo
        self._cargar()  # al iniciar, lee el archivo (si existe)

    # ---------- persistencia ----------
    def _cargar(self):
        if not self._archivo or not os.path.exists(self._archivo):
            return
        with open(self._archivo, encoding="utf-8") as f:
            for datos in json.load(f):
                d = Docente(**datos)
                self._docentes[d.numero_empleado] = d

    def _guardar(self):
        if not self._archivo:
            return
        with open(self._archivo, "w", encoding="utf-8") as f:
            json.dump(
                [d.a_dict() for d in self._docentes.values()],
                f,
                indent=2,
                ensure_ascii=False,
            )

    # CREATE 
    def crear(self, numero_empleado, nombre, especialidad) -> Docente:
        numero_empleado = str(numero_empleado).strip()
        if not numero_empleado or not nombre.strip() or not especialidad.strip():
            raise DocenteError("Todos los campos son obligatorios.")
        if numero_empleado in self._docentes:
            raise DocenteDuplicado(f"Ya existe el empleado {numero_empleado}.")
        docente = Docente(numero_empleado, nombre.strip(), especialidad.strip())
        self._docentes[numero_empleado] = docente
        self._guardar()  # guarda en el archivo
        return docente

    # READ 
    def obtener(self, numero_empleado) -> Docente:
        try:
            return self._docentes[str(numero_empleado).strip()]
        except KeyError:
            raise DocenteNoEncontrado(f"No existe el empleado {numero_empleado}.")

    def listar(self) -> list[Docente]:
        return list(self._docentes.values())

    # UPDATE 
    def actualizar(self, numero_empleado, nombre=None, especialidad=None) -> Docente:
        docente = self.obtener(numero_empleado)
        if nombre and nombre.strip():
            docente.nombre = nombre.strip()
        if especialidad and especialidad.strip():
            docente.especialidad = especialidad.strip()
        self._guardar()  # guarda en el archivo
        return docente

    # DELETE 
    def eliminar(self, numero_empleado) -> Docente:
        docente = self.obtener(numero_empleado)
        del self._docentes[docente.numero_empleado]
        self._guardar()  # guarda en el archivo
        return docente