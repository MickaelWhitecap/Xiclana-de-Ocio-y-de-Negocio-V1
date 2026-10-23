# Cobertura integral de categorías y fuentes públicas de Xiclana

## Estado y límites

Este documento prepara la ampliación del inventario para la rama de trabajo `feat/cobertura-categorias-fuentes`. Es un diseño de investigación; no modifica la web pública, `data.json`, las fuentes existentes, el flujo semanal ni Supabase. No implica que todas las categorías estén ya descargadas o verificadas.

El objetivo es descubrir actividades y servicios de Chiclana de la Frontera, contrastar cada campo por separado y registrar la procedencia. La cobertura real se medirá con una ejecución de búsqueda y un informe de recuentos, no se dará por supuesta.

## Taxonomía amplia inicial

Una ficha puede tener una categoría principal y varias etiquetas secundarias. La lista es deliberadamente extensa; solo se crearán categorías públicas cuando existan fichas pertinentes y se mantenga una taxonomía legible.

### Comercio y alimentación
- Alimentación general, supermercados, tiendas de barrio, ultramarinos, mercados y puestos, fruterías, verdulerías, panaderías, pastelerías, confiterías, carnicerías, charcuterías, pescaderías, marisquerías, congelados, comida preparada, delicatessen, productos ecológicos, productos locales, bodegas y vinotecas.
- Ropa, calzado, complementos, bolsos, joyería, relojería, óptica, perfumería, cosmética, droguería, papelería, librería, juguetes, regalos, bazar, electrónica, telefonía, informática, electrodomésticos, muebles, colchones, decoración, iluminación, bricolaje, ferretería, pinturas, materiales de construcción, jardinería, floristería, artículos deportivos, bicicletas, mascotas, acuarios, instrumentos musicales, telas, mercería, segunda mano y reparación/venta de artículos usados.
- Estancos y otros comercios especializados cuando proceda.

### Hostelería, ocio nocturno y eventos
- Restaurantes por tipo de cocina, bares, tabernas, ventas, cafeterías, churrerías, heladerías, pubs, discotecas, salas de música, coctelerías, comida rápida, comida para llevar, catering, salones de celebraciones, fincas de eventos y espacios para reuniones.
- Chiringuitos, terrazas y establecimientos estacionales; distinguir temporada de cierre definitivo.

### Turismo, alojamiento y experiencias
- Hoteles, hostales, pensiones, apartamentos turísticos, casas rurales, viviendas y alojamientos anunciados legalmente, campings, áreas de autocaravanas, albergues, agencias de viaje, guías, visitas, rutas, actividades ecuestres, náuticas, surf, kayak, pesca recreativa, golf, turismo activo, experiencias gastronómicas y visitas a salinas/bodegas.
- Playas, accesos, servicios de playa, miradores, puntos de interés, patrimonio, museos, centros de interpretación, monumentos y rutas culturales/naturales.

### Automoción, transporte y movilidad
- Concesionarios, compraventas, talleres, mecánica, electricidad, chapa y pintura, neumáticos, recambios, ITV, lavaderos, detailing, grúas, alquiler de vehículos, autoescuelas, taxis, VTC cuando consten en fuentes autorizadas, autobuses, estaciones/paradas, aparcamientos públicos y privados, parkings, áreas de estacionamiento de autocaravanas, puntos de recarga eléctrica, gasolineras y estaciones de servicio.

### Vivienda, construcción y servicios profesionales
- Inmobiliarias, administradores de fincas, alquileres, arquitectura, ingeniería, reformas, albañilería, electricidad, fontanería, climatización, carpintería, cerrajería, cristalería, alarmas, limpieza, control de plagas, mudanzas, jardinería, piscinas, mantenimiento, energía solar, telecomunicaciones y suministros.
- Abogacía, notarías, gestorías, asesorías fiscales/laborales, contabilidad, seguros, consultoría, traducción, diseño, fotografía, impresión, marketing, informática, reparación tecnológica, agencias y servicios a empresas.

### Salud, cuidados y bienestar
- Centros médicos, consultas, especialidades, odontología, fisioterapia, podología, psicología, ópticas, farmacias, ortopedias, veterinarios, hospitales/urgencias, laboratorios y centros de diagnóstico, siempre usando fuentes públicas apropiadas.
- Peluquerías, barberías, estética, uñas, spas, masajes, centros deportivos y bienestar. No inferir datos de salud ni publicar información personal de profesionales que no actúen como contacto profesional público.

### Educación, infancia y apoyo
- Escuelas infantiles, colegios, institutos, academias, idiomas, música, danza, arte, formación profesional, formación para empresas, apoyo escolar, bibliotecas, ludotecas, parques infantiles, actividades extraescolares y centros de formación vial.

### Deporte, cultura y asociaciones
- Gimnasios, clubes, polideportivos, piscinas, pistas, campos, clubes de pádel/tenis, fútbol, baloncesto, atletismo, artes marciales, yoga, pilates, baile, equitación, golf, deportes acuáticos y alquiler de equipamiento.
- Teatros, cines, salas, galerías, espacios culturales, talleres, asociaciones, peñas, hermandades, clubes, centros cívicos y actividades municipales; diferenciar entidad, sede y evento temporal.

### Servicios públicos, comunidad y naturaleza
- Ayuntamiento y dependencias, oficinas públicas, policía, bomberos, protección civil, Correos, servicios sociales, centros de mayores, centros de día, instalaciones deportivas municipales, puntos limpios, recogida de residuos, fuentes, baños públicos, parques, jardines, áreas recreativas, espacios naturales, salinas, senderos, zonas de observación, playas y accesos.
- Iglesias y lugares de culto como puntos de interés público; cementerios, tanatorios y servicios funerarios.
- Asociaciones vecinales, ONG y entidades sociales con datos de contacto publicados por la propia entidad.

### Servicios cotidianos y otros
- Lavanderías, tintorerías, costura, reparación de calzado, cerrajeros, copisterías, mensajería, paquetería, guardamuebles, fotógrafos, peluquería canina, cuidadores/servicios domésticos anunciados profesionalmente, alquiler de equipos y otros servicios locales que aparezcan en fuentes fiables.

## Fuentes y uso previsto

Orden de búsqueda recomendado; la prioridad se evalúa por campo, no se aplica una única fuente ganadora a toda la ficha.

1. **Fuentes del propio negocio:** web oficial, página de contacto, perfiles empresariales gestionados por el establecimiento y cartelería/datos recogidos directamente por el propietario o por el equipo de Xiclana. Para teléfonos, la web oficial o la fachada pueden ser más actuales que un directorio antiguo.
2. **Fuentes oficiales:** Ayuntamiento de Chiclana, portal municipal/turístico, Junta de Andalucía, registros públicos sectoriales cuando su reutilización esté permitida, datos abiertos y organismos públicos.
3. **OpenStreetMap:** datos abiertos con etiquetas de contacto, horarios, accesibilidad y ubicación cuando existan; respetar licencia ODbL, atribución y obligaciones de base de datos derivada.
4. **Directorios y asociaciones sectoriales:** cámaras, asociaciones empresariales, colegios profesionales y guías locales; comprobar las condiciones de reutilización de cada fuente.
5. **Buscadores y plataformas:** utilizarlos para descubrir la web oficial o localizar una fuente autorizada. No asumir que aparecer en un resultado autoriza a copiar y almacenar su contenido.
6. **Aportaciones de usuarios y visitas presenciales:** guardar fecha, método y quién verificó; no reemplazar silenciosamente valores conflictivos.

## Google y otros directorios cerrados

No realizar scraping, descarga masiva ni copia persistente de nombres, teléfonos, direcciones, reseñas, fotos o fichas de Google Maps para construir el directorio. Las condiciones de Google Maps Platform restringen extraer/almacenar contenido para reutilizarlo fuera del servicio y crear bases de datos de fichas de empresas a partir de ese contenido.

Uso prudente: emplear Google como punto de descubrimiento manual para encontrar el sitio oficial del negocio; después capturar los datos desde la web propia, un registro abierto o una fuente con permiso de reutilización. Si se desea integrar Places API, revisar sus condiciones EEE, atribución, almacenamiento y coste antes de diseñar el flujo. No importar reseñas ni fotografías sin licencia. Véase:
- https://cloud.google.com/terms/maps-platform/es-419
- https://developers.google.com/maps/documentation/javascript/policies?hl=es-419
- https://www.google.es/intl/es_ALL/help/terms_maps/

## Campos que se intentarán recoger

- Identidad: nombre, alias comercial, categoría principal, etiquetas, descripción literal o resumen autorizado, estado de actividad cuando haya evidencia.
- Ubicación: dirección, código postal, zona/barrio, latitud/longitud y tipo de lugar.
- Contacto profesional público: teléfono, correo genérico/profesional, web oficial, formulario de contacto y enlaces sociales oficiales.
- Servicio: horarios y excepciones/temporada, servicios ofrecidos, accesibilidad, reservas, entrega, recogida, aparcamiento y otros atributos publicados.
- Procedencia: URL o referencia de origen, tipo de fuente, fecha de consulta, fecha de la última verificación, campo obtenido, evidencia breve, licencia/condición de reutilización y nivel de confianza.
- Calidad: conflictos entre fuentes, dato ausente, posible duplicado, fuente caducada y razón de cualquier propuesta.
- No almacenar reseñas completas, fotos de terceros ni datos personales innecesarios.

## Selección de valores por campo

- No hay una jerarquía universal: un registro municipal puede ser mejor para la categoría administrativa; la web del negocio para el teléfono; OSM para coordenadas abiertas; la página oficial para horarios; una visita reciente para confirmar el rótulo.
- Priorizar evidencia reciente, fuente primaria, formato válido y corroboración independiente.
- Una coincidencia de teléfono no demuestra por sí sola que dos fichas sean el mismo negocio: puede ser centralita, franquicia o gestoría compartida.
- Los valores en conflicto se conservan como alternativas con su procedencia. No se sustituye un dato manual protegido ni se borra una ficha por falta de evidencia.
- No inferir cierre a partir de ausencia en una fuente. Usar estados como `activo_confirmado`, `posible_cierre` y `sin_verificar` con evidencia y fecha.

## Resultado exigido antes de publicar

La búsqueda debe producir un informe separado de la web pública con:
1. total de entidades descubiertas por fuente y categoría;
2. nuevas entidades candidatas y posibles coincidencias con las 1.013 fichas actuales;
3. porcentaje de cobertura por campo;
4. teléfonos, webs y direcciones con evidencia/procedencia;
5. conflictos y candidatos a duplicado;
6. fuentes fallidas, límites de cobertura y fecha de ejecución;
7. resumen de licencias y restricciones de cada fuente.

No activar publicación automática hasta comparar el informe con el catálogo actual, validar una muestra representativa y confirmar que los overrides manuales de Supabase permanecen intactos.
