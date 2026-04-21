"""Parser simple de CFDI 4.0 / 3.3 XML. Extrae UUID, Emisor, Receptor, Total, Fecha."""
from __future__ import annotations
import xml.etree.ElementTree as ET
from decimal import Decimal
from datetime import datetime
from typing import Any


NS = {
    "cfdi": "http://www.sat.gob.mx/cfd/4",
    "cfdi3": "http://www.sat.gob.mx/cfd/3",
    "tfd": "http://www.sat.gob.mx/TimbreFiscalDigital",
}


def parse_cfdi_xml(xml_content: bytes | str) -> dict[str, Any]:
    if isinstance(xml_content, bytes):
        text = xml_content.decode("utf-8", errors="ignore")
    else:
        text = xml_content
    try:
        root = ET.fromstring(text)
    except ET.ParseError as e:
        raise ValueError(f"XML inválido: {e}")

    # Namespace detection (cfdi 4.0 o 3.3)
    tag = root.tag
    if "}" not in tag:
        raise ValueError("XML no parece CFDI (sin namespace)")
    ns = tag.split("}")[0].strip("{")

    def a(key):
        return root.attrib.get(key) or root.attrib.get(f"{{{ns}}}{key}")

    total = a("Total") or a("total") or "0"
    fecha = a("Fecha") or a("fecha")
    serie = a("Serie") or ""
    folio = a("Folio") or ""

    # Emisor
    emisor = root.find(f"{{{ns}}}Emisor")
    emisor_rfc = emisor.attrib.get("Rfc") if emisor is not None else None
    emisor_nombre = emisor.attrib.get("Nombre") if emisor is not None else None

    # Receptor
    receptor = root.find(f"{{{ns}}}Receptor")
    receptor_rfc = receptor.attrib.get("Rfc") if receptor is not None else None
    receptor_nombre = receptor.attrib.get("Nombre") if receptor is not None else None

    # Timbre Fiscal UUID
    complemento = root.find(f"{{{ns}}}Complemento")
    uuid_val = None
    if complemento is not None:
        for child in complemento.iter():
            if child.tag.endswith("TimbreFiscalDigital"):
                uuid_val = child.attrib.get("UUID")
                break

    try:
        total_dec = Decimal(total)
    except Exception:
        total_dec = Decimal("0")

    try:
        fecha_dt = datetime.fromisoformat(fecha) if fecha else None
    except Exception:
        fecha_dt = None

    return {
        "uuid": uuid_val,
        "serie": serie,
        "folio": folio,
        "fecha": fecha_dt,
        "total": total_dec,
        "emisor_rfc": emisor_rfc,
        "emisor_nombre": emisor_nombre,
        "receptor_rfc": receptor_rfc,
        "receptor_nombre": receptor_nombre,
    }
