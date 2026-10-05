# Implementer Guide

## Development order
1. `SourceVaultService` + workspace/storage
2. parser/OCR adapters
3. SourceLocation + TextLayer + Segment
4. entity/time/place
5. claim/observation
6. evidence/conflict
7. source criticism/genealogy/variants
8. model control
9. acquisition connectors
10. research layer
11. UI
12. real-world tests

## Rule
实现顺序可调，但不可改变 Domain Contract。
