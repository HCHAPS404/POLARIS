# Skill: mobile

## Purpose

Flutter Horizon Mobile.

## When to invoke

apps/horizon-mobile or ADR-0003 work.

## Inputs

Field user story, offline needs.

## Workflow

1. Confirm pubspec. 2. If missing, do not scaffold a full app. 3. Keep CI skip behaviour.

## Outputs

Mobile note or later Dart slice.

## Validation

mobile.yml skips without pubspec.

## Forbidden shortcuts

Commit a generated Flutter counter app as the product.

## Relevant paths

apps/horizon-mobile/, docs/adr/0003-flutter-mobile.md
