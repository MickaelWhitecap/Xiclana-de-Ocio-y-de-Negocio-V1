#!/usr/bin/env python3
"""Auditoría de calidad y candidatos a duplicado para Xiclana.

Modo deliberadamente no destructivo:
- Solo lee los JSON de fuentes.
- No modifica data.json ni los JSON de origen.
- No accede a Supabase ni publica fichas.
- El informe muestra candidatos y valores preferidos por campo; no aplica cambios.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
SOURCE_FILES = {
    "manuales": ("manuales.json", 90),
    "oficiales": ("oficiales.json", 82),
    "turismo": ("turismo.json", 78),
    "osm": ("datos/osm.json", 68),
}
FIELDS = ("n", "t", "c", "a", "p", "e", "w", "d", "s", "h", "m", "lat", "lon")
FIELD_PRIORITY = {
    "n": {"manuales": 94, "oficiales": 88, "turismo": 82, "osm": 72},
    "t": {"manuales": 94, "oficiales": 86, "turismo": 82, "osm": 78},
    "c": {"manuales": 92, "oficiales": 86, "turismo": 82, "osm": 78},
    "a": {"manuales": 88, "oficiales": 84, "turismo": 82, "osm": 74},
    "p": {"manuales": 88, "oficiales": 82, "turismo": 82, "osm": 70},
    "e": {"manuales": 88, "oficiales": 80, "turismo": 82, "osm": 70},
    "w": {"manuales": 86, "oficiales": 78, "turismo": 74, "osm": 72},
    "d": {"manuales": 82, "oficiales": 68, "turismo": 74, "osm": 62},
    "s": {"manuales": 82, "oficiales": 68, "turismo": 74, "osm": 62},
    "h": {"manuales": 82, "oficiales": 68, "turismo": 76, "osm": 72},
    "m": {"manuales": 80, "oficiales": 78, "turismo": 72, "osm": 68},
    "lat": {"manuales": 72, "oficiales": 68, "turismo": 68, "osm": 92},
    "lon": {"manuales": 72, "oficiales": 68, "turismo": 68, "osm": 92},
}
SOURCE_LABELS = {
    "manuales": "Ficha manual de Xiclana",
    "oficiales": "Ayuntamiento de Chiclana / datos abiertos",
    "turismo": "Turismo de Chiclana",
    "osm": "OpenStreetMap",
}
CONTACT_FIELDS = {"p", "e", "w"}
ADDRESS_FIELDS = {"a"}
COORD_FIELDS = {"lat", "lon"}


def normalize(value: object) -> str:
    text = unicodedata.normalize("NFKD", str(value or "").casefold())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(re.findall(r"[a-z0-9]+", text))


def tokens(value: object) -> set[str]:
    ignored = {"de", "del", "la", "las", "el", "los", "y", "en", "chiclana"}
    return {word for word in normalize(value).split() if word not in ignored}


def phone_digits(value: object) -> str:
    return "".join(re.findall(r"\d", str(value or "")))


def normalized_domain(value: object) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    parsed = urlsplit(raw if "://" in raw else "https://" + raw)
    host = (parsed.hostname or "").casefold()
    return host[4:] if host.startswith("www.") else host


def valid_value(field: str, value: object) -> bool:
    if value is None or value == "":
        return False
    if field == "p":
        digits = phone_digits(value)
        return 7 <= len(digits) <= 15
    if field == "e":
        return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", str(value).strip()))
    if field == "w":
        return normalized_domain(value) != ""
    if field == "lat":
        try:
            return -90 <= float(value) <= 90
        except (TypeError, ValueError):
            return False
    if field == "lon":
        try:
            return -180 <= float(value) <= 180
        except (TypeError, ValueError):
            return False
    if isinstance(value, str):
        return bool(value.strip())
    return True


def load_source(source: str, path: Path) -> list[dict]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("items", [])
    if not isinstance(data, list):
        raise ValueError(f"{path}: se esperaba una lista o un objeto con 'items'")
    result = []
    for index, original in enumerate(data):
        if not isinstance(original, dict):
            continue
        item = dict(original)
        item["_source"] = source
        item["_source_label"] = SOURCE_LABELS[source]
        item["_source_index"] = index
        result.append(item)
    return result


def same_coordinates(a: dict, b: dict, metres: float = 300) -> bool:
    try:
        lat1, lon1 = float(a["lat"]), float(a["lon"])
        lat2, lon2 = float(b["lat"]), float(b["lon"])
    except (KeyError, TypeError, ValueError):
        return False
    # Equirectangular approximation is sufficient for a small local comparison radius.
    import math
    x = math.radians(lon2 - lon1) * math.cos(math.radians((lat1 + lat2) / 2))
    y = math.radians(lat2 - lat1)
    distance = 6371000 * math.sqrt(x * x + y * y)
    return distance <= metres


def name_similarity(a: object, b: object) -> float:
    na, nb = normalize(a), normalize(b)
    if not na or not nb:
        return 0.0
    sequence = difflib.SequenceMatcher(None, na, nb).ratio()
    ta, tb = tokens(a), tokens(b)
    jaccard = len(ta & tb) / len(ta | tb) if ta and tb else 0.0
    return max(sequence, jaccard)


def identity_signals(a: dict, b: dict) -> list[str]:
    signals = []
    pa, pb = phone_digits(a.get("p")), phone_digits(b.get("p"))
    if len(pa) >= 8 and pa == pb:
        signals.append("mismo_telefono")
    da, db = normalized_domain(a.get("w")), normalized_domain(b.get("w"))
    if da and da == db:
        signals.append("mismo_dominio")
    if normalize(a.get("e")) and normalize(a.get("e")) == normalize(b.get("e")):
        signals.append("mismo_correo")
    if same_coordinates(a, b):
        signals.append("coordenadas_cercanas")
    aa, ab = tokens(a.get("a")), tokens(b.get("a"))
    if aa and ab and len(aa & ab) / len(aa | ab) >= 0.5:
        signals.append("direccion_similar")
    return signals


def compare_records(a: dict, b: dict) -> dict | None:
    if a.get("t") and b.get("t") and a["t"] != b["t"]:
        return None
    similarity = name_similarity(a.get("n"), b.get("n"))
    signals = identity_signals(a, b)
    strong = any(x in signals for x in ("mismo_telefono", "mismo_dominio", "mismo_correo"))
    location_support = any(x in signals for x in ("coordenadas_cercanas", "direccion_similar"))
    exact_name = normalize(a.get("n")) == normalize(b.get("n")) and bool(normalize(a.get("n")))
    if not (strong or (similarity >= 0.88 and location_support) or (exact_name and location_support)):
        return None
    confidence = 96 if strong and (similarity >= 0.55 or location_support) else 90 if strong else 84 if exact_name else 75
    if len(signals) >= 2:
        confidence = min(99, confidence + 3)
    return {
        "name_similarity": round(similarity, 3),
        "confidence": confidence,
        "signals": signals,
        "decision": "possible_duplicate_review",
        "note": "Candidato de duplicado: no se fusiona ni se publica automáticamente.",
    }


def corroboration_count(records: list[dict], field: str, value: object) -> int:
    def comparable(v: object) -> str:
        if field == "p":
            return phone_digits(v)
        if field == "w":
            return normalized_domain(v)
        if field in COORD_FIELDS:
            try:
                return str(round(float(v), 5))
            except (TypeError, ValueError):
                return ""
        return normalize(v)
    wanted = comparable(value)
    if not wanted:
        return 0
    sources = {
        r["_source"] for r in records
        if r["_source"] and r.get(field) not in (None, "") and comparable(r.get(field)) == wanted
    }
    return max(0, len(sources) - 1)


def field_score(field: str, value: object, source: str, records: list[dict]) -> int:
    if not valid_value(field, value):
        return 0
    score = FIELD_PRIORITY.get(field, {}).get(source, 60)
    score += min(8, corroboration_count(records, field, value) * 4)
    if field == "n" and len(str(value).strip()) < 3:
        score -= 20
    if field in {"d", "s"} and len(str(value).strip()) < 12:
        score -= 5
    return max(0, min(100, score))


def choose_fields(records: list[dict]) -> dict:
    selected = {}
    for field in FIELDS:
        candidates = []
        for record in records:
            value = record.get(field)
            if not valid_value(field, value):
                continue
            score = field_score(field, value, record["_source"], records)
            candidates.append({
                "value": value,
                "source": record["_source"],
                "source_label": record["_source_label"],
                "score": score,
            })
        if candidates:
            candidates.sort(key=lambda item: (item["score"], len(str(item["value"]))), reverse=True)
            winner = candidates[0]
            selected[field] = {
                **winner,
                "alternatives": candidates[1:5],
                "selection_mode": "propuesta_no_aplicada",
            }
    return selected


def build_report() -> dict:
    all_records = []
    missing_sources = []
    for source, (relative_path, _) in SOURCE_FILES.items():
        path = ROOT / relative_path
        if not path.exists():
            missing_sources.append(relative_path)
            continue
        all_records.extend(load_source(source, path))

    # Group exact strong identifiers only. Similar names without a strong identifier
    # are reported as candidates, not merged into a single identity.
    pairs = []
    for i, left in enumerate(all_records):
        for right in all_records[i + 1:]:
            match = compare_records(left, right)
            if match:
                pairs.append({
                    "left": {
                        "name": left.get("n", ""),
                        "source": left["_source"],
                        "source_index": left["_source_index"],
                    },
                    "right": {
                        "name": right.get("n", ""),
                        "source": right["_source"],
                        "source_index": right["_source_index"],
                    },
                    **match,
                })

    # Field proposals are generated for each record plus only its direct matches.
    proposals = []
    for record in all_records:
        related = [record]
        for pair in pairs:
            left = pair["left"]
            right = pair["right"]
            is_left = left["source"] == record["_source"] and left["source_index"] == record["_source_index"]
            is_right = right["source"] == record["_source"] and right["source_index"] == record["_source_index"]
            if is_left or is_right:
                other = right if is_left else left
                related.extend(
                    item for item in all_records
                    if item["_source"] == other["source"] and item["_source_index"] == other["source_index"]
                )
        fields = choose_fields(related)
        if len(related) > 1 or any(not valid_value(f, record.get(f)) for f in ("p", "e", "w", "a")):
            proposals.append({
                "record": record.get("n", ""),
                "source": record["_source"],
                "source_index": record["_source_index"],
                "related_sources": sorted({r["_source"] for r in related}),
                "selected_fields": fields,
                "action": "review_or_candidate_update",
                "applied": False,
            })

    source_counts = Counter(r["_source"] for r in all_records)
    return {
        "mode": "dry_run_only",
        "generated_from_repository_files": True,
        "public_data_modified": False,
        "supabase_modified": False,
        "source_counts": dict(source_counts),
        "total_source_records": len(all_records),
        "potential_duplicate_pairs": len(pairs),
        "proposals_for_review": len(proposals),
        "missing_source_files": missing_sources,
        "thresholds": {
            "auto_publication_enabled": False,
            "duplicate_handling": "candidate_only_no_merge",
            "low_confidence_action": "review",
            "confidence_scale": "operational_score_not_statistical_probability",
        },
        "duplicate_candidates": pairs,
        "field_proposals": proposals,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="Opcional: guardar el informe en un archivo indicado; nunca escribe data.json.")
    args = parser.parse_args()
    try:
        report = build_report()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Error al generar el informe: {exc}", file=sys.stderr)
        return 1
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        output = Path(args.output)
        if output.resolve() == (ROOT / "data.json").resolve():
            print("Error: el informe no puede sobrescribir data.json.", file=sys.stderr)
            return 2
        output.write_text(rendered + "\n", encoding="utf-8")
        print(f"Informe de simulación guardado en {output}")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
