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
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
CKAN_URL = "https://datosabiertos.chiclana.es/api/3/action/package_search"
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


def request_json(url: str, data: bytes | None = None, timeout: int = 90):
    req = urllib.request.Request(
        url, data=data, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
    )
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
    return {
        "source": "Portal de Datos Abiertos del Ayuntamiento de Chiclana",
        "catalog_url": "https://datosabiertos.chiclana.es/dataset/",
        "api_url": CKAN_URL,
        "datasets_found": len(datasets),
        "datasets": datasets,
    }


def capture_overpass() -> list[dict]:
    body = urllib.parse.urlencode({"data": overpass_query()}).encode()
    payload = request_json(OVERPASS_URL, data=body, timeout=120)
    return [normalize_element(e) for e in payload.get("elements", []) if (e.get("tags") or {}).get("name")]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="informe-captura-publica.json",
                        help="Informe separado de los datos públicos (no usar data.json)")
    parser.add_argument("--skip-overpass", action="store_true",
                        help="Consultar solo el catálogo municipal de conjuntos de datos")
    parser.add_argument("--skip-municipal", action="store_true",
                        help="Consultar solo OpenStreetMap")
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
            "Los recursos municipales se inventarían primero; cada recurso debe revisarse por licencia antes de importar sus filas.",
            "No se infiere cierre por ausencia de un establecimiento en una fuente.",
            "Los resultados son candidatos a comparar, no fichas aprobadas ni publicaciones automáticas.",
        ],
        "sources": {},
        "entities": [],
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
        "errors": errors,
        "production_data_modified": False,
        "supabase_modified": False,
    }, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
