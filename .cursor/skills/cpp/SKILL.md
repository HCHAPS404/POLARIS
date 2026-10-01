# Skill: cpp

## Purpose

C++20 kernels and CMake.

## When to invoke

simulation/cpp, CMakeLists.txt.

## Inputs

Kernel name, numerical spec.

## Workflow

1. C++20. 2. Test executable. 3. Keep placeholder tiny until P3.

## Outputs

Library + test.

## Validation

make test-cpp or equivalent CI job.

## Forbidden shortcuts

Header-only physics without tests.

## Relevant paths

simulation/cpp/, CMakeLists.txt
