import unittest

from capturar_catalogo_publico import classify, normalize_element, normalize_openrta_record, _as_records, build_unified_records, overpass_query, license_allows_row_capture, _structured_resource_rows


class CatalogCaptureTests(unittest.TestCase):
    def test_normalizes_named_point_and_contact_fields(self):
        item = normalize_element({
            "type": "node",
            "id": 123,
            "lat": 36.42,
            "lon": -6.14,
            "tags": {
                "name": "Ejemplo",
                "shop": "bakery",
                "addr:street": "Calle Mayor",
                "addr:housenumber": "4",
                "addr:city": "Chiclana de la Frontera",
                "contact:phone": "956000000",
                "contact:email": "hola@example.org",
                "contact:website": "https://example.org",
                "opening_hours": "Mo-Fr 09:00-14:00",
            },
        })
        self.assertEqual(item["name"], "Ejemplo")
        self.assertEqual(item["category"], "Comercio")
        self.assertEqual(item["latitude"], 36.42)
        self.assertEqual(item["longitude"], -6.14)
        self.assertEqual(item["address"], "Calle Mayor, 4, Chiclana de la Frontera")
        self.assertEqual(item["phone"], "956000000")
        self.assertEqual(item["email"], "hola@example.org")
        self.assertEqual(item["website"], "https://example.org")
        self.assertEqual(item["opening_hours"], "Mo-Fr 09:00-14:00")
        self.assertEqual(item["license"], "ODbL 1.0; atribución y obligaciones de base de datos derivada aplicables")

    def test_classifies_common_categories(self):
        self.assertEqual(classify({"tourism": "hotel"}), "Turismo y alojamiento")
        self.assertEqual(classify({"parking": "surface"}), "Aparcamiento")
        self.assertEqual(classify({"healthcare": "doctor"}), "Salud y cuidados")
        self.assertEqual(classify({}), "Sin categoría asignada")

    def test_normalizes_official_openrta_tourism_record(self):
        item = normalize_openrta_record({
            "ID": 456, "Denominación": "Hotel de prueba",
            "Municipality": "CHICLANA DE LA FRONTERA", "Province": "CÁDIZ",
            "Direccion": "Calle Ejemplo, 2", "Telefono": "956123123",
            "Web": "https://example.org", "Grupo": "Hotel",
        })
        self.assertEqual(item["name"], "Hotel de prueba")
        self.assertEqual(item["municipality"], "CHICLANA DE LA FRONTERA")
        self.assertEqual(item["address"], "Calle Ejemplo, 2")
        self.assertEqual(item["source"], "Registro de Turismo de Andalucía (OpenRTA)")
        self.assertIn("CC BY 4.0", item["license"])
        self.assertTrue(item["source_url"].endswith("/456"))

    def test_openrta_records_accept_common_response_wrappers(self):
        self.assertEqual(_as_records({"data": [{"id": 1}]}), [{"id": 1}])
        self.assertEqual(_as_records([{"id": 2}]), [{"id": 2}])

    def test_unifies_all_source_record_types_without_losing_raw_data(self):
        report = {
            "entities": [{"name": "Panadería", "source": "OpenStreetMap", "raw_tags": {"shop": "bakery"}}],
            "official_tourism_candidates": [{"name": "Hotel", "source": "OpenRTA", "raw_record": {"ID": 9}}],
            "sources": {"municipal_open_data": {"source": "Portal municipal", "datasets": [
                {"title": "Mercados", "url": "https://example.org/dataset", "resources": [
                    {"name": "mercados.csv", "url": "https://example.org/mercados.csv", "license": "CC BY"}
                ]}
            ]}}
        }
        records = build_unified_records(report)
        self.assertEqual([r["record_type"] for r in records], [
            "place_candidate", "official_tourism_candidate", "municipal_dataset", "municipal_dataset_resource"
        ])
        self.assertEqual(records[0]["raw_tags"]["shop"], "bakery")
        self.assertEqual(records[1]["raw_record"]["ID"], 9)
        self.assertEqual(records[3]["url"], "https://example.org/mercados.csv")

    def test_query_is_scoped_to_chiclana_and_named_objects(self):
        query = overpass_query()
        self.assertIn('area["name"="Chiclana de la Frontera"]', query)
        self.assertIn('["name"]', query)
        self.assertIn('["parking"]', query)
        self.assertIn("out center tags;", query)

    def test_only_recognized_open_licenses_allow_row_capture(self):
        self.assertTrue(license_allows_row_capture("Creative Commons Attribution 4.0 International"))
        self.assertTrue(license_allows_row_capture("ODbL 1.0"))
        self.assertFalse(license_allows_row_capture("No identificada: comprobar antes de reutilizar"))
        self.assertFalse(license_allows_row_capture(""))

    def test_csv_resource_rows_are_captured_only_when_open_license_is_declared(self):
        import unittest.mock as mock
        import io
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, size=-1): return b"nombre;tipo\\nParking Central;aparcamiento\\n"
        with mock.patch("urllib.request.urlopen", return_value=Response()):
            rows, reason = _structured_resource_rows({
                "url": "https://example.org/parking.csv",
                "format": "CSV",
                "license": "CC BY 4.0",
            })
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["nombre"], "Parking Central")
        self.assertEqual(reason, "")
        rows, reason = _structured_resource_rows({
            "url": "https://example.org/parking.csv",
            "format": "CSV",
            "license": "No identificada",
        })
        self.assertEqual(rows, [])
        self.assertIn("Licencia", reason)


if __name__ == "__main__":
    unittest.main()
