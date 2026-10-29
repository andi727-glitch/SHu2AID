import json
import xml.etree.ElementTree as ET

import yaml

FORMATOS_VALIDOS = ("json", "yaml", "xml")


def a_json(docentes) -> str:
    return json.dumps([d.a_dict() for d in docentes], indent=2, ensure_ascii=False)


def a_yaml(docentes) -> str:
    return yaml.safe_dump(
        {"docentes": [d.a_dict() for d in docentes]},
        allow_unicode=True,
        sort_keys=False,
    )


def a_xml(docentes) -> str:
    raiz = ET.Element("docentes")
    for d in docentes:
        nodo = ET.SubElement(raiz, "docente")
        for campo, valor in d.a_dict().items():
            ET.SubElement(nodo, campo).text = valor
    ET.indent(raiz)  # Python 3.9+
    return ET.tostring(raiz, encoding="unicode")


def exportar(docentes, formato: str) -> str:
    formato = formato.lower().strip()
    if formato == "json":
        return a_json(docentes)
    elif formato == "yaml":
        return a_yaml(docentes)
    elif formato == "xml":
        return a_xml(docentes)
    else:
        raise ValueError(f"Formato no soportado: {formato}")

def guardar(docentes, formato: str, nombre_archivo: str) -> str:
    """Exporta los docentes y los guarda en un archivo. Devuelve la ruta."""
    contenido = exportar(docentes, formato)
    ruta = f"{nombre_archivo}.{formato}"
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    return ruta
 