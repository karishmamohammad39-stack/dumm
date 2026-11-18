# E2E Test Infra: Vibe Cuts Engine

## Test Philosophy
- Opaque-box, requirement-driven. No dependency on implementation design.
- Methodology: Category-Partition + BVA + Pairwise + Workload Testing.

## Feature Inventory
| # | Feature | Source (requirement) | Tier 1 | Tier 2 | Tier 3 |
|---|---------|---------------------|:------:|:------:|:------:|
| 1 | Ingest raw video | ORIGINAL_REQUEST §R3, AC1 | 5 | 5 | ✓ |
| 2 | Extract audio | ORIGINAL_REQUEST §R1, AC2 | 5 | 5 | ✓ |
| 3 | Generate subtitles | ORIGINAL_REQUEST §R1, AC2 | 5 | 5 | ✓ |
| 4 | Apply speed curve | ORIGINAL_REQUEST §R1, AC3 | 5 | 5 | ✓ |
| 5 | Composite layers | ORIGINAL_REQUEST §R2, AC4 | 5 | 5 | ✓ |
| 6 | Masking shapes | ORIGINAL_REQUEST §R2, AC4 | 5 | 5 | ✓ |
| 7 | Dynamic blend modes | ORIGINAL_REQUEST §R2, AC4 | 5 | 5 | ✓ |
| 8 | Custom keyframing | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ |

## Test Architecture
- Test runner: `pytest e2e_tests/`
- Test case format: Python functions taking mock/sample media, expecting standard media output or API results.
- Directory layout: 
  - `e2e_tests/conftest.py` - test data generation and fixtures
  - `e2e_tests/test_tier1_feature.py` - Feature isolation tests
  - `e2e_tests/test_tier2_boundary.py` - Boundary and error tests
  - `e2e_tests/test_tier3_pairwise.py` - Cross-feature integration
  - `e2e_tests/test_tier4_workload.py` - Real-world scenarios

## Real-World Application Scenarios (Tier 4)
| # | Scenario | Features Exercised | Complexity |
|---|----------|--------------------|------------|
| 1 | TikTok-style auto-captioned edit | F1, F2, F3 | Medium |
| 2 | Speed-ramped action montage | F1, F2, F4 | Medium |
| 3 | Complex intro with masked text & blend | F1, F5, F6, F7, F8 | High |
| 4 | Picture-in-picture stream highlights | F1, F5, F8 | Medium |
| 5 | Full cinematic trailer (all effects) | F1, F2, F3, F4, F5, F6, F7, F8 | Very High |

## Coverage Thresholds
- Tier 1: ≥5 per feature
- Tier 2: ≥5 per feature (where boundaries exist)
- Tier 3: pairwise coverage of major feature interactions
- Tier 4: ≥5 realistic application scenarios
