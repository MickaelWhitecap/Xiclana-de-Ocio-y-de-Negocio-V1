# Segunda pasada de validación de candidatos

Fecha de análisis: 2026-10-24. Entrada: expediente de candidatos de captura pública y catálogo publicado de referencia de 1.013 fichas.

## Resultado general

Se han refinado las 214 propuestas iniciales. Ninguna se ha publicado automáticamente.

- **OpenRTA: 105** registros turísticos pendientes de comprobar vigencia y duplicados. Los 105 tienen el indicador `ind_pub_open_rta=S`; 83 son viviendas de uso turístico y 22 viviendas turísticas de alojamiento rural. El indicador no demuestra que la actividad siga vigente hoy. Las direcciones particulares se mantienen fuera de los materiales públicos.
- **Municipales: 32** registros revisados con una segunda comparación semántica contra el catálogo actual. El primer cotejo por similitud textual generaba falsos positivos (por ejemplo, asociar un skate park a un bar). La revisión refinada clasifica 10 como duplicados probables, 2 como posibles duplicados semánticos, 2 para revisar identidad, 1 para revisión manual y 17 como candidatas sin duplicado evidente. Estas 17 siguen sin estar confirmadas ni publicadas.
- **OSM: 77** candidatos refinados: 34 lugares/actividades que pueden merecer confirmación, 14 elementos puntuales, viviendas particulares o nombres genéricos que se excluyen de altas de fichas con la evidencia actual, y 29 que siguen en revisión manual.

## Reglas aplicadas

1. Coincidencia de nombre o proximidad no basta por sí sola para afirmar identidad.
2. Una ficha en OpenRTA no se incorpora automáticamente: revisar vigencia, tipo de alojamiento, duplicado y pertinencia local.
3. No exponer domicilios particulares de alojamientos.
4. Elementos OSM puntuales (fuentes de agua, obras de arte, etc.) y nombres genéricos no se tratan como fichas de negocio por defecto.
5. La similitud de texto entre categorías no relacionadas no se acepta como evidencia de duplicado. Una coincidencia debe ser coherente en nombre, función y, cuando exista, ubicación.
6. Los candidatos y descartes permanecen en el expediente de revisión para trazabilidad.

## Artefacto de revisión

El Excel de segunda pasada incluye:
- resumen;
- duplicados probables;
- cotejo municipal refinado;
- OpenRTA y campos relevantes para revisar vigencia;
- OSM filtrado;
- todas las 214 candidatas con decisión provisional y siguiente paso.

## Límites y protección de producción

Esta pasada es una clasificación conservadora, no una verificación individual en tiempo real de cada negocio. No se ha escrito en `data.json`, GitHub Pages, Supabase ni en la rama principal. No se ha modificado el repositorio original ni fusionado/publicado el PR. Cualquier alta requiere confirmar existencia/vigencia, categoría, ubicación pública apropiada y ausencia de duplicado.

## Siguiente lote de trabajo

Priorizar las 17 instalaciones municipales sin duplicado evidente, validar los 2 posibles duplicados semánticos y revisar las 2 identidades ambiguas. Después verificar las 34 candidatas OSM con etiquetas de lugar/actividad. Para OpenRTA, resolver vigencia y deduplicación antes de plantear altas, empezando por una comprobación por lote contra las fichas actuales y por fuentes oficiales accesibles.
