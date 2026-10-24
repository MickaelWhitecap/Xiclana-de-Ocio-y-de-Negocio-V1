# Primer cruce del catálogo público con las 1.013 fichas existentes

**Fecha de análisis:** 24 de octubre de 2026  
**Alcance:** solo lectura; no se modificaron la web pública, Supabase ni el catálogo de producción.

## Fuentes comparadas

- Catálogo existente: 1.013 fichas, recuperadas del artefacto de GitHub Pages de la ejecución del 23/10/2026.
- Captura pública unificada: 9.440 registros brutos.
- Candidatos comparables extraídos: 1.779 (1.571 de OpenStreetMap, 168 de OpenRTA y 40 filas de conjuntos municipales seleccionados).

No se cuentan las 6.204 filas del callejero como establecimientos. También se excluyen eventos y reservas del primer cruce de posibles fichas.

## Resultados preliminares

| Estado de comparación | OSM | OpenRTA | Municipal | Total |
|---|---:|---:|---:|---:|
| Coincidencia probable por nombre y ubicación | 836 | 0 | 0 | 836 |
| Nombre exacto; ubicación pendiente | 32 | 0 | 5 | 37 |
| Posible variante de nombre | 20 | 0 | 2 | 22 |
| Ficha cercana; nombre distinto | 73 | 19 | 0 | 92 |
| Nombre duplicado; ambiguo | 87 | 0 | 0 | 87 |
| Varias fichas cercanas; ambiguo | 125 | 44 | 0 | 169 |
| Sin coincidencia automática | 398 | 105 | 33 | 536 |
| **Total** | **1.571** | **168** | **40** | **1.779** |

## Interpretación y control de calidad

- Una coincidencia probable no autoriza por sí sola una fusión; debe verificarse que se trata del mismo establecimiento.
- «Sin coincidencia automática» no significa ficha nueva confirmada. Puede deberse a variantes de nombre, coordenadas ausentes o diferencias entre nombre comercial y denominación oficial.
- Ejemplo de coincidencia: «La Rana Verde» coincide con una ficha existente a 0 m; debe conservarse la ficha actual y no añadir un duplicado.
- Ejemplo de falso candidato: el elemento OSM llamado «public» tiene la etiqueta `amenity=toilets`; es un nombre genérico y no debe incorporarse como ficha con ese título. Se conserva solo como registro de origen para revisión/filtrado.
- OpenRTA publica parte de sus coordenadas en ETRS89 / UTM 30N (EPSG:25830); la comparación transforma esas coordenadas a latitud/longitud cuando la biblioteca de proyección está disponible.
- Los candidatos no se incorporan automáticamente. Toda coincidencia y toda posible novedad requiere revisión.

## Siguiente paso

La hoja de revisión separa coincidencias probables, casos ambiguos, candidatos sin coincidencia automática y nombres genéricos. Revisar esos grupos permite formar una propuesta de catálogo maestro sin alterar las 1.013 fichas existentes. No se publica ni se escribe en Supabase hasta que exista una lista de altas y fusiones revisada.
