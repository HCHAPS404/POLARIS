# Spain (ES) — integración territorial

**Evidence:** IMPLEMENTED (config + catálogo + adaptador nacional). **No** es piloto de campo ni autoridad de alerta.

## Autoridad de referencia

AEMET / DGPCE

## Caso de integración

| Capa | ID | Etiqueta |
|------|-----|----------|
| País | `es.yaml` | INTEGRATION CASE |
| Región | `es-madrid` | INTEGRATION CASE |
| Sitio | `es-madrid-demo` | INTEGRATION CASE |

## Fuentes de datos

- Catálogo: `configs/data/catalog/es.yaml`
- Perfil país: `configs/countries/es.yaml`
- Precipitación proxy: Open-Meteo en `es-madrid-demo` (Metadata from versioned YAML catalog; precipitation via Open-Meteo (LIVE_INTEGRATED when reachable).)

## Amenazas prioritarias (config)

flood, wildfire, heat, drought

## Descargo

POLARIS es apoyo a la decisión. No reemplaza a AEMET / DGPCE ni emite alertas oficiales.
