# Primer cruce del catálogo público con las 1.013 fichas existentes

**Fecha de análisis:** 24 de octubre de 2026  
**Alcance:** solo lectura y propuesta de trabajo. No se modificaron la web pública, Supabase ni el catálogo de producción.

## Fuentes comparadas

- Catálogo existente: 1.013 fichas, recuperadas del artefacto de GitHub Pages.
- Captura pública unificada: 9.440 registros brutos; no representan establecimientos únicos.
- Candidatos iniciales comparables: 1.779 (1.571 OSM, 168 OpenRTA y 40 filas municipales seleccionadas).

## Primer resultado del comparador

| Estado inicial | OSM | OpenRTA | Municipal | Total |
|---|---:|---:|---:|---:|
| Coincidencia probable por nombre y ubicación | 836 | 0 | 0 | 836 |
| Nombre exacto; ubicación pendiente | 32 | 0 | 5 | 37 |
| Posible variante de nombre | 20 | 0 | 2 | 22 |
| Ficha cercana; nombre distinto | 73 | 19 | 0 | 92 |
| Nombre repetido; ambiguo | 87 | 0 | 0 | 87 |
| Varias fichas cercanas; ambiguo | 125 | 44 | 0 | 169 |
| Sin coincidencia automática | 398 | 105 | 33 | 536 |
| **Total** | **1.571** | **168** | **40** | **1.779** |

## Segundo paso: triage conservador

El análisis de las etiquetas originales de OpenStreetMap detecta elementos que no deben tratarse como fichas de negocio, especialmente paradas de transporte público. Tras aplicar reglas conservadoras, el libro de trabajo propone:

- **900** coincidencias probables o coincidencias de ubicación exacta que no deben generar duplicados.
- **351** registros excluidos del flujo de altas por ser paradas/transporte público o por tener un nombre genérico.
- **214** propuestas de alta para contrastar: 105 registros turísticos oficiales, 32 instalaciones municipales y 77 entidades OSM con etiquetas de lugar/actividad y sin coincidencia automática.
- **314** casos que requieren revisión adicional por ambigüedad o falta de evidencia suficiente.

Estas categorías son recomendaciones de triage, no una certificación de que un negocio esté activo. La coincidencia por nombre y ubicación no autoriza a sobrescribir la ficha existente; la ausencia de coincidencia no demuestra que la ficha sea nueva.

## Casos de control

- «La Rana Verde» coincide con una ficha existente a 0 m; no se debe añadir otra.
- El elemento OSM «public» con `amenity=toilets` es un aseo público, no una ficha comercial con ese nombre.
- Los registros de OpenRTA pueden representar alojamientos particulares; hay que comprobar actividad, duplicidad y pertinencia para el directorio antes de darlos de alta.
- Los datos de OSM se usan bajo ODbL 1.0, con sus obligaciones de atribución y bases de datos derivadas; los registros OpenRTA, bajo CC BY 4.0 con atribución a la Junta de Andalucía. Los conjuntos municipales solo se capturan cuando su licencia está identificada como reutilizable.

## Siguiente paso

El archivo de revisión separa coincidencias, exclusiones, propuestas y casos manuales. Las altas están **preparadas como propuestas**, pero no se han escrito en el catálogo público ni en Supabase. La incorporación definitiva requiere revisar las propuestas y aplicar los cambios de forma controlada.
