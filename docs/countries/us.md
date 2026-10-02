# United States (US) — integración territorial

**Evidence:** IMPLEMENTED (config + catálogo + adaptador nacional). **No** es piloto de campo ni autoridad de alerta.

## Autoridad de referencia

NWS / FEMA

## Caso de integración

| Capa | ID | Etiqueta |
|------|-----|----------|
| País | `us.yaml` | INTEGRATION CASE |
| Región | `us-texas` | INTEGRATION CASE |
| Sitio | `us-houston-demo` | INTEGRATION CASE |

## Fuentes de datos

- Catálogo: `configs/data/catalog/us.yaml`
- Perfil país: `configs/countries/us.yaml`
- Precipitación proxy: Open-Meteo en `us-houston-demo` (Keyless public metadata HTTP configured in `configs/data/catalog`.)

## Amenazas prioritarias (config)

flood, cyclone, wildfire, earthquake, tornado

## Descargo

POLARIS es apoyo a la decisión. No reemplaza a NWS / FEMA ni emite alertas oficiales.
