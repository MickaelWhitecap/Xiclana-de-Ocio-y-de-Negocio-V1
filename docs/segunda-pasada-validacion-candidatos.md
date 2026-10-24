# Segunda pasada de validación de candidatos

Fecha de análisis: 2026-10-24. Entrada: expediente de candidatos de captura pública y catálogo publicado de referencia de 1.013 fichas.

## Resultado

Esta pasada refina las 214 propuestas iniciales, sin convertir ninguna automáticamente en ficha publicada.

- **OpenRTA: 105** registros turísticos quedan pendientes de comprobar vigencia y duplicados. Los 105 tienen el indicador `ind_pub_open_rta=S`; 83 son viviendas de uso turístico y 22 viviendas turísticas de alojamiento rural. Ese indicador no demuestra que la actividad siga vigente hoy. No se trasladan direcciones particulares al expediente de revisión.
- **Municipales: 32** instalaciones cotejadas nominalmente contra el catálogo existente: 9 duplicados probables que no deben darse de alta otra vez; 1 posible duplicado que requiere comprobación; 22 candidatas para confirmar con el Ayuntamiento, revisando nombre alternativo, ubicación y si la instalación sigue en servicio.
- **OSM: 77** candidatos refinados: 34 lugares/actividades que pueden merecer confirmación, 14 elementos puntuales, viviendas particulares o nombres genéricos que se excluyen de altas de fichas con la evidencia actual, y 29 que siguen en revisión manual.

## Reglas aplicadas

1. Coincidencia de nombre o proximidad no basta por sí sola para afirmar identidad.
2. Una ficha en OpenRTA no se incorpora automáticamente: revisar vigencia, tipo de alojamiento, duplicado y pertinencia local.
3. No exponer domicilios particulares de alojamientos.
4. Elementos OSM puntuales (fuentes de agua, obras de arte, etc.) y nombres genéricos no se tratan como fichas de negocio por defecto.
5. Las coincidencias municipales fuertes se etiquetan como duplicados probables; no se sobrescribe la ficha existente ni se enriquecen campos sin validación.
6. Los candidatos y los descartes permanecen en el expediente de revisión para trazabilidad.

## Artefacto de revisión

El Excel `validacion-segunda-pasada-xiclana.xlsx` contiene:
- resumen;
- duplicados probables;
- cotejo municipal;
- OpenRTA y campos relevantes para revisar vigencia;
- OSM filtrado;
- todas las 214 candidatas con decisión provisional y siguiente paso.

## Límites y protección de producción

Esta pasada es una clasificación conservadora, no una verificación individual en tiempo real de cada negocio. No se ha escrito en `data.json`, GitHub Pages, Supabase ni en la rama principal. No se ha modificado el repositorio original ni fusionado/publicado el PR. Cualquier alta requiere confirmar existencia/vigencia, categoría, ubicación pública apropiada y ausencia de duplicado.

## Siguiente lote de trabajo

Priorizar las 22 instalaciones municipales candidatas, porque tienen una fuente municipal directa; después verificar las 34 candidatas OSM con etiquetas de lugar/actividad. Para OpenRTA, resolver vigencia y deduplicación antes de plantear altas, empezando por una comprobación por lote contra las fichas actuales y por fuentes oficiales accesibles.
