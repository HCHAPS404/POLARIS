# Skill: data-engineering

## Purpose

Catalogs, adapters, lineage.

## When to invoke

adapters/data, data/, provenance.

## Inputs

Source name, license, schema.

## Workflow

1. Record license. 2. Map to observation schema. 3. No dumps in git.

## Outputs

Catalog entry or adapter stub.

## Validation

No secrets; contracts compile as YAML/JSON Schema.

## Forbidden shortcuts

Scraping paywalled data into the repo.

## Relevant paths

adapters/data/, data/catalog/, domains/provenance/
