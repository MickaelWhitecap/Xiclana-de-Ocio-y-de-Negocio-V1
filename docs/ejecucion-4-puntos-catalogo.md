# Ejecución de los cuatro pasos de revisión del catálogo

**Fecha:** 24 de octubre de 2026  
**Estado:** propuesta preparada en rama de desarrollo; sin publicación.

## 1. Resolver

Se separaron las coincidencias de forma conservadora. 900 candidatos se clasifican como coincidencias probables o coincidencias exactas de ubicación y no deben crear una ficha duplicada. La ficha existente se conserva como referencia; cualquier enriquecimiento de teléfono, web, dirección o descripción se hará solo después de comprobar campo por campo la fuente y su fecha.

## 2. Revisar

Se separaron 351 elementos que no deben pasar al flujo de altas: 347 paradas/elementos de transporte público y 4 nombres genéricos. Se detectaron además 314 casos ambiguos o insuficientemente documentados que permanecen en la cola manual. Los elementos excluidos se conservan en los datos de origen; no se borran de la fuente.

## 3. Confirmar

Se prepararon 214 propuestas para contrastar:
- 105 candidatos del Registro de Turismo de Andalucía (OpenRTA).
- 32 instalaciones deportivas/culturales de datos municipales.
- 77 entidades de OpenStreetMap con etiquetas de lugar o actividad.

La clasificación de «propuesta» no certifica que el establecimiento siga abierto ni que no exista bajo otro nombre. Antes del alta hay que comprobar identidad, vigencia, dirección, categoría, pertinencia y licencia/atribución. Los alojamientos particulares requieren especial cuidado para evitar convertir domicilios privados en fichas innecesarias.

## 4. Incorporar

Las 214 propuestas se han incorporado al **libro de trabajo de revisión**, separadas de las 1.013 fichas existentes. No se han añadido a `data.json`, no se han enviado a Supabase y no se han publicado en GitHub Pages. Este es el límite seguro de incorporación automática con la evidencia actual: no hay confirmación humana suficiente para convertir la cola de propuestas en altas públicas.

## Artefacto de revisión

El libro `plan-ejecucion-4-puntos-xiclana.xlsx` contiene:
- Plan y resumen.
- Resolver coincidencias.
- Excluir ruido.
- Propuestas por confirmar.
- Revisión manual.
- Todas las candidatas.

El archivo se genera fuera del sitio público. No debe importarse directamente en producción. Tras revisar las propuestas, la siguiente operación será preparar una lista explícita de altas, fusiones y correcciones, y aplicar únicamente esa lista en una actualización controlada.

## Protección de producción

Durante esta fase no se modifica el repositorio original, la web V1 publicada, la rama principal ni Supabase. Los cambios documentales de esta fase permanecen en `feat/captura-catalogo-publico` y en la PR de trabajo pendiente de revisión.
