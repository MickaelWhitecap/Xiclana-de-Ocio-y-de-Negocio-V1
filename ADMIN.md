# Panel privado de administración de Xiclana

El panel está en `admin.html`. La web pública sigue siendo GitHub Pages. Las ediciones se guardan en Supabase y la página pública solo las lee; los permisos de escritura se validan en la base de datos.

## Configuración inicial (una sola vez)

1. Crea un proyecto en [Supabase](https://supabase.com/) con tu propia cuenta.
2. En **Authentication → Users**, crea tu usuario administrador con tu correo y una contraseña robusta. No habilites el registro público de usuarios; desactiva las altas públicas en la configuración de Authentication.
3. Abre **SQL Editor**, copia el contenido de `supabase-schema.sql`, sustituye `ADMIN_EMAIL_HERE` por el correo exacto de tu cuenta en las tres políticas y ejecuta el SQL.
4. En **Project Settings → API** (o Connect), copia la URL del proyecto y la clave pública **anon/publishable**. Edita `supabase-config.js` y rellena `url` y `anonKey`.
   - La URL y la clave anon/publishable son públicas por diseño; la seguridad depende de las políticas RLS.
   - **Nunca** copies la clave `service_role`, una contraseña ni un secreto privado en archivos de este repositorio.
5. Guarda los cambios en el repositorio V1. GitHub Actions publicará la versión actualizada.
6. Abre `https://mickaelwhitecap.github.io/Xiclana-de-Ocio-y-de-Negocio-V1/admin.html` e inicia sesión con tu cuenta.

## Uso

- Busca una ficha por nombre, categoría o dirección.
- Selecciónala, modifica sus campos y pulsa **Guardar ficha**.
- Pulsa **Nueva ficha** para incorporar un establecimiento visitado personalmente.
- Los datos guardados se almacenan en Supabase y la web pública los incorpora al cargar.
- La ficha muestra su estado de verificación y fecha de última comprobación.

## Protección de datos

- La tabla permite lectura pública porque las fichas forman parte del directorio público.
- Las operaciones de escritura se limitan mediante Row Level Security (RLS) a la dirección de correo autorizada en el SQL.
- El registro de nuevos usuarios debe estar desactivado. No compartas la contraseña.
- No se usa una clave service_role en el navegador.
- El panel no incluye un botón de borrado de fichas base para evitar eliminaciones accidentales.

## Nota técnica

El flujo de publicación genera `data.json` desde las fuentes existentes. Los cambios del panel se guardan por separado, de modo que una actualización de OpenStreetMap no los borra. Para fichas nuevas y cambios manuales, el identificador se mantiene en la tabla de Supabase.
