"""National data adapters — catalog metadata ingest (INTEGRATION CASE countries)."""

from adapters.data.national.catalog_ingest import (
    NationalCatalogIngestResult,
    ingest_all_integration_countries,
    ingest_national_catalog,
    load_country_catalog,
    load_country_profile,
    result_to_dict,
)
from adapters.data.national.registry import (
    INTEGRATION_COUNTRY_ISO_CODES,
    list_integration_country_codes,
)

__all__ = [
    "INTEGRATION_COUNTRY_ISO_CODES",
    "NationalCatalogIngestResult",
    "ingest_all_integration_countries",
    "ingest_national_catalog",
    "list_integration_country_codes",
    "load_country_catalog",
    "load_country_profile",
    "result_to_dict",
]
