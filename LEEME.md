# Guía paso a paso: tu sitio de Chiclana que se actualiza solo

Tiempo estimado: unos 30 minutos, una sola vez. Coste: 0 €. No necesitas saber programar: solo hacer clic y copiar/pegar.

## 1. Qué es cada cosa (vocabulario)

- **GitHub**: una web gratuita (github.com) donde se guardan archivos. La usaremos como "almacén" y como "máquina que trabaja por ti".
- **Repositorio**: una carpeta tuya dentro de GitHub. Aquí guardaremos los archivos del sitio.
- **GitHub Actions**: un robot de GitHub. Le das unas instrucciones escritas en un archivo y las cumple solo, en el horario que le digas.
- **GitHub Pages**: el servicio de GitHub que convierte tu carpeta en una página web pública con su dirección.
- **OpenStreetMap (OSM)**: un mapa mundial gratuito que mantiene la gente, como una Wikipedia de mapas. Contiene comercios y lugares con nombre, dirección, teléfono, web y horario.
- **JSON**: un archivo de texto con datos ordenados. `data.json` es la lista de todos los sitios.

## 2. Cómo funciona (la idea completa)

Cada lunes de madrugada el robot de GitHub: (1) pregunta a OpenStreetMap "dame todos los comercios y lugares de Chiclana", (2) los ordena y los guarda en `data.json`, (3) añade tus fichas manuales de `manuales.json`, (4) publica la web con los datos nuevos. Tú no haces nada.

## 3. Qué hay en esta carpeta

| Archivo | Para qué sirve |
|---|---|
| `index.html` | La página web que ven los visitantes. |
| `actualizar.py` | El programa que descarga y ordena los datos de OpenStreetMap. |
| `manuales.json` | Tus fichas escritas a mano (las 13 iniciales). Siempre tienen prioridad y nunca se borran. |
| `actualizar.yml` | Las instrucciones para el robot (cuándo y qué hacer). |
| `LEEME.md` | Esta guía. |

## 4. Puesta en marcha

**Paso 1 – Cuenta.** Entra en github.com, pulsa **Sign up** y crea una cuenta con tu correo. Confirma el correo que te envíen.

**Paso 2 – Repositorio.** Con la sesión iniciada, pulsa el botón **+** (arriba a la derecha) y elige **New repository**.
- *Repository name*: escribe `chiclana`.
- Marca **Public** (público; es necesario para que la web sea gratuita).
- Marca **Add a README file**.
- Pulsa **Create repository**.

**Paso 3 – Subir los archivos.** En tu repositorio pulsa **Add file → Upload files**. Arrastra estos 4 archivos: `index.html`, `actualizar.py`, `manuales.json`, `LEEME.md`. Abajo pulsa **Commit changes** (significa "guardar").

**Paso 4 – Crear el archivo del robot.** Este archivo va dentro de una carpeta oculta, por eso se crea a mano:
1. Pulsa **Add file → Create new file**.
2. En el cuadro del nombre escribe exactamente `.github/workflows/actualizar.yml` (al escribir cada `/` GitHub crea una carpeta).
3. Abre el archivo `actualizar.yml` de esta carpeta con el Bloc de notas, selecciona todo (Ctrl+A), copia (Ctrl+C) y pega (Ctrl+V) en el cuadro grande de GitHub.
4. Pulsa **Commit changes** y confirma.

**Paso 5 – Activar la web.** Ve a **Settings** (pestaña de arriba del repositorio) → **Pages** (menú de la izquierda). En *Build and deployment → Source* elige **GitHub Actions**.

**Paso 6 – Primera ejecución.** Ve a la pestaña **Actions**. Si te pide activarlas, acepta. Elige **Actualizar sitio** (izquierda) → **Run workflow** → **Run workflow**. Espera de 2 a 5 minutos y recarga. Verás una línea con un símbolo:
- 🟡 amarillo: trabajando.
- ✅ verde: terminado.
- ❌ rojo: ha fallado. Pulsa sobre ella, copia el texto del error y envíamelo.

**Paso 7 – Ver tu web.** Su dirección será `https://TU_USUARIO.github.io/chiclana/` (cambia TU_USUARIO por el nombre de tu cuenta). También aparece en Settings → Pages.

Desde aquí, se actualiza sola cada lunes. Si subes cualquier archivo nuevo, también se actualiza en ese momento.

## 5. Cómo añadir o corregir una ficha a mano

Abre `manuales.json` en GitHub, pulsa el lápiz ✏️ y añade una ficha copiando este formato (cuidado con las comas entre fichas):

```
{"n":"Nombre del sitio","t":"negocio","c":"Categoría","a":"Dirección","p":"956000000","w":"https://ejemplo.es","d":"Descripción breve"}
```
`t` solo puede ser `"ocio"` o `"negocio"`. Pulsa **Commit changes**; la web se actualiza en unos minutos. Si una ficha manual tiene el mismo nombre que una de OpenStreetMap, gana la tuya.

Truco: cualquier negocio puede darse de alta gratis en openstreetmap.org, y aparecerá aquí en la siguiente actualización.

## 6. Límites que debes conocer

- OpenStreetMap **no tiene todos los negocios**, sobre todo los pequeños. Si falta uno, añádelo como ficha manual.
- Los horarios y teléfonos son tan buenos como los que haya introducido la gente.
- GitHub **desactiva las tareas programadas si el repositorio pasa 60 días sin ninguna actividad**. Te avisarán por correo; se reactiva con un clic en la pestaña Actions.
- Si la descarga falla un lunes, el programa se detiene a propósito y la web conserva los datos anteriores (nunca se queda vacía).

## 7. Poner una foto de fondo en la cabecera (opcional)

1. Busca una foto que tengas derecho a usar: la tuya, una con permiso escrito, o una con licencia libre (por ejemplo en commons.wikimedia.org; cada foto indica su autor y su licencia).
2. Guárdala en tu ordenador con el nombre exacto `fondo.jpg` (en minúsculas). Mejor que pese menos de 1 MB.
3. En tu repositorio pulsa **Add file → Upload files**, arrastra `fondo.jpg` y pulsa **Commit changes**.
4. Si la licencia pide citar al autor (casi todas las libres lo piden), crea otro archivo: **Add file → Create new file**, nómbralo `fondo.txt` y escribe una línea, por ejemplo: `Foto: Nombre del autor, licencia CC BY-SA 4.0`. Pulsa **Commit changes**.
5. Espera 1 o 2 minutos a que termine la pestaña **Actions** y recarga la web con Ctrl+F5.

Si no existe `fondo.jpg`, la página muestra el mosaico de salinas.

## 8. Espacios destacados de pago (laterales)

La web tiene dos espacios fijos, uno a cada lado, que se quedan visibles mientras se baja por la página. En pantallas anchas (de unos 1200 píxeles de ancho en adelante) salen en los márgenes. En pantallas más estrechas, como móviles y portátiles, esos negocios salen en una franja horizontal bajo los botones Ocio y Negocio, para que no pierdan visibilidad.

**Cómo añadir un negocio que ha pagado un mes**
1. En tu repositorio abre `destacados.json` y pulsa el lápiz ✏️.
2. Dentro de los corchetes de `"espacios": []` pega un bloque como este (con una coma entre bloques si hay varios):
```
{"n":"Nombre del negocio","c":"Restaurante","lema":"Una frase corta","p":"956 000 000","w":"https://www.ejemplo.es","lado":"izquierda","desde":"2026-11-01","hasta":"2026-11-30"}
```
3. `lado` es `"izquierda"` o `"derecha"`. Las fechas van como año-mes-día.
4. **Pon siempre la fecha `hasta`.** Si falta, el anuncio no caduca nunca.
5. Pulsa **Commit changes**. En 1 o 2 minutos aparece. Cuando pasa la fecha `hasta`, desaparece solo.

**Cartel "Tu negocio aquí"**
Si escribes un correo o un enlace de WhatsApp en `"contacto"`, los espacios libres muestran un cartel con un enlace para reservar. Si lo dejas vacío, los espacios libres se ven igualmente con el cartel, pero sin enlace para reservar.

**Notas**
- Cada tarjeta lleva la etiqueta "Destacado · Publicidad", porque la publicidad tiene que poder identificarse como tal. Los enlaces llevan la marca `sponsored`, la recomendada para enlaces de pago.
- El logo "ON" indica promoción especial. Si el anunciante tiene una oferta, escríbela en el campo opcional `"promo"` (con sus condiciones y hasta cuándo vale) y saldrá destacada en la tarjeta. Si el logo promete una promoción, conviene que cada anuncio diga en qué consiste. Confírmalo con tu gestor.
- Cada lado muestra como máximo dos negocios a la vez.
- La fecha se comprueba con el reloj de quien visita la web.
- El cobro, la factura y el IVA los gestionas aparte. Consúltalo con tu gestor.
