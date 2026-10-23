import unittest

from capturar_catalogo_publico import classify, normalize_element, normalize_openrta_record, _as_records, overpass_query


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
            "ID": 456, "Denominacion": "Hotel de prueba",
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

    def test_query_is_scoped_to_chiclana_and_named_objects(self):
        query = overpass_query()
        self.assertIn('area["name"="Chiclana de la Frontera"]', query)
        self.assertIn('["name"]', query)
        self.assertIn('["parking"]', query)
        self.assertIn("out center tags;", query)


if __name__ == "__main__":
    unittest.main()
