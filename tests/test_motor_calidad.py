import unittest

import motor_calidad as mc


class MotorCalidadTests(unittest.TestCase):
    def test_normaliza_tildes_y_puntuacion(self):
        self.assertEqual(mc.normalize("Actividades Náuticas, Gurri!"), "actividades nauticas gurri")

    def test_dominio_ignora_www_y_esquema(self):
        self.assertEqual(mc.normalized_domain("https://www.ejemplo.es/ruta"), "ejemplo.es")
        self.assertEqual(mc.normalized_domain("ejemplo.es"), "ejemplo.es")

    def test_mismo_telefono_es_senal_fuerte(self):
        a = {"n": "Empresa A", "t": "negocio", "p": "956 123 456"}
        b = {"n": "Empresa distinta", "t": "negocio", "p": "+34 956123456"}
        result = mc.compare_records(a, b)
        self.assertIsNotNone(result)
        self.assertIn("mismo_telefono", result["signals"])

    def test_nombre_parecido_sin_prueba_no_fusiona(self):
        a = {"n": "Bar La Plaza", "t": "negocio", "a": ""}
        b = {"n": "Bar La Plasa", "t": "negocio", "a": ""}
        self.assertIsNone(mc.compare_records(a, b))

    def test_tipo_distinto_no_es_duplicado(self):
        a = {"n": "Mercado Central", "t": "ocio", "p": "956123456"}
        b = {"n": "Mercado Central", "t": "negocio", "p": "956123456"}
        self.assertIsNone(mc.compare_records(a, b))

    def test_puntuacion_prioriza_coordenadas_osm(self):
        records = [
            {"_source": "oficiales", "lat": 36.4, "lon": -6.2},
            {"_source": "osm", "lat": 36.40001, "lon": -6.20001},
        ]
        self.assertGreater(
            mc.field_score("lat", 36.40001, "osm", records),
            mc.field_score("lat", 36.4, "oficiales", records),
        )

    def test_no_considera_valido_un_telefono_imposible(self):
        self.assertFalse(mc.valid_value("p", "123"))

    def test_no_considera_valido_un_correo_mal_formado(self):
        self.assertFalse(mc.valid_value("e", "no-es-un-correo"))

    def test_informe_declara_modo_no_destructivo(self):
        report = mc.build_report()
        self.assertEqual(report["mode"], "dry_run_only")
        self.assertFalse(report["public_data_modified"])
        self.assertFalse(report["supabase_modified"])
        self.assertFalse(report["thresholds"]["auto_publication_enabled"])


if __name__ == "__main__":
    unittest.main()
