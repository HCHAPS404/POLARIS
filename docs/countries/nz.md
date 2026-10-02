# New Zealand (NZ) — integración territorial

**Evidence:** IMPLEMENTED (config + catálogo + adaptador nacional). **No** es piloto de campo ni autoridad de alerta.

## Autoridad de referencia

MetService / NEMA

## Caso de integración

| Capa | ID | Etiqueta |
|------|-----|----------|
| País | `nz.yaml` | INTEGRATION CASE |
| Región | `nz-auckland` | INTEGRATION CASE |
| Sitio | `nz-auckland-demo` | INTEGRATION CASE |

## Fuentes de datos

- Catálogo: `configs/data/catalog/nz.yaml`
- Perfil país: `configs/countries/nz.yaml`
- Precipitación proxy: Open-Meteo en `nz-auckland-demo` (Keyless public metadata HTTP configured in `configs/data/catalog`.)

## Amenazas prioritarias (config)

earthquake, tsunami, volcano, flood

## Descargo

POLARIS es apoyo a la decisión. No reemplaza a MetService / NEMA ni emite alertas oficiales.
