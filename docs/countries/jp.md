# Japan (JP) — integración territorial

**Evidence:** IMPLEMENTED (config + catálogo + adaptador nacional). **No** es piloto de campo ni autoridad de alerta.

## Autoridad de referencia

JMA

## Caso de integración

| Capa | ID | Etiqueta |
|------|-----|----------|
| País | `jp.yaml` | INTEGRATION CASE |
| Región | `jp-kanto` | INTEGRATION CASE |
| Sitio | `jp-tokyo-demo` | INTEGRATION CASE |

## Fuentes de datos

- Catálogo: `configs/data/catalog/jp.yaml`
- Perfil país: `configs/countries/jp.yaml`
- Precipitación proxy: Open-Meteo en `jp-tokyo-demo` (Keyless public metadata HTTP configured in `configs/data/catalog`.)

## Amenazas prioritarias (config)

earthquake, tsunami, cyclone, volcano, flood

## Descargo

POLARIS es apoyo a la decisión. No reemplaza a JMA ni emite alertas oficiales.
