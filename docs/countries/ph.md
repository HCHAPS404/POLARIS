# Philippines (PH) — integración territorial

**Evidence:** IMPLEMENTED (config + catálogo + adaptador nacional). **No** es piloto de campo ni autoridad de alerta.

## Autoridad de referencia

PAGASA / NDRRMC

## Caso de integración

| Capa | ID | Etiqueta |
|------|-----|----------|
| País | `ph.yaml` | INTEGRATION CASE |
| Región | `ph-ncr` | INTEGRATION CASE |
| Sitio | `ph-manila-demo` | INTEGRATION CASE |

## Fuentes de datos

- Catálogo: `configs/data/catalog/ph.yaml`
- Perfil país: `configs/countries/ph.yaml`
- Precipitación proxy: Open-Meteo en `ph-manila-demo` (Metadata from versioned YAML catalog; precipitation via Open-Meteo (LIVE_INTEGRATED when reachable).)

## Amenazas prioritarias (config)

cyclone, flood, earthquake, volcano

## Descargo

POLARIS es apoyo a la decisión. No reemplaza a PAGASA / NDRRMC ni emite alertas oficiales.
