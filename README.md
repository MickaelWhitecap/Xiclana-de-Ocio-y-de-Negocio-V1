# Xiclana de Ocio y de NegOcio

Directorio web de ocio y negocios de Chiclana de la Frontera (Cádiz).

- **`index.html`**: la página. Lee `data.json`, que se genera sola.
- **`actualizar.py`** y **`.github/workflows/actualizar.yml`**: el robot que cada lunes reúne los datos y publica la web.
- **`manuales.json`**: fichas escritas a mano (tienen prioridad sobre las demás fuentes).
- **`oficiales.json`**: datos del Ayuntamiento (Portal de Datos Abiertos, licencia ODC-By).
- **`turismo.json`**: datos de la web de Turismo de Chiclana (solo datos sueltos).
- **`destacados.json`**: negocios que pagan un espacio destacado, con fechas.
- **`datos/osm.json`**: copia de seguridad de los datos de OpenStreetMap (la crea el robot).

Fuentes: © colaboradores de OpenStreetMap (licencia ODbL) y Ayuntamiento de Chiclana, Portal de Datos Abiertos (licencia ODC-By).
Guía paso a paso para el propietario: ver `LEEME.md`.


## V3 de revisión

- Web pública de revisión: `https://mickaelwhitecap.github.io/Xiclana-de-Ocio-y-de-Negocio-V1/v3/`
- Administración de prueba: `https://mickaelwhitecap.github.io/Xiclana-de-Ocio-y-de-Negocio-V1/v3/admin.html`
- `v3/manuales.json`: ocho instalaciones deportivas municipales confirmadas incorporadas sin tocar el catálogo de producción.
- `v3/informe-investigacion.json`: resumen de la segunda pasada de verificación.
- La Administración V3 guarda borradores solo en el navegador; no escribe en Supabase.
