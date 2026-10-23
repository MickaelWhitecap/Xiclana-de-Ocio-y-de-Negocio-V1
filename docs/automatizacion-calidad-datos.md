# Automatización de calidad de datos — fase piloto

## Objetivo

Reducir la revisión manual de fichas aplicando reglas reproducibles, puntuación por campo, detección conservadora de posibles duplicados y una cola de excepciones.

## Estado de esta fase

Esta implementación es una **simulación de solo lectura**. El programa \`motor_calidad.py\`:

- Lee \`manuales.json\`, \`oficiales.json\`, \`turismo.json\` y, si existe, \`datos/osm.json\`.
- Calcula propuestas de valor por campo según prioridades explícitas y corroboración entre fuentes.
- Identifica pares candidatos a duplicado con señales explicables.
- Informa de campos ausentes y posibles alternativas.
- No escribe en \`data.json\`, no modifica los archivos de origen, no accede a Supabase y no publica fichas.

No se debe conectar todavía al flujo de publicación semanal ni activar escrituras automáticas.

## Prioridad inicial por campo

Las puntuaciones son reglas operativas iniciales, no probabilidades estadísticas. Deben calibrarse con una muestra etiquetada antes de permitir actualizaciones automáticas.

| Campo | Prioridad inicial |
|---|---|
| Nombre, tipo, categoría | Ficha manual; Ayuntamiento; Turismo; OSM |
| Dirección | Ficha manual; Ayuntamiento; Turismo; OSM |
| Teléfono y correo | Ficha manual; Ayuntamiento/Turismo; OSM |
| Web | Ficha manual; Ayuntamiento; Turismo; OSM |
| Descripción | Ficha manual; Turismo; Ayuntamiento; OSM |
| Coordenadas | OSM cuando existan y sean coherentes; después las otras fuentes |

La jerarquía no sustituye validaciones: cada campo se valida por separado. Un campo vacío no se trata como información contradictoria. La coincidencia de varias fuentes añade confianza, pero no compensa una fuente sin autoridad o una señal de identidad débil.

## Decisiones conservadoras

- Un posible duplicado se informa; no se fusiona automáticamente durante el piloto.
- Una similitud de nombre por sí sola no basta para marcar una identidad como segura.
- No se elimina ni se marca como cerrado un negocio por ausencia de datos.
- Los cambios manuales y los overrides de Supabase deberán protegerse como una capa separada al diseñar la integración.
- La puntuación no es una probabilidad estadística.
- Ninguna escritura en la web pública se habilita en esta fase.

## Ejecutar localmente

Desde la raíz del repositorio:

\`\`\`bash
python motor_calidad.py
python -m unittest discover -s tests -v
\`\`\`

Para guardar el informe fuera de los datos públicos:

\`\`\`bash
python motor_calidad.py --output /tmp/informe-calidad-xiclana.json
\`\`\`

No uses \`data.json\` como destino. El programa bloquea explícitamente ese nombre.

## Umbrales propuestos para una futura fase

- 85–100: candidato a automatización solo para campos no conflictivos, tras calibración y aprobación del piloto.
- 60–84: revisión selectiva.
- 0–59: no actualizar automáticamente.

Antes de activar la primera banda habrá que comprobar precisión y falsos positivos sobre fichas revisadas. Además, siempre se bloquearán automáticamente la eliminación definitiva, los cierres no confirmados, las identidades dudosas, las contradicciones de contacto y los cambios sobre datos manuales protegidos.

## Siguiente fase

1. Ejecutar la simulación y revisar sus resultados.
2. Ajustar las reglas con ejemplos reales etiquetados.
3. Diseñar las tablas de procedencia, evidencia, coincidencias y cola de revisión en Supabase.
4. Probar integración de solo lectura con los overrides y propuestas actuales.
5. Solo tras validar el piloto, proponer por separado la activación de actualizaciones automáticas.
