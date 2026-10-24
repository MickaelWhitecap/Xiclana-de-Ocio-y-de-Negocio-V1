# Primer cruce del catálogo público con las 1.013 fichas existentes

**Fecha de análisis:** 24 de octubre de 2026  
**Alcance:** solo lectura; no se modificaron la web pública, Supabase ni el catálogo de producción.

## Fuentes comparadas

- Catálogo existente: 1.013 fichas, recuperadas del artefacto de GitHub Pages de la ejecución del 23/10/2026.
- Captura pública unificada: 9.440 registros brutos.
- Candidatos comparables extraídos: 1.779 (1.571 de OpenStreetMap, 168 de OpenRTA y 40 filas de conjuntos municipales seleccionados).

No se cuentan las 6.204 filas del callejero como establecimientos. También se excluyen eventos y reservas del primer cruce de posibles fichas.

## Resultados preliminares

| Fuente | Coincidencia probable por nombre y proximidad | Nombre cercano a ficha existente | Coincidencia espacial con nombre distinto | Ambiguo | Sin coincidencia automática |
|---|---:|---:|---:|---:|---:|
| OpenStreetMap | 836 | 20 | 73 | 212 | 398 |
| OpenRTA | 0 | 0 | 19 | 44 | 105 |
| Municipal | 0 | 2 | 0 | 0 | 38 |

Notas:
- Para OpenStreetMap, «ambiguo» agrupa 87 nombres duplicados en el catálogo y 125 candidatos próximos a varias fichas.
- «Sin coincidencia automática» **no significa ficha nueva confirmada**. Puede deberse a variantes de nombre, coordenadas ausentes, coordenadas no comparables o diferencias entre el nombre turístico y el nombre comercial.
- OpenRTA publica parte de sus coordenadas en ETRS89 / UTM 30N (EPSG:25830); la comparación preliminar transforma esas coordenadas a latitud/longitud cuando la biblioteca de proyección está disponible.
- Las coincidencias automáticas son una cola de revisión, no una autorización para fusionar registros.

## Siguiente paso

Revisar primero las coincidencias espaciales probables, después los casos ambiguos y, por último, los candidatos sin coincidencia. Solo tras esa revisión se puede proponer un catálogo maestro deduplicado. No se incorpora ni se publica ninguna ficha automáticamente.

El CSV de trabajo generado fuera del repositorio contiene el detalle de los 1.779 candidatos y sus posibles coincidencias. Este documento registra únicamente los resultados agregados; no contiene el catálogo de producción.
