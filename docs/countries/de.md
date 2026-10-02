# Germany (DE) — integración territorial

**Evidence:** IMPLEMENTED (config + catálogo + adaptador nacional). **No** es piloto de campo ni autoridad de alerta.

## Autoridad de referencia

DWD / BBK

## Caso de integración

| Capa | ID | Etiqueta |
|------|-----|----------|
| País | `de.yaml` | INTEGRATION CASE |
| Región | `de-berlin` | INTEGRATION CASE |
| Sitio | `de-berlin-demo` | INTEGRATION CASE |

## Fuentes de datos

- Catálogo: `configs/data/catalog/de.yaml`
- Perfil país: `configs/countries/de.yaml`
- Precipitación proxy: Open-Meteo en `de-berlin-demo` (Metadata from versioned YAML catalog; precipitation via Open-Meteo (LIVE_INTEGRATED when reachable).)

## Amenazas prioritarias (config)

flood, heat, storm

## Descargo

POLARIS es apoyo a la decisión. No reemplaza a DWD / BBK ni emite alertas oficiales.
