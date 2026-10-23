# Captura exploratoria del catálogo público

## Objetivo

El script `capturar_catalogo_publico.py` hace una primera captura reproducible en modo lectura. No modifica `data.json`, los JSON de origen, la web pública ni Supabase.

## Fuentes incluidas en esta primera versión

1. **OpenStreetMap mediante Overpass API**: busca objetos con nombre y etiquetas relacionadas con comercio, hostelería, alojamiento, salud, educación, deporte, cultura, aparcamiento, movilidad, servicios y otros puntos de interés. Conserva la referencia OSM, coordenadas, etiquetas de contacto y licencia ODbL.
2. **Portal de Datos Abiertos de Chiclana (CKAN)**: descubre conjuntos de datos y recursos disponibles, registrando sus formatos y licencias declaradas. Esta fase inventaría los recursos; no importa automáticamente cada XLS/ODS ni da por supuesta su licencia de reutilización.

El script no hace scraping de Google Maps ni importa sus fichas. Google puede utilizarse para localizar una web oficial, pero cualquier uso de Places API requiere revisar antes sus condiciones vigentes, atribución, almacenamiento y costes.

## Ejecución local

Requiere Python 3.10 o posterior; solo utiliza la biblioteca estándar.

```bash
python capturar_catalogo_publico.py --output informe-captura-publica.json
```

Para probar solamente el catálogo municipal:

```bash
python capturar_catalogo_publico.py --skip-overpass --output informe-fuentes-municipales.json
```

Para probar solamente OpenStreetMap:

```bash
python capturar_catalogo_publico.py --skip-municipal --skip-openrta --output informe-osm.json
```

Para probar solo el registro turístico oficial:

```bash
python capturar_catalogo_publico.py --skip-overpass --skip-municipal --output informe-openrta.json
```

Respeta los límites de los servicios, no ejecutes repetidamente consultas grandes y conserva la atribución a OpenStreetMap. Si Overpass está saturado, vuelve a intentarlo más tarde.

## Salida

El JSON incluye:
- candidatos turísticos oficiales de OpenRTA en `official_tourism_candidates`, separados de los objetos OSM;
- fuente y licencia de OpenRTA, con atribución a la Junta de Andalucía;
- fecha y hora UTC de la captura;
- número de objetos con nombre por categoría;
- campos públicos disponibles (nombre, categoría, dirección, teléfono, correo, web, horario y coordenadas);
- identificador y enlace de origen;
- recursos municipales descubiertos y licencia declarada;
- errores y limitaciones de la ejecución.

## Próximas fases necesarias

- Descargar y procesar, de manera selectiva, los recursos municipales cuya licencia permita la reutilización prevista.
- Incorporar el Registro de Turismo de Andalucía (OpenRTA), cuya ficha de datos declara licencia CC BY 4.0 y actualización diaria; verificar el endpoint y los campos antes de integrarlo.
- Comparar candidatos con las 1.013 fichas actuales y los overrides de Supabase en modo de solo lectura.
- Añadir resolución de web oficial y extracción limitada desde páginas propias de negocios, respetando robots.txt, términos de uso y límites de petición.
- Producir un informe de cobertura, duplicados probables, campos ausentes y conflictos.

**No se publican cambios automáticamente.** Un registro ausente de una fuente no se considera cerrado; posibles duplicados son candidatos para revisión, no fusiones. Las correcciones manuales protegidas deben conservar prioridad.
