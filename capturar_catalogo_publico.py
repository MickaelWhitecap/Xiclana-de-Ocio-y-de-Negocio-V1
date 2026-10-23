#!/usr/bin/env python3
"""Captura exploratoria de entidades públicas de Chiclana. Solo genera un informe separado.

Fuentes iniciales:
- OpenStreetMap vía Overpass API (ODbL; atribución obligatoria).
- Portal municipal CKAN: descubre conjuntos y recursos, sin asumir que cada licencia
  permite reutilización comercial.
No consulta ni copia fichas de Google Maps. No escribe en data.json ni en Supabase.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
CKAN_URL = "https://datosabiertos.chiclana.es/api/3/action/package_search"
OPENRTA_SEARCH_URL = "https://datos.juntadeandalucia.es/api/v0/openrta/search"
OPENRTA_LICENSE = "CC BY 4.0; atribución a la Junta de Andalucía"
USER_AGENT = "XiclanaCatalogAudit/0.1 (public-data discovery; contact via project repository)"
TAGS = (
    "amenity", "shop", "tourism", "leisure", "craft", "office", "healthcare",
    "education", "sport", "historic", "natural", "public_transport", "parking",
    "emergency", "club", "religion", "man_made", "industrial", "service",
    "railway", "aeroway", "power", "barrier", "waterway", "route",
)
CONTACT_TAGS = {
    "phone": ("phone", "contact:phone"),
    "email": ("email", "contact:email"),
    "website": ("website", "contact:website", "url"),
    "opening_hours": ("opening_hours",),
    "address": ("addr:full",),
}
CATEGORY_MAP = {
    "shop": "Comercio",
    "amenity": "Servicios y equipamientos",
    "tourism": "Turismo y alojamiento",
    "leisure": "Ocio y deporte",
    "craft": "Oficios y talleres",
    "office": "Servicios profesionales",
    "healthcare": "Salud y cuidados",
    "education": "Educación",
    "sport": "Deporte",
    "historic": "Patrimonio",
    "natural": "Naturaleza",
    "public_transport": "Transporte público",
    "parking": "Aparcamiento",
    "emergency": "Emergencias",
    "club": "Clubes y asociaciones",
    "religion": "Lugares de culto",
    "industrial": "Industria",
    "railway": "Ferrocarril",
    "aeroway": "Transporte aéreo",
    "power": "Energía",
    "waterway": "Agua y litoral",
    "route": "Rutas",
}


def request_json(url: str, data: bytes | None = None, timeout: int = 90, content_type: str | None = None):
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def overpass_query() -> str:
    selectors = "\n".join(
        f'  nwr(area.a)["name"]["{tag}"];' for tag in TAGS
    )
    return (
        '[out:json][timeout:80];\n'
        'area["name"="Chiclana de la Frontera"]["boundary"="administrative"]'
        '["admin_level"~"^(7|8)$"]->.a;\n'
        '(\n' + selectors + '\n);\nout center tags;'
    )


def first_tag(tags: dict, keys: tuple[str, ...]) -> str:
    for key in keys:
        value = tags.get(key)
        if value:
            return str(value).strip()
    return ""


def classify(tags: dict) -> str:
    for key in TAGS:
        if tags.get(key):
            return CATEGORY_MAP.get(key, key.replace("_", " ").capitalize())
    return "Sin categoría asignada"


def normalize_element(element: dict) -> dict:
    tags = element.get("tags") or {}
    center = element.get("center") or {}
    lat = element.get("lat", center.get("lat"))
    lon = element.get("lon", center.get("lon"))
    address = first_tag(tags, ("addr:full",))
    if not address:
        pieces = [
            tags.get("addr:street", ""),
            tags.get("addr:housenumber", ""),
            tags.get("addr:postcode", ""),
            tags.get("addr:city", ""),
        ]
        address = ", ".join(str(x) for x in pieces if x)
    category_key = next((key for key in TAGS if tags.get(key)), "")
    return {
        "name": tags.get("name", ""),
        "category": classify(tags),
        "category_tag": category_key,
        "osm_type": element.get("type", ""),
        "osm_id": element.get("id"),
        "latitude": lat,
        "longitude": lon,
        "address": address,
        "phone": first_tag(tags, CONTACT_TAGS["phone"]),
        "email": first_tag(tags, CONTACT_TAGS["email"]),
        "website": first_tag(tags, CONTACT_TAGS["website"]),
        "opening_hours": first_tag(tags, CONTACT_TAGS["opening_hours"]),
        "source": "OpenStreetMap",
        "source_url": f'https://www.openstreetmap.org/{element.get("type", "")}/{element.get("id", "")}',
        "license": "ODbL 1.0; atribución y obligaciones de base de datos derivada aplicables",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "raw_tags": tags,
    }



MAX_RESOURCE_BYTES = 5 * 1024 * 1024
MAX_ROWS_PER_RESOURCE = 5000


def license_allows_row_capture(license_text: str) -> bool:
    """Permite capturar filas solo cuando el metadato declara una licencia abierta reconocible."""
    value = (license_text or "").casefold()
    if not value or "no identificada" in value or "unknown" in value or "all rights reserved" in value:
        return False
    # No aceptar licencias Creative Commons con restricciones NC/ND, ni una mención genérica.
    if any(marker in value for marker in ("-nc", " nc", "noncommercial", "no comercial", "-nd", " nd", "no derivatives")):
        return False
    markers = ("cc by 4.0", "cc by 3.0", "cc by 2.0", "cc0", "odbl", "open data commons", "public domain", "dominio público")
    return any(marker in value for marker in markers)


def _decode_csv(data: bytes) -> list[dict]:
    import csv
    import io
    sample = data[:8192].decode("utf-8-sig", errors="replace")
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\\t|")
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig", errors="replace")), dialect=dialect)
    return [dict(row) for _, row in zip(range(MAX_ROWS_PER_RESOURCE), reader)]


def _structured_resource_rows(resource: dict) -> tuple[list[dict], str]:
    """Descarga CSV/JSON/GeoJSON pequeño; no ejecuta contenido ni procesa formatos binarios."""
    url = str(resource.get("url") or "").strip()
    fmt = str(resource.get("format") or "").casefold().strip()
    if not url.startswith("https://"):
        return [], "URL no HTTPS o ausente"
    if not license_allows_row_capture(str(resource.get("license") or "")):
        return [], "Licencia no reconocida como abierta; solo se conserva el metadato"
    path_fmt = urllib.parse.urlparse(url).path.casefold().rsplit(".", 1)[-1] if "." in urllib.parse.urlparse(url).path else ""
    kind = fmt if fmt else path_fmt
    if kind in ("geojson", "geo json", "json", "application/json"):
        kind = "json" if kind != "geojson" else "geojson"
    elif kind in ("csv", "text/csv", "comma-separated values"):
        kind = "csv"
    else:
        return [], "Formato no compatible en esta fase"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/csv, application/json, application/geo+json"})
        with urllib.request.urlopen(req, timeout=25) as response:
            raw = response.read(MAX_RESOURCE_BYTES + 1)
        if len(raw) > MAX_RESOURCE_BYTES:
            return [], "Recurso supera el límite de 5 MiB"
        if kind == "csv":
            rows = _decode_csv(raw)
        else:
            payload = json.loads(raw.decode("utf-8-sig"))
            if isinstance(payload, dict) and payload.get("type") == "FeatureCollection":
                rows = []
                for feature in payload.get("features", [])[:MAX_ROWS_PER_RESOURCE]:
                    if not isinstance(feature, dict):
                        continue
                    row = dict(feature.get("properties") or {})
                    geometry = feature.get("geometry")
                    if geometry is not None:
                        row["_geometry"] = geometry
                    rows.append(row)
            elif isinstance(payload, list):
                rows = [x if isinstance(x, dict) else {"value": x} for x in payload[:MAX_ROWS_PER_RESOURCE]]
            elif isinstance(payload, dict):
                for key in ("results", "records", "data", "items"):
                    if isinstance(payload.get(key), list):
                        rows = [x if isinstance(x, dict) else {"value": x} for x in payload[key][:MAX_ROWS_PER_RESOURCE]]
                        break
                else:
                    rows = [payload]
            else:
                rows = []
        return rows, ""
    except Exception as exc:
        return [], f"{type(exc).__name__}: {exc}"


def capture_municipal_resource_rows(datasets: list[dict]) -> tuple[list[dict], list[dict]]:
    rows, audit = [], []
    for dataset in datasets:
        for resource in dataset.get("resources", []):
            source_resource = {**resource, "license": resource.get("license") or dataset.get("license", "")}
            data_rows, skip_reason = _structured_resource_rows(source_resource)
            audit.append({
                "dataset_title": dataset.get("title", ""),
                "resource_name": resource.get("name", ""),
                "resource_url": resource.get("url", ""),
                "license": source_resource.get("license", ""),
                "rows_captured": len(data_rows),
                "status": "captured" if data_rows else "skipped_or_empty",
                "reason": skip_reason,
            })
            for index, row in enumerate(data_rows, start=1):
                rows.append({
                    "record_type": "municipal_dataset_record",
                    "source": "Portal de Datos Abiertos del Ayuntamiento de Chiclana",
                    "dataset_title": dataset.get("title", ""),
                    "dataset_url": dataset.get("url", ""),
                    "resource_name": resource.get("name", ""),
                    "resource_url": resource.get("url", ""),
                    "resource_id": resource.get("resource_id", ""),
                    "row_number": index,
                    "license": source_resource.get("license", ""),
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "raw_record": row,
                })
    return rows, audit


def discover_municipal_datasets() -> dict:
    url = CKAN_URL + "?" + urllib.parse.urlencode({"q": "Chiclana", "rows": 100})
    payload = request_json(url, timeout=30)
    if not payload.get("success"):
        raise RuntimeError("El portal municipal CKAN no devolvió success=true")
    results = payload.get("result", {}).get("results", [])
    datasets = []
    for ds in results:
        resources = []
        for resource in ds.get("resources", []):
            resources.append({
                "name": resource.get("name", ""),
                "format": resource.get("format", ""),
                "url": resource.get("url", ""),
                "resource_id": resource.get("id", ""),
                "license": ds.get("license_title") or ds.get("license_id") or "No identificada: comprobar antes de reutilizar",
            })
        datasets.append({
            "title": ds.get("title", ""),
            "name": ds.get("name", ""),
            "url": ds.get("url") or ("https://datosabiertos.chiclana.es/dataset/" + str(ds.get("name", ""))),
            "license": ds.get("license_title") or ds.get("license_id") or "No identificada: comprobar antes de reutilizar",
            "resources": resources,
        })
    row_records, resource_audit = capture_municipal_resource_rows(datasets)
    return {
        "source": "Portal de Datos Abiertos del Ayuntamiento de Chiclana",
        "catalog_url": "https://datosabiertos.chiclana.es/dataset/",
        "api_url": CKAN_URL,
        "datasets_found": len(datasets),
        "datasets": datasets,
        "resource_records": row_records,
        "resource_capture_audit": resource_audit,
        "resource_rows_captured": len(row_records),
    }


def capture_overpass() -> list[dict]:
    body = urllib.parse.urlencode({"data": overpass_query()}).encode()
    payload = request_json(OVERPASS_URL, data=body, timeout=120)
    return [normalize_element(e) for e in payload.get("elements", []) if (e.get("tags") or {}).get("name")]



def _as_records(payload) -> list[dict]:
    """Acepta las formas habituales de respuesta de la API sin asumir un único envoltorio."""
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("data", "results", "result", "items", "records", "features"):
        value = payload.get(key)
        if isinstance(value, list):
            if key == "features":
                return [x.get("properties", x) for x in value if isinstance(x, dict)]
            return [x for x in value if isinstance(x, dict)]
        if isinstance(value, dict):
            nested = _as_records(value)
            if nested:
                return nested
    # Algunos servicios devuelven un registro o un objeto indexado por identificador.
    if any(k in payload for k in ("municipality", "municipality_name", "municipio", "municipalityName")):
        return [payload]
    return []


def _field(record: dict, *names: str) -> str:
    """Obtiene el primer campo no vacío, tolerando tildes, mayúsculas y espacios."""
    def key(value: object) -> str:
        plain = unicodedata.normalize("NFKD", str(value).casefold())
        plain = "".join(ch for ch in plain if not unicodedata.combining(ch))
        return re.sub(r"[^a-z0-9]", "", plain)
    normalized = {key(k): v for k, v in record.items()}
    for name in names:
        value = normalized.get(key(name))
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def normalize_openrta_record(record: dict) -> dict:
    name = _field(record, "name", "denomination", "denominacion", "nombre", "business_name", "commercial_name")
    municipality = _field(record, "municipality", "municipality_name", "municipalityName", "municipio", "locality")
    province = _field(record, "province", "province_name", "provincia")
    bid = _field(record, "id", "bid", "registration_number", "numero_registro", "registration")
    latitude = _field(record, "latitude", "lat", "coord_latitude", "y")
    longitude = _field(record, "longitude", "lon", "lng", "coord_longitude", "x")
    address = _field(record, "address", "direccion", "domicilio", "street_address")
    phone = _field(record, "phone", "telephone", "telefono", "contact_phone")
    website = _field(record, "website", "web", "url", "pagina_web")
    category = _field(record, "object_type", "object_type_name", "tipo_objeto", "group", "grupo", "category", "categoria")
    return {
        "name": name,
        "category": "Turismo y alojamiento",
        "official_category": category,
        "registration_id": bid,
        "municipality": municipality,
        "province": province,
        "address": address,
        "phone": phone,
        "website": website,
        "latitude": latitude,
        "longitude": longitude,
        "source": "Registro de Turismo de Andalucía (OpenRTA)",
        "source_url": f"https://datos.juntadeandalucia.es/api/v0/openrta/{urllib.parse.quote(bid)}" if bid.isdigit() else "https://datos.juntadeandalucia.es/api/v0/openrta/docs",
        "license": OPENRTA_LICENSE,
        "raw_record": record,
    }


def capture_openrta() -> list[dict]:
    """Busca en OpenRTA por municipio; nunca importa directamente a la web."""
    body = {
        "municipalities": "CHICLANA DE LA FRONTERA",
        "provinces": "CÁDIZ",
        "format": "json",
        "size": 0,
        "mode": "ASC",
        "order_by": "data.ID",
    }
    payload = request_json(
        OPENRTA_SEARCH_URL,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        timeout=90,
        content_type="application/json",
    )
    records = _as_records(payload)
    candidates = [normalize_openrta_record(x) for x in records]
    # Defensa adicional: la respuesta debe corresponder al municipio solicitado.
    return [
        x for x in candidates
        if "CHICLANA" in (x["municipality"] + " " + x["province"]).upper()
        and x["name"]
    ]


def build_unified_records(report: dict) -> list[dict]:
    """Reúne en una lista común todos los registros capturados, preservando el dato original."""
    records = []
    for item in report.get("entities", []):
        records.append({"record_type": "place_candidate", **item})
    for item in report.get("official_tourism_candidates", []):
        records.append({"record_type": "official_tourism_candidate", **item})
    municipal = report.get("sources", {}).get("municipal_open_data", {})
    for dataset in municipal.get("datasets", []):
        records.append({
            "record_type": "municipal_dataset",
            "source": municipal.get("source", "Portal municipal CKAN"),
            **dataset,
        })
        for resource in dataset.get("resources", []):
            records.append({
                "record_type": "municipal_dataset_resource",
                "source": municipal.get("source", "Portal municipal CKAN"),
                "dataset_title": dataset.get("title", ""),
                "dataset_url": dataset.get("url", ""),
                **resource,
            })
    records.extend(municipal.get("resource_records", []))
    return records

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="informe-captura-publica.json",
                        help="Informe separado de los datos públicos (no usar data.json)")
    parser.add_argument("--skip-overpass", action="store_true",
                        help="Consultar solo el catálogo municipal de conjuntos de datos")
    parser.add_argument("--skip-municipal", action="store_true",
                        help="Omitir el catálogo municipal CKAN")
    parser.add_argument("--skip-openrta", action="store_true",
                        help="Omitir el Registro de Turismo de Andalucía")
    parser.add_argument("--delay", type=float, default=2.0,
                        help="Pausa entre fuentes (segundos)")
    args = parser.parse_args()
    output = Path(args.output)
    if output.name.casefold() == "data.json":
        print("ERROR: el informe nunca puede sobrescribir data.json", file=sys.stderr)
        return 2

    report = {
        "report_type": "exploratory_public_data_capture",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "municipality": "Chiclana de la Frontera, Cádiz, España",
        "mode": "read_only",
        "production_data_modified": False,
        "supabase_modified": False,
        "google_maps_scraping": False,
        "limitations": [
            "La cobertura OSM depende de los datos cartografiados por la comunidad y no es exhaustiva.",
            "Solo se capturan filas municipales en CSV/JSON/GeoJSON con licencia abierta reconocible; otros recursos quedan inventariados con motivo de omisión.",
            "No se infiere cierre por ausencia de un establecimiento en una fuente.",
            "Los resultados son candidatos a comparar, no fichas aprobadas ni publicaciones automáticas.",
        ],
        "sources": {},
        "entities": [],
        "official_tourism_candidates": [],
        "records": [],
        "counts_by_category": {},
    }
    errors = []
    if not args.skip_overpass:
        try:
            entities = capture_overpass()
            # Deduplicate repeated OSM objects only by exact source identifier.
            unique = {(x["osm_type"], x["osm_id"]): x for x in entities}
            report["entities"] = list(unique.values())
            report["sources"]["OpenStreetMap"] = {
                "url": "https://www.openstreetmap.org/",
                "query_url": OVERPASS_URL,
                "raw_named_objects": len(entities),
                "unique_named_objects": len(unique),
                "license": "ODbL 1.0",
                "attribution": "© OpenStreetMap contributors",
            }
        except Exception as exc:
            errors.append({"source": "OpenStreetMap/Overpass", "error": str(exc)})
        if not args.skip_municipal:
            time.sleep(max(0, args.delay))
    if not args.skip_municipal:
        try:
            report["sources"]["municipal_open_data"] = discover_municipal_datasets()
        except Exception as exc:
            errors.append({"source": "Portal municipal CKAN", "error": str(exc)})
    if not args.skip_openrta:
        try:
            tourism = capture_openrta()
            report["official_tourism_candidates"] = tourism
            report["sources"]["OpenRTA"] = {
                "url": "https://datos.juntadeandalucia.es/api/v0/openrta/docs",
                "dataset_url": "https://www.juntadeandalucia.es/datosabiertos/portal/dataset/openrta",
                "records_found_for_municipality": len(tourism),
                "license": OPENRTA_LICENSE,
                "attribution": "Junta de Andalucía — Registro de Turismo de Andalucía (OpenRTA)",
            }
        except Exception as exc:
            errors.append({"source": "OpenRTA", "error": str(exc)})
    report["records"] = build_unified_records(report)
    report["records_found"] = len(report["records"])
    report["counts_by_record_type"] = dict(Counter(x.get("record_type", "unknown") for x in report["records"]))
    report["counts_by_category"] = dict(Counter(x["category"] for x in report["entities"]))
    report["entities_found"] = len(report["entities"])
    report["errors"] = errors
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output),
        "entities_found": report["entities_found"],
        "counts_by_category": report["counts_by_category"],
        "municipal_datasets_found": report.get("sources", {}).get("municipal_open_data", {}).get("datasets_found"),
        "municipal_resource_rows_captured": report.get("sources", {}).get("municipal_open_data", {}).get("resource_rows_captured", 0),
        "openrta_candidates_found": len(report.get("official_tourism_candidates", [])),
        "records_found": report.get("records_found", 0),
        "errors": errors,
        "production_data_modified": False,
        "supabase_modified": False,
    }, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
